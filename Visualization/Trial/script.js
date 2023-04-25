const data = [
    { frame: 1, team1: 10, team2: 5 },
    { frame: 2, team1: 15, team2: 7 },
    { frame: 3, team1: 22, team2: 12 },
    // ... 其他帧数据
  ];
  
  let mode = "score"; // 初始模式为'score'
  
  const margin = { top: 20, right: 20, bottom: 30, left: 50 };
  const width = 600 - margin.left - margin.right;
  const height = 300 - margin.top - margin.bottom;
  
  const x = d3.scaleLinear().domain([1, data.length]).range([0, width]);
  const y = d3.scaleLinear().domain([0, d3.max(data, (d) => Math.max(d.team1, d.team2))]).range([height, 0]);
  
  const line = d3
    .line()
    .x((d) => x(d.frame))
    .y((d) => y(d.value));
  
  const svg = d3
    .select("#chart")
    .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", `translate(${margin.left},${margin.top})`);
  
  svg.append("g").attr("transform", `translate(0,${height})`).call(d3.axisBottom(x));
  svg.append("g").call(d3.axisLeft(y));
  
  const team1Line = svg.append("path").attr("stroke", "red").attr("fill", "none");
  const team2Line = svg.append("path").attr("stroke", "blue").attr("fill", "none");
  
  function updateChart() {
    const dataToDisplay = data.map((d) => {
      if (mode === "score") {
        return [{ frame: d.frame, value: d.team1 }, { frame: d.frame, value: d.team2 }];
      } else {
        return [{ frame: d.frame, value: d.team1 - d.team2 }];
      }
    });
  
    team1Line.datum(dataToDisplay.map((d) => d[0])).attr("d", line);
    team2Line.datum(mode === "score" ? dataToDisplay.map((d) => d[1]) : []).attr("d", line);

        // ...之前的代码
      
        team1Line
          .datum(dataToDisplay.map((d) => d[0]))
          .transition()
          .duration(750)
          .attr("d", line);
        team2Line
          .datum(mode === "score" ? dataToDisplay.map((d) => d[1]) : [])
          .transition()
          .duration(750)
          .attr("d", line);
      
  }
  
  const legend = svg.append("g").attr("transform", `translate(${width - 100}, 10)`);

  legend
    .append("rect")
    .attr("width", 20)
    .attr("height", 2)
    .attr("fill", "red");
  
  legend
    .append("rect")
    .attr("x", 60)
    .attr("width", 20)
    .attr("height", 2)
    .attr("fill", "blue");
  
  legend
    .append("text")
    .attr("x", 24)
    .attr("y", 1)
    .attr("dy", "0.32em")
    .text("队伍1");
  
  legend
    .append("text")
    .attr("x", 84)
    .attr("y", 1)
    .attr("dy", "0.32em")
    .text("队伍2");
  


  updateChart();
  
  document.getElementById("toggleMode").addEventListener("click", () => {
    mode = mode === "score" ? "difference" : "score";
    updateChart();
  });
  

  const tooltip = d3.select("#tooltip");

const bisectFrame = d3.bisector((d) => d.frame).left;

function mousemove(event) {
  const x0 = x.invert(d3.pointer(event)[0]);
  const i = bisectFrame(data, x0, 1);
  const d = data[i];

  tooltip
    .style("display", "inline")
    .style("left", `${event.pageX + 10}px`)
    .style("top", `${event.pageY + 10}px`)
    .html(`帧：${d.frame}<br>队伍1：${d.team1}<br>队伍2：${d.team2}`);
}

svg
  .append("rect")
  .attr("class", "overlay")
  .attr("width", width)
  .attr("height", height)
  .attr("opacity", 0)
  .on("mousemove", mousemove)
  .on("mouseout", () => tooltip.style("display", "none"));

