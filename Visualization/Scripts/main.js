// Global variables
const size=6;
const preview=2;

const unitTime=400;

const width=380;
const unitSize=width/size;
const borderWidth=unitSize/size;

const remainedBarHeight=60;

const blockGap=unitSize/10;
const blockBorderRadius=unitSize/10;

const radiusGap=unitSize/9;

const graphWidth=260;
const strokeWidth=1;

const board=document.getElementById("board");

const currentBoard={};

const player={0:'left',1:'right'}
// Green Blue Orange Pink Colors
const colorArray=["rgb(13, 211, 82)","rgb(22, 218, 224)","rgb(224, 134, 60)","rgb(243, 121, 137)","rgb(244, 67, 54)","rgb(255, 193, 7)","rgb(96, 125, 139)","rgb(0, 188, 212)","rgb(103, 58, 183)","rgb(233, 30, 99)","rgb(255, 152, 0)","rgb(3, 169, 244)"];
let colorShift=5;

let currentFrame=0;
let isPlaying=false;

const playtoolsContainer=document.getElementById('playtools-container');
const playButton=playtoolsContainer.querySelector('#play');
const stopButton=playtoolsContainer.querySelector('#stop');
const speedButton=playtoolsContainer.querySelector('#speed');
const speedInput=speedButton.previousElementSibling;
const jumpButton=playtoolsContainer.querySelector('#jump');
const jumpInput=jumpButton.previousElementSibling;
const currentTurnNumber=playtoolsContainer.querySelector('#current-turn');
// const currentTurnStartNumber=playtoolsContainer.querySelector('#current-turn-start')
const startOrEnd=playtoolsContainer.querySelector('#start-or-end')
const currentFrameNumber=playtoolsContainer.querySelector('#current-frame');
const totalFrameNumber=playtoolsContainer.querySelector('#total-frame');
const lastButton=playtoolsContainer.querySelector('#last');
const nextButton=playtoolsContainer.querySelector('#next');



// 烦人的接口!
PLAYING_SPEED = 1;
PLAYING_FPS = 1.25;
// record_obj
// TOTAL_FRAMES
/////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////

// The file choser
// Get the object
const fileChooser=document.getElementById('file-chooser');
// Update the Chooser when it is chosen
const updateChooser=function(object){
  object.innerText='';
  object.classList.add('chosen');
  object.nextElementSibling.disabled=true;
  object.style.display="none";
  playtoolsContainer.style.display="block";
}
// Get the information of chosen file
const getInfo=function(file){
  const reader = new FileReader();

  reader.readAsText(file);
  reader.onload = function() {
    // The information abou the File
    const {name,type}=file;
    if (type === "application/json"){
      const record=JSON.parse(reader.result);
      // Initialization
      initialization(record);
    } else{
      alert('请选择一个咖啡脚本宾语注释文件！！！');
    }
  };
  reader.onerror = function() {
    console.log('Error ',reader.error);
  };
}
// Add Event Listeners
fileChooser.nextElementSibling.addEventListener('change',(event)=>{
  getInfo(event.target.files[0]);
  updateChooser(fileChooser);
},true)
/////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////
// Define the initialization function
function startPlaying(){
  if (!isPlaying){
    playingCache=setInterval(()=>{
      if (currentFrame<totalFrames){
        drawFrame(frames[currentFrame]);
        currentFrame++;
      }
    },650/PLAYING_SPEED)
    isPlaying=true;
  }
}
function stopPlaying(){
  clearInterval(playingCache);
  isPlaying=false;
}
let playingCache
let totalRemains,totalFrames,scores,exitStatus,errorMessage,winner,frames;
initialization=function(record){
  // Global variables
  totalFrames=record.totalFrames;
  scores=record.scores;
  exitStatus=record.exitStatus;
  errorMessage=record.errorMessage;
  winner=record.winner;
  frames=record.frames;
  totalRemains=record.totalRemains;

  totalFrameNumber.innerText=totalFrames-1;

  initializeGraph(scores);
  myChart.setOption(optionAbsolute);
  startPlaying();
}



// Define a function to draw a frame

function drawFrame(frame) {
  // Global variables
  const {turnNumber,currentPlayer,remainedBarStatus,boardStatus,sideBarStatus}=frame;

  document.documentElement.style.setProperty('--PLAYING_SPEED', PLAYING_SPEED);

  updateRemainedBar(remainedBarStatus);
  updateSideBar(sideBarStatus);
  updateBoard(boardStatus,player[currentPlayer]);
  updateCurrentFrameDisplay();
  updateCurrentTurnDisplay(turnNumber);
}
/////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////
// Define a function to draw the remained bar
const remainedBar=document.getElementsByClassName("remained-bar");
updateRemainedBar=function (remainedBarStatus) {
  for (i=0;i<remainedBarStatus.length;i++) {
    remainedBar[i].style.height=`${remainedBarStatus[i] / totalRemains * remainedBarHeight}px`;
  }
}
// Define a function to update the sidebars
const sideBar=document.getElementsByClassName("sidebar");
const leftTeamName=sideBar[0].querySelector('h3')
const rightTeamName=sideBar[1].querySelector('h3')
const leftItems = sideBar[0].querySelectorAll('div');
const rightItems = sideBar[1].querySelectorAll('div');
  // Status Dictionary
const statusDictionary={0:'持平',1:'领先','-1':'落后'}
  // NodeList(11) [div.status, div.total-scores, div.sidebar-header, div.numbers, div.highest-combo, div.sidebar-header, div.numbers, div.current-combos, div.sidebar-header, div.numbers, div.placeholder]
updateSideBar=function (sideBarStatus) {
  leftItems[0].children[0].innerText=statusDictionary[sideBarStatus.left.status];
  leftItems[3].innerText=sideBarStatus.left.totalScores;
  leftItems[6].innerText=sideBarStatus.left.highestCombo;
  leftItems[9].innerText=sideBarStatus.left.currentCombo;

  rightItems[0].children[0].innerText=statusDictionary[sideBarStatus.right.status];
  rightItems[3].innerText=sideBarStatus.right.totalScores;
  rightItems[6].innerText=sideBarStatus.right.highestCombo;
  rightItems[9].innerText=sideBarStatus.right.currentCombo;
}
// Define a function to update the board
  // Define a function to get the color of a piece
  getColor=function(pieceId){
    return colorArray[colorShift+parseInt(pieceId.slice(-1))];
  }
updateBoard=function(boardStatus,team='unknown'){
  for (let pieceId in currentBoard){
    if (!(pieceId in boardStatus)){
      eliminate(currentBoard[pieceId],team);
      delete currentBoard[pieceId];
    }
  }
  for (let pieceId in boardStatus){
    if (!(pieceId in currentBoard)){
      const piece=createPiece(pieceId,getColor(pieceId));
      currentBoard[pieceId]=piece;
      // moveTo(piece,size-1-boardStatus[pieceId][1],-2);
      moveTo(piece,boardStatus[pieceId][1],-2);
      piece.style.display='block';
      board.appendChild(piece);
      // Make the piece to appear
      setTimeout(()=>{
        // piece.style.display='block';
        piece.classList.add('appearing');
        // moveTo(piece,size-1-boardStatus[pieceId][1],size+preview-1-boardStatus[pieceId][0]);
        moveTo(piece,boardStatus[pieceId][1],size+preview-1-boardStatus[pieceId][0]);
        setTimeout(()=>{
          piece.classList.remove('appearing');
        },unitTime/PLAYING_SPEED);
      },25/PLAYING_SPEED);// The lag time here should be changed according to the play scale
    } else{
      const piece=currentBoard[pieceId];
      // moveTo(piece,size-1-boardStatus[pieceId][1],size+preview-1-boardStatus[pieceId][0]);
      moveTo(piece,boardStatus[pieceId][1],size+preview-1-boardStatus[pieceId][0]);
    }
  }
}
// Define a function to draw the score graph
updateScoreGraph=function(){
  
}
/////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////
// Create a template background block
function createTemplateBackgroundBlock(){
  let backgroundBlock=document.createElement("div");
  backgroundBlock.className="background-block";
  board.appendChild(backgroundBlock);
  return backgroundBlock;
}

templateBackgroundBlock=createTemplateBackgroundBlock();

// Define a function to initialize the gird on the board and run it
function initializeGrid() {
  for (let i=1;i<=size+preview;i++) {
    for (let j=1;j<=size;j++){
      let backgroundBlock=templateBackgroundBlock.cloneNode(true);
      if (i<=preview){
        backgroundBlock.style.backgroundColor="white";
        backgroundBlock.style.opacity="0.9";
      } else{
        backgroundBlock.style.backgroundColor="white";
        backgroundBlock.style.opacity="0.2";
      }
      backgroundBlock.style.left=`${borderWidth + (j-1) * unitSize + blockGap/2}px`;
      backgroundBlock.style.top=`${borderWidth + (i-1) * unitSize + blockGap/2}px`;

      board.appendChild(backgroundBlock);
    }
  }
}  

initializeGrid();

const remainedSection=document.getElementById('remained-bar-section');
// Define a function to initialize the remained bar
function initializeRemainedBar(){
  const remainedBarContainer=document.createElement('div');
  remainedBarContainer.className='remained-bar-container';

  const remainedBar=document.createElement('div');
  remainedBar.className='remained-bar';
  remainedBarContainer.appendChild(remainedBar);
  remainedSection.appendChild(remainedBarContainer);
}
for (let i=0;i<size;i++){
  initializeRemainedBar();
}

// Define a series of functions to create pieces with different colors

function createTemplatePiece() {
  let piece=document.createElement("div");
  piece.className="piece";
  return piece;
}
// Create a template piece
const templatePiece=createTemplatePiece()

// Create a piece with certain id and color
function createPiece(id,color) {
  let piece=templatePiece.cloneNode(true);
  piece.id=id;
  piece.style.backgroundColor=color;
  return piece;
}
/////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////
// Define a function to remove a piece
function remove(piece){
  piece.remove();
}
// Define a function to eliminate a piece
function eliminate(piece,team='unknown'){
  if (piece.style.display === "none") {
    return;
  } else{
  piece.classList.add("eliminated");
  piece.style.zIndex='90';
  setTimeout(function(){
    remove(piece);
  }
  ,unitTime/PLAYING_SPEED);// Need to be adjusted according to the play scale
  setTimeout(()=>{
    if (team==='unknown'){
      piece.style.top=`${borderWidth + (2+size) * unitSize + blockGap/2+radiusGap / 2}px`;
      }else if (team==="left") {
      piece.style.left=`${borderWidth +  (-2) * unitSize + blockGap/2+radiusGap / 2}px`;
      } else if (team==="right") {
      piece.style.left=`${borderWidth +  (2+size) * unitSize + blockGap/2+radiusGap / 2}px`;
      }
  },150/PLAYING_SPEED)
} 
}

// Define a function to move a piece
function moveTo(piece,x,y){
  piece.style.left=`${borderWidth + (x) * unitSize + blockGap/2+radiusGap / 2}px`;
  piece.style.top=`${borderWidth + (y) * unitSize + blockGap/2+radiusGap / 2}px`;
  // if (piece.style.display==="none") {
  //   piece.style.display="block";
  // }
}
/////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////
// A function for testing
function test() {
  for(i=0;i<size;i++){
    for (j=0;j<size+preview;j++){
      let piece=createPiece(`r${j}c${i}`,colorArray[colorShift+Math.floor(Math.random()*5)]);
      piece.style.display='block';
      moveTo(piece,i,j);
      board.appendChild(piece);
    }
  }
}
/////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////
// Event listener for the select dropdown (written by GPT-4)
document.addEventListener('DOMContentLoaded', () => {
  const selectElement = document.getElementById('scores-mode');
  const customSelect = selectElement.parentElement;

  const selected = document.createElement('div');
  selected.className = 'select-selected';
  selected.textContent = selectElement.options[selectElement.selectedIndex].textContent;
  customSelect.appendChild(selected);

  const itemsContainer = document.createElement('div');
  itemsContainer.className = 'select-items';
  customSelect.appendChild(itemsContainer);

  for (const option of selectElement.options) {
      const item = document.createElement('div');
      item.textContent = option.textContent;
      item.addEventListener('click', () => {
          selectElement.value = option.value;
          selected.textContent = option.textContent;
          itemsContainer.classList.remove('show');
          onSelectChange(option.value);
      });
      itemsContainer.appendChild(item);
  }

  selected.addEventListener('click', () => {
      itemsContainer.classList.toggle('show');
  });

  document.addEventListener('click', (event) => {
      if (!customSelect.contains(event.target)) {
          itemsContainer.classList.remove('show');
      }
  });
});

// Define a function to handle the change in the selected option
function onSelectChange(newValue) {
  console.log("Selected value changed to:", newValue);
  if (newValue==="difference"){
    myChart.setOption(optionRelative);
  } else if (newValue==="raw"){
    myChart.setOption(optionAbsolute);
  }
}





// For testing

const a={"turnNumber": 0, "currentPlayer": 0, "remainedBarStatus": [292, 292, 292, 292, 292, 292, 292, 292], "boardStatus": {"r0000c0000": [0, 0], "r0000c0001": [0, 1], "r0000c0002": [0, 2], "r0000c0003": [0, 3], "r0000c0004": [0, 4], "r0000c0005": [0, 5], "r0000c0006": [0, 6], "r0000c0007": [0, 7], "r0001c0000": [1, 0], "r0001c0001": [1, 1], "r0001c0002": [1, 2], "r0001c0003": [1, 3], "r0001c0004": [1, 4], "r0001c0005": [1, 5], "r0001c0006": [1, 6], "r0001c0007": [1, 7], "r0002c0000": [2, 0], "r0002c0001": [2, 1], "r0002c0002": [2, 2], "r0002c0003": [2, 3], "r0002c0004": [2, 4], "r0002c0005": [2, 5], "r0002c0006": [2, 6], "r0002c0007": [2, 7], "r0003c0000": [3, 0], "r0003c0001": [3, 1], "r0003c0002": [3, 2], "r0003c0003": [3, 3], "r0003c0004": [3, 4], "r0003c0005": [3, 5], "r0003c0006": [3, 6], "r0003c0007": [3, 7], "r0004c0000": [4, 0], "r0004c0001": [4, 1], "r0004c0002": [4, 2], "r0004c0003": [4, 3], "r0004c0004": [4, 4], "r0004c0005": [4, 5], "r0004c0006": [4, 6], "r0004c0007": [4, 7], "r0005c0000": [5, 0], "r0005c0001": [5, 1], "r0005c0002": [5, 2], "r0005c0003": [5, 3], "r0005c0004": [5, 4], "r0005c0005": [5, 5], "r0005c0006": [5, 6], "r0005c0007": [5, 7], "r0006c0000": [6, 0], "r0006c0001": [6, 1], "r0006c0002": [6, 2], "r0006c0003": [6, 3], "r0006c0004": [6, 4], "r0006c0005": [6, 5], "r0006c0006": [6, 6], "r0006c0007": [6, 7], "r0007c0000": [7, 0], "r0007c0001": [7, 1], "r0007c0002": [7, 2], "r0007c0003": [7, 3], "r0007c0004": [7, 4], "r0007c0005": [7, 5], "r0007c0006": [7, 6], "r0007c0007": [7, 7], "r0008c0000": [8, 0], "r0008c0001": [8, 1], "r0008c0002": [8, 2], "r0008c0003": [8, 3], "r0008c0004": [8, 4], "r0008c0005": [8, 5], "r0008c0006": [8, 6], "r0008c0007": [8, 7], "r0009c0000": [9, 0], "r0009c0001": [9, 1], "r0009c0002": [9, 2], "r0009c0003": [9, 3], "r0009c0004": [9, 4], "r0009c0005": [9, 5], "r0009c0006": [9, 6], "r0009c0007": [9, 7]}, "sideBarStatus": {"left": {"totalScores": 0, "highestCombo": 0, "currentCombo": 0, "status": 0}, "right": {"totalScores": 0, "highestCombo": 0, "currentCombo": 0, "status": 0}}};


const c={"turnNumber": 13, "currentPlayer": 1, "remainedBarStatus": [272, 238, 192, 195, 207, 221, 247, 269], "boardStatus": {"r0010c0000": [0, 0], "r0044c0001": [0, 1], "r0092c0002": [0, 2], "r0094c0003": [0, 3], "r0079c0004": [0, 4], "r0067c0005": [0, 5], "r0042c0006": [0, 6], "r0022c0007": [0, 7], "r0012c0000": [1, 0], "r0046c0001": [1, 1], "r0096c0002": [1, 2], "r0095c0003": [1, 3], "r0082c0004": [1, 4], "r0070c0005": [1, 5], "r0046c0006": [1, 6], "r0023c0007": [1, 7], "r0013c0000": [2, 0], "r0055c0001": [2, 1], "r0101c0002": [2, 2], "r0098c0003": [2, 3], "r0084c0004": [2, 4], "r0072c0005": [2, 5], "r0047c0006": [2, 6], "r0025c0007": [2, 7], "r0021c0000": [3, 0], "r0056c0001": [3, 1], "r0102c0002": [3, 2], "r0100c0003": [3, 3], "r0085c0004": [3, 4], "r0073c0005": [3, 5], "r0048c0006": [3, 6], "r0026c0007": [3, 7], "r0024c0000": [4, 0], "r0058c0001": [4, 1], "r0104c0002": [4, 2], "r0089c0004": [4, 3], "r0101c0003": [4, 4], "r0074c0005": [4, 5], "r0049c0006": [4, 6], "r0027c0007": [4, 7], "r0025c0000": [5, 0], "r0059c0001": [5, 1], "r0105c0002": [5, 2], "r0102c0003": [5, 3], "r0090c0004": [5, 4], "r0076c0005": [5, 5], "r0050c0006": [5, 6], "r0028c0007": [5, 7], "r0026c0000": [6, 0], "r0060c0001": [6, 1], "r0106c0002": [6, 2], "r0103c0003": [6, 3], "r0091c0004": [6, 4], "r0077c0005": [6, 5], "r0051c0006": [6, 6], "r0029c0007": [6, 7], "r0027c0000": [7, 0], "r0061c0001": [7, 1], "r0107c0002": [7, 2], "r0104c0003": [7, 3], "r0092c0004": [7, 4], "r0078c0005": [7, 5], "r0052c0006": [7, 6], "r0030c0007": [7, 7], "r0028c0000": [8, 0], "r0062c0001": [8, 1], "r0108c0002": [8, 2], "r0105c0003": [8, 3], "r0093c0004": [8, 4], "r0079c0005": [8, 5], "r0053c0006": [8, 6], "r0031c0007": [8, 7], "r0029c0000": [9, 0], "r0063c0001": [9, 1], "r0109c0002": [9, 2], "r0106c0003": [9, 3], "r0094c0004": [9, 4], "r0080c0005": [9, 5], "r0054c0006": [9, 6], "r0032c0007": [9, 7]}, "sideBarStatus": {"left": {"totalScores": 359, "highestCombo": 103, "currentCombo": 103, "status": -1}, "right": {"totalScores": 772, "highestCombo": 109, "currentCombo": 0, "status": 1}}}


/////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////
const chartDom = document.getElementById("chart");
const myChart = echarts.init(chartDom);

// myChart.setOption(optionRelative);
var optionRelative;
var optionAbsolute;

function initializeGraph(scores){
  optionRelative = {
    title: {
      text: '相对分数',
      left: 10
    },
    toolbox: {
      feature: {
        dataZoom: {
          yAxisIndex: false
        },
        saveAsImage: {
          pixelRatio: 2
        }
      }
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      }
    },
    grid: {
      bottom: 90
    },
    dataZoom: [
      {
        type: 'inside',
        yAxisIndex: [0]
      },
      {
        type: 'slider',
        yAxisIndex: [0]
      }
    ],
    yAxis: {
      // data: scores.relative,
      // data:data.categoryData,
      // data:data.relative,
      
      data:[0,...Array.from({length: scores.relative.length-1}, (_, i) => i + 1)],
      
      silent: false,
      splitLine: {
        show: false
      },
      splitArea: {
        show: false
      }
    },
    xAxis: {
      splitArea: {
        show: false
      }
    },
    series: [
      {
        type: 'line',
        // data: data.valueData,
        data:scores.relative,
        // Set `large` for large data amount
        large: true,
        itemStyle: {
          color: 'rgb(255, 70, 131)'
        },
        areaStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            {
              offset: 0,
              color: 'rgb(255, 158, 68)'
            },
            {
              offset: 1,
              color: 'rgb(255, 70, 131)'
            }
          ])
        },
      },
      {
        type: 'custom', // 使用 'custom' 类型
        renderItem: function() {}, // 定义一个空的 renderItem 函数
        data: [] // 无数据
      }
    ]
  };

  optionAbsolute = {
    title: {
      text: '绝对分数',
      left: 10
    },
    toolbox: {
      feature: {
        dataZoom: {
          yAxisIndex: false
        },
        saveAsImage: {
          pixelRatio: 2
        }
      }
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      }
    },
    grid: {
      bottom: 90
    },
    dataZoom: [
      {
        type: 'inside',
        yAxisIndex: [0]
      },
      {
        type: 'slider',
        yAxisIndex: [0]
      }
    ],
    yAxis: {
      data:[0,...Array.from({length: scores.right.length-1}, (_, i) => i + 1)],
      
      silent: false,
      splitLine: {
        show: false
      },
      splitArea: {
        show: false
      }
    },
    xAxis: {
      splitArea: {
        show: false
      }
    },
    series: [
      // {
      //   type: 'none',
      // },
      {
        type: 'line',
        // data: data.valueData,
        data:scores.left,
        // Set `large` for large data amount
        large: true,
        itemStyle: {
          color: 'rgb(5, 5, 153)'
        },
        areaStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            {
              offset: 0,
              color: 'rgb(5, 5, 153, 0.15)'
            },
            {
              offset: 1,
              color: 'rgb(5, 5, 153, 0.4)'
            }
          ])
        },
      },
      {
        type: 'line',
        // data: data.valueData,
        data:scores.right,
        // Set `large` for large data amount
        large: true,
        itemStyle: {
          color: 'rgb(153, 5, 5)'
        },
        areaStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            {
              offset: 0,
              color: 'rgb(153, 5, 5, 0.15)'
            },
            {
              offset: 1,
              color: 'rgb(153, 5, 5, 0.4)'
            }
          ])
        },
      }
    ]
  };


}


/////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////
// Play tools
function play(){
  startPlaying();
  playButton.style.display="none";
  stopButton.style.display="inline-block";
  lastButton.style.display="none";
  nextButton.style.display="none";
}
function stop(){
  stopPlaying();
  playButton.style.display="inline-block";
  stopButton.style.display="none";
  lastButton.style.display="inline-block";
  nextButton.style.display="inline-block"

}
function updateCurrentTurnDisplay(turn){
  if (currentTurnNumber.innerText===`${turn}`)
  {
    return
  } else{
    currentTurnNumber.innerText=turn;
    // currentTurnStartNumber.innerText=currentFrame;
  }

}
function updateCurrentFrameDisplay(){
  currentFrameNumber.innerText=currentFrame;
}
function jump(){
  currentFrame=parseInt(jumpInput.value);
  drawFrame(frames[currentFrame]);
}
function speed(){
  stopPlaying();
  PLAYING_SPEED=parseFloat(speedInput.value);
  startPlaying();
}
function next(){
  drawFrame(frames[currentFrame]);
  currentFrame++;
}
function last(){
  if (currentFrame>=2){
    currentFrame-=2;
    drawFrame(frames[currentFrame]);
    currentFrame++;
  }
}


