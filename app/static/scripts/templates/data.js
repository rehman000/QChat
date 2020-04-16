$("#legend").empty(); /* legend not needed */

$(document).ready(function () {

  /* STATES */
  var state = { 
    /* index of the region you have loaded*/
    regionLoadedIndex: -1,
    /* determines the index of what region you are graphing*/
    regionIndex: 0,
    /* buffer for the datase. date, deaths, cases are the labels*/
    cData: null, 
  }

  /* CONSTANTS (except in the case of setting up these values)*/
  var cnst = { 
    /* url for state data csv file */
    stateUrl: "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv",
    /* url for US data csv file */
    usUrl: "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us.csv",
    /* an array of regions you can select */
    regions: []
  }

  /* checks if data is loaded for the given selection*/
  function isDataLoaded() {
    /* checking if you switched to or from the 'ALL' selection */
    var uSToState = state.regionLoadedIndex == 0 && state.regionIndex !== state.regionLoadedIndex;
    var stateToUS = state.regionLoadedIndex !== 0 &&  state.regionIndex == 0;
    var levelChanged = stateToUS || uSToState;

    /* checking if data store is loaded */
    var cDataLoaded = (state.cData)? true : false;

    return !levelChanged && cDataLoaded;
  }

  /* gets the url for a given selection */
  function selectedUrl() {
    return state.regionIndex == 0 ? cnst.usUrl : cnst.stateUrl;
  }

  function isScreenSmall() {
    return window.innerWidth <= 768;
  }

  function insertTableRow(table, rowData, index, isHeading, beginHeading=false) {
    if(isHeading) {
      beginHeading = true;
    }
    var elemTag = isHeading? '<th/>':'<td/>';
    var startTag = beginHeading? '<th/>':'<td/>';
    var newRow = $('<tr/>').insertAfter( table.find('tr').eq(index) );
    $(rowData).each(function(colIndex) {  
        if(colIndex == 0) {
          newRow.append($(startTag).text(this));
        } else {
          newRow.append($(elemTag).text(this));
        }
    });
    
    return newRow;
  }

  function appendTableRow(table, rowData, isHeading, beginHeading=false) {
    //table.find('tr:last').index() also works
    return insertTableRow( table, rowData, -1, isHeading, beginHeading);
  }

  /* summerizes data into a table */
  function dataTable(data) {
    var formatTime = d3.timeFormat("%m/%d/%Y");

    var latestInfo = data.reduce(function(currentMax, next){
      return currentMax.date < next.date? next : currentMax
    }, data[0]);
    var previousInfo = data.reduce(function(currentMax, next){
      if(+next.date === +latestInfo.date) {
        return currentMax;
      } else if(+currentMax.date === +latestInfo.date) {
        return next;
      } else {
        return  currentMax.date < next.date? next : currentMax;
      }
    }, data[0]);
    var sign = function(n) {
      if (n>0) return '+';
      else if(n<0) return '-';
      else return '';
    }
    var latestDate = formatTime(latestInfo.date)
    var prevDate = formatTime(previousInfo.date);
    /*percentage of cases changed since prevDate*/
    var casesChange = Math.round(100*(latestInfo.cases - previousInfo.cases)/previousInfo.cases);
    /* percentage of deaths change since prevDate */
    var deathsChange = Math.round(100*(latestInfo.deaths - previousInfo.deaths)/previousInfo.deaths); 
    var deathRate = Math.round(100*latestInfo.deaths/latestInfo.cases);
    var tableHeadings = ['Latest reported Date', 'Latest Total Cases', 'Cases changed since ' + prevDate, 'Latest Total Deaths', 'Deaths increased since ' + prevDate, 'Death Rate'];
    var tableInfo = [
      latestDate, 
      latestInfo.cases.toLocaleString(), 
      sign(casesChange) + ' ' + Math.abs(casesChange).toLocaleString() + '%', 
      latestInfo.deaths.toLocaleString(), 
      deathsChange.toLocaleString() + '%',
      deathRate + '%'
    ];
    covid19TableLarge = $("#covid19Table");
    covid19TableLarge.empty();
    covid19TableLarge.html("<tr></tr>");
    if(isScreenSmall()) {
      covid19TableSmall = $("#covid19Table");
      covid19TableSmall.empty();
      covid19TableSmall.html("<tr></tr>");
      for(var i = 0; i < tableHeadings.length; i++) {
        appendTableRow(covid19TableSmall, [tableHeadings[i], tableInfo[i]], false, true);
      }
    } else {
      insertTableRow(covid19TableLarge, tableHeadings, 0, true);
      appendTableRow(covid19TableLarge, tableInfo, false);
    }
  }

  function graphData(data, margin, width, height, x, y, svg, valueline, valueline2) {
    /* parse the date / time */
    var parseTime = d3.timeParse("%Y-%m-%d");
    console.log(data)

    /* filter the data */
    if(state.regionIndex != 0) {
      data = data.filter(function(d){
        return d.state === cnst.regions[state.regionIndex];
      });
    }

    data = data.map(function(d){
      return {
        date: parseTime(d.date),
        deaths: +d.deaths,
        cases: +d.cases
      }
    });

    dataTable(data);

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

    svg.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height + ")")
      .call(d3.axisBottom(x)
              .ticks(5));

    /* Add the Y Axis */
    svg.append("g")
      .attr("class", "y axis")
      .call(d3.axisLeft(y));

    /* format X axis texts */
    svg.select(".x.axis")
      .selectAll("text")
      .attr("transform"," translate(-25,35) rotate(-65)") /* To rotate the texts on x axis. Translate y position a little bit to prevent overlapping on axis line. */
      .style("font-size","18px") 
      .style("font-weight", "560");

    /* format Y axis texts */
    svg.select(".y.axis")
    .selectAll("text")
    .attr("transform"," translate(-7,0)") 
    .style("font-size", "17px")
    .style("font-weight", "560");

    /* text label for the x axis */
    svg.append("text")             
      .attr("transform", "translate(" + (width/2) + " ," + (height + margin.top + 90) + ")")
      .style("text-anchor", "middle")
      .style("font-size", "25px")
      .style("font-weight", "bold")
      .text("Date");

    /* text label for the y axis */
    svg.append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", 0 - margin.left)
      .attr("x",0 - (height / 2))
      .attr("dy", "1em")
      .style("text-anchor", "middle")
      .style("font-size", "25px")
      .style("font-weight", "bold")
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
    displayLoad(); /* graph is being loaded */
    $("#chart").empty();
    var margin = {top: 20, right: 20, bottom: 120, left: 130};
    var width = Math.max(375, window.innerWidth*0.40) - margin.left - margin.right;
    var height = Math.max(375, window.innerHeight*0.55) - margin.top - margin.bottom;

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
    
    svg.append("circle")
      .attr("cx",200*widthScale).attr("cy",130*heightScale)
      .attr("r", 6).style("fill", "#69b3a2");

    svg.append("circle")
      .attr("cx",200*widthScale).attr("cy",130*heightScale+30)
      .attr("r", 6).style("fill", "#404080");

    svg.append("text")
      .attr("x", 200*widthScale + 20).attr("y", 130*heightScale).text("Total Cases")
      .style("font-size", "18px").attr("alignment-baseline","middle").style("font-weight", "bold");

    svg.append("text")
      .attr("x", 200*widthScale + 20).attr("y", 130*heightScale+30).text("Total Deaths")
      .style("font-size", "18x").attr("alignment-baseline","middle").style("font-weight", "bold");
    

    if (isDataLoaded()) {
      console.log(1);
      graphData(state.cData, margin, width, height, x, y, svg, valueline, valueline2);
      state.regionLoadedIndex = state.regionIndex;
      displayResult();
    } else {
      d3.csv(selectedUrl(), function(error, data) {
        console.log(2);
        console.log(selectedUrl())
        if (error) {
          displayLoadError();
          throw error;
        } 
        state.cData = data;
        graphData(data, margin, width, height, x, y, svg, valueline, valueline2);
        state.regionLoadedIndex = state.regionIndex;
        displayResult();
      });
    }
  }

  /* displays loading screen */
  function displayLoad() {
    $("#loadError").hide();
    $("#loadData").show(); 
    $(".dataDisplay").hide();
  }

  /* displays result */
  function displayResult() {
    $("#loadError").hide();
    $("#loadData").hide(); 
    $(".dataDisplay").show();
  }

  /* displayy error */
  function displayLoadError() {
    $("#loadError").show();
    $(".loading").hide();
    $(".dataDisplay").hide();
  }

  /* set up regions state */
  function setupRegions(){
    /* csv string queried from a url */
    var csvString = $.ajax({ 
      type: "GET",
      async: false,
      url: cnst.stateUrl,
    }).responseText;

    /* csv string is formatted */
    var c19Table = new dataParse.CSVTable(csvString);

    /* save all regions to the regions state */
    var regionsSet = new Set(c19Table.data.map(function(row){
      return row[1];
    }));
    var regions = Array.from(regionsSet);
    regions.sort();
    cnst.regions = ['All'].concat(regions);

    /* gets the default region index to choose the region to graph*/
    state.regionIndex = 0;
  };

  /* sets up the selector for regions */
  function setupSelectRegion() {
    setupRegions();
    $("#selectRegion").empty();
    for(var i = 0; i < cnst.regions.length; i++) { 
      $("#selectRegion").append(new Option(cnst.regions[i], i));
    }
    $("#selectRegion").val(state.regionIndex);
    var chosenRegion = cnst.regions[state.regionIndex];
    var chosenRegion = chosenRegion === "All"? "US (All states)":chosenRegion;
    $("#regionHeading").html(chosenRegion);
  }

  /* every time a region is selected the state must update and the data be graphed again */
  $('#decideRegion').click(function(){
    var index = $( "#selectRegion option:selected" ).val();
    if(index < 0) {
      alert("something went wrong")
      return;
    }
    state.regionIndex = index;
    graph()
    $("#regionHeading").html(cnst.regions[state.regionIndex]);
  });

  $("#loadError").find("button").click(function(){
    graph();
  });

  $(window).resize(function() {
    /* graph is rerendered to ensure responsiveness */
    try {
      graph();
    } catch (err) {
      console.log(err)
      displayLoadError();
    }
  });

  /* indicates things are being set up */
  displayLoad();

  /* set up default selections and their assosiated states*/
  setupSelectRegion();
  $('#selectLevel').val(state.regionIndex);
  
  graph();
});
