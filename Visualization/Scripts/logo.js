container=document.getElementById('container')

function generate(){
    for(i=1;i<=25;i++){
        for (j=1;j<=7;j++){
            block=document.createElement('div');
            block.style.gridColumn=`${i}`;
            block.style.gridRow=`${j}`;
            if (template[j-1][i-1]===1){
                block.classList.add('show')
                block.style.backgroundColor=colorArray[4+Math.floor(Math.random()*2)]

            } else if (template[j-1][i-1]===0){
                block.classList.add('back');
                // block.style.backgroundColor=colorAnother[Math.floor(Math.random()*2)]
            }
            container.appendChild(block);
        }
    }
}
const colorAnother=['rgb(5, 5, 153)','rgb(153, 5, 5)']
const colorArray=["rgb(13, 211, 82)","rgb(22, 218, 224)","rgb(224, 134, 60)","rgb(243, 121, 137)","rgb(244, 67, 54)","rgb(255, 193, 7)","rgb(0, 188, 212)","rgb(103, 58, 183)","rgb(233, 30, 99)","rgb(255, 152, 0)","rgb(3, 169, 244)"];
const template=[
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,1,1,1,0,1,1,0,0,0,1,0,0,0,1,1,0,1,1,1,0,1,1,0,0],
    [0,1,0,0,0,1,0,1,0,1,0,1,0,1,0,0,0,1,0,0,0,1,0,1,0],
    [0,1,1,1,0,1,1,0,0,1,1,1,0,1,1,1,0,1,1,1,0,1,1,0,0],
    [0,1,0,0,0,1,0,1,0,1,0,1,0,0,0,1,0,1,0,0,0,1,0,1,0],
    [0,1,1,1,0,1,0,1,0,1,0,1,0,1,1,0,0,1,1,1,0,1,0,1,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
]

generate()



