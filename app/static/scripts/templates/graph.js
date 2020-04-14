$("#legend").empty(); /* legend not needed */

$(document).ready(function () {

  /* STATES */
  var state = { 
    /* determines the index of what region you are graphing*/
    regionIndex: 0,
    /* buffer for the dataset*/
    cData: null,
  }

  /* CONSTANTS (except in the case of setting up these values)*/
  var cnst = { 
    /* url for a csv file */
    dataUrl: "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv",
    /* an array of regions you can select */
    regions: []
  }

  function isDataLoaded() {
    return (state.cData)? true : false;
  }

  function graphData(data, margin, width, height, x, y, svg, valueline, valueline2) {
    /* parse the date / time */
    var parseTime = d3.timeParse("%Y-%m-%d");

    /* filter the data */
    data = data.filter(function(d){
      return d.state === cnst.regions[state.regionIndex];
    })
    .map(function(d){
      return {
        date: parseTime(d.date),
        deaths: +d.deaths,
        cases: +d.cases
      }
    });

    /* Scale the range of the data */
    x.domain(d3.extent(data, function(d) { return d.date; }));
    y.domain([0, d3.max(data, function(d) {
      return Math.max(d.deaths, d.cases); 
    })]);

    /* Add the valueline path. */
    svg.append("path")
      .data([data])
      .attr("class", "line")
      .style("stroke", "#69b3a2")
      .attr("d", valueline);

    /* Add the valueline2 path. */
    svg.append("path")
      .data([data])
      .attr("class", "line")
      .style("stroke", "#404080")
      .attr("d", valueline2);

    /* Add the X Axis */
    // svg.append("g")
    //   .attr("transform", "translate(0," + height + ")")
    //   .call(d3.axisBottom(x));

    svg.append("g")
      .attr("class", "axis")
      .attr("transform", "translate(0," + height + ")")
      .call(d3.axisBottom(x)
              .ticks(5));

    /* Add the Y Axis */
    svg.append("g")
      .call(d3.axisLeft(y));

    /* text label for the x axis */
    svg.append("text")             
      .attr("transform", "translate(" + (width/2) + " ," + (height + margin.top + 40) + ")")
      .style("text-anchor", "middle")
      .text("Date");

    /* text label for the y axis */
    svg.append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", 0 - margin.left)
      .attr("x",0 - (height / 2))
      .attr("dy", "1em")
      .style("text-anchor", "middle")
      .text("Number of People");  

    /* adding grid lines */

    function make_x_gridlines() {
      return d3.axisBottom(x)
        .ticks(5)
    }
    function make_y_gridlines() {
      return d3.axisLeft(y)
        .ticks(5)
    }

    svg.append("g")
      .attr("class","grid")
      .attr("transform","translate(0," + height + ")")
      .style("stroke-dasharray",("3,3"))
      .call(make_x_gridlines()
            .tickSize(-height)
            .tickFormat("")
          );
    svg.append("g")
      .attr("class","grid")
      .style("stroke-dasharray",("3,3"))
      .call(
        make_y_gridlines()
          .tickSize(-width)
          .tickFormat("")
      );
  }

  /* graphing timeline of covid-19 for a specific region using a line graph*/
  function graph() {

    $("#chart").empty();

    /* set the dimensions and margins of the graph */
    // var margin = {top: 20, right: 20, bottom: 80, left: 70},
    // width = 960 - margin.left - margin.right,
    // height = 500 - margin.top - margin.bottom;
    var margin = {top: 20, right: 20, bottom: 80, left: 90},
    width = Math.max(375, window.innerWidth/1.3) - margin.left - margin.right,
    height = Math.max(375, window.innerHeight/1.3) - margin.top - margin.bottom;

    var widthScale = width / 1920;
    var heightScale = height / 1080;

    /* set the ranges */
    var x = d3.scaleTime().range([0, width]);
    var y = d3.scaleLinear().range([height, 0]);

    /* define the 1st line */
    var valueline = d3.line()
      .x(function(d) { return x(d.date); })
      .y(function(d) { return y(d.cases); });

    /* define the 2nd line */
    var valueline2 = d3.line()
      .x(function(d) { return x(d.date); })
      .y(function(d) { return y(d.deaths); });

    var svg = d3.select("#chart")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
      .append("g")
      .attr("transform",
            "translate(" + margin.left + "," + margin.top + ")");
    
    svg.append("circle").attr("cx",200*widthScale).attr("cy",130*heightScale).attr("r", 6).style("fill", "#69b3a2");
    svg.append("circle").attr("cx",200*widthScale).attr("cy",130*heightScale+30).attr("r", 6).style("fill", "#404080");
    svg.append("text").attr("x", 200*widthScale + 20).attr("y", 130*heightScale).text("Cases").style("font-size", "15px").attr("alignment-baseline","middle");
    svg.append("text").attr("x", 200*widthScale + 20).attr("y", 130*heightScale+30).text("Deaths").style("font-size", "15x").attr("alignment-baseline","middle");
    

    if (isDataLoaded()) {
      graphData(state.cData, margin, width, height, x, y, svg, valueline, valueline2);
    } else {
      d3.csv(cnst.dataUrl, function(error, data) {
        if (error) {throw error;} 
        state.cData = data;
        graphData(data, margin, width, height, x, y, svg, valueline, valueline2);
      });
    }
  }

  /* displays loading screen */
  function displayLoad() {
    $("#loadData").show(); 
    $(".dataDisplay").hide();
  }

  /* no longer displayes loading screen*/
  function noDisplayLoad() {
    $("#loadData").hide(); 
    $(".dataDisplay").show();
  }

  /* set up regions state */
  function setupRegions(){
    /* csv string queried from a url */
    var csvString = $.ajax({ 
      type: "GET",
      async: false,
      url: cnst.dataUrl,
    }).responseText;

    /* csv string is formatted */
    var c19Table = new dataParse.CSVTable(csvString);

    /* save all regions to the regions state */
    var regionsSet = new Set(c19Table.data.map(function(row){
      return row[1];
    }));
    var regions = Array.from(regionsSet);
    regions.sort();
    cnst.regions = regions;

    /* gets the default region index to choose the region to graph*/
    state.regionIndex = cnst.regions.indexOf("New York");
    if (state.regionIndex < 0) {
      state.regionIndex = 0;
    }
  };

  /* sets up the selector for regions */
  function setupSelectRegion() {
    setupRegions();
    $("#selectRegion").empty();
    for(var i = 0; i < cnst.regions.length; i++) { 
      $("#selectRegion").append(new Option(cnst.regions[i], i));
    }
    $("#selectRegion").val(state.regionIndex);
    $("#c19Data").find("h2").html(cnst.regions[state.regionIndex]);
  }

  /* every time a region is selected the state must update and the data be graphed again */
  $('#decideRegion').click(function(){
    var index = $( "#selectRegion option:selected" ).val();
    if(index < 0) {
      alert("something went wrong")
      return;
    }
    state.regionIndex = index;
    displayLoad();
    graph();
    noDisplayLoad();
    $("#c19Data").find("h2").html(cnst.regions[state.regionIndex]);
  });

  $(window).resize(function() {
    /* graph is recreated to ensure responsiveness */
    graph();
  });

  /* indicates things are being set up */
  displayLoad();

  /* set up default selections and their assosiated states*/
  setupSelectRegion();
  $('#selectLevel').val(state.regionIndex);
  
  /* default graph is given */
  graph();

  /* everything is set up so loading stops */
  noDisplayLoad();
});
