var chartDom = document.getElementById("chartl");
var myChart = echarts.init(chartDom);
var option;

var turns = ["0"];
var AScore = [0];
var BScore = [0];
var Delta = [0];

function setChart(mode){
  if (mode==="raw"){
    option = {
      animationDuration: 1000,
      animationDurationUpdate: 200,
      legend: {
        data: ["Team A", "Team B"],
      },
      tooltip: {
        trigger: "axis",
        formatter: "Score : {c}",
      },
      grid: {
        containLabel: true,
      },
      xAxis: {
        type: "value",
        axisLabel: {
          formatter: "{value}",
        },
      },
      yAxis: {
        type: "category",
        axisLine: { onZero: false },
        axisLabel: {
          formatter: "{value}",
        },
        boundaryGap: false,
        data: turns,
      },
      series: [
        {
          name: "Team A",
          type: "line",
          symbolSize: 5,
          symbol: "circle",
          smooth: true,
          lineStyle: {
            shadowColor: "rgba(0,0,0,0.3)",
            shadowBlur: 10,
            shadowOffsetY: 8,
          },
          data: AScore,
        },
        {
          name: "Team B",
          type: "line",
          symbolSize: 5,
          symbol: "circle",
          smooth: true,
          lineStyle: {
            color: "#ff0000",
            shadowColor: "rgba(0,0,0,0.3)",
            shadowBlur: 10,
            shadowOffsetY: 8,
          },
          data: BScore,
        },
      ],
    };
  }
  else if (mode==="difference"){
    option = {
      animationDuration: 1000,
      animationDurationUpdate: 200,
      legend: {
        data: ["Delta"],
      },
      tooltip: {
        trigger: "axis",
        formatter: "Score : {c}",
      },
      grid: {
        containLabel: true,
      },
      xAxis: {
        type: "value",
        axisLine: { onZero: true },
        axisLabel: {
          formatter: "{value}",
        },
      },
      yAxis: {
        type: "category",
        axisLine: { onZero: true },
        axisLabel: {
          formatter: "{value}",
        },
        boundaryGap: false,
        data: turns,
      },
      series: [
        {
          name: "Delta",
          type: "line",
          symbolSize: 5,
          symbol: "circle",
          smooth: true,
          lineStyle: {
            shadowColor: "rgba(0,0,0,0.3)",
            shadowBlur: 10,
            shadowOffsetY: 8,
          },
          data: Delta,
        }
      ],
    };
  }
  myChart.setOption(option);
}

setChart("difference");
option && myChart.setOption(option);

// 随机生成数据，每0.1s插入一组数据到AScore和BScore中
function testDataA() {
  var i = 0;
  var tA = [10,20,30,40,50,60,70,80,90,100];
  var tB = [15,30,35,42,60,75,76,85,100,152];
  var timer = setInterval(function () {
    i++;
    turns.push(i);
    AScore.push(tA[i-1]);
    BScore.push(tB[i-1]);
    myChart.setOption({
      yAxis: {
        data: turns,
      },
      series: [
        {
          name: "Team A",
          data: AScore,
        },
        {
          name: "Team B",
          data: BScore,
        },
      ],
    });
    if (i === 10) {
      clearInterval(timer);
    }
  }, 200);
}

function testDataB() {
  var i = 0;
  var tD = [1,-1,5,-5,1,-5,4,5,1,-5];
  var timer = setInterval(function () {
    i++;
    turns.push(i);
    Delta.push(tD[i-1]);
    myChart.setOption({
      yAxis: {
        data: turns,
      },
      series: [
        {
          name: "Delta",
          data: Delta,
        }
      ],
    });
    if (i === 10) {
      clearInterval(timer);
    }
  }, 200);
}

var chartDom = document.getElementById('chartr');
var myChart = echarts.init(chartDom);
var option;

let base = +new Date(1988, 9, 3);
let oneDay = 24 * 3600 * 1000;
let data = [[base, Math.random() * 300]];
for (let i = 1; i < 20000; i++) {
  let now = new Date((base += oneDay));
  data.push([+now, Math.round((Math.random() - 0.5) * 20 + data[i - 1][1])]);
}
option = {
  animationDuration: 1000,
  animationDurationUpdate: 200,
  legend: {
    data: ["Delta"],
  },
  tooltip: {
    trigger: "axis",
    formatter: "Score : {c}",
  },
  grid: {
    containLabel: true,
  },
  xAxis: {
    type: "value",
    axisLine: { onZero: true },
    axisLabel: {
      formatter: "{value}",
    },
  },
  yAxis: {
    type: "category",
    axisLine: { onZero: true },
    axisLabel: {
      formatter: "{value}",
    },
    boundaryGap: false,
    data: turns,
  },
  series: [
    {
      name: "Delta",
      type: "line",
      symbolSize: 5,
      symbol: "circle",
      smooth: true,
      lineStyle: {
        shadowColor: "rgba(0,0,0,0.3)",
        shadowBlur: 10,
        shadowOffsetY: 8,
      },
      data: Delta,
    }
  ],
};

option && myChart.setOption(option);