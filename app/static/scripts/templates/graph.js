$(document).ready(function () {

  /* PURE FUNCTIONS BELONG HERE */

  /*The data used follow this format: date, state/county, fips, cases, deaths */

  /*retrieves csv data from a URL issues a callback containing a CSVTable*/
  function getC19Data(csvUrl) { 
    /* retrives csv string from a synchronous ajax call */
    var csvString = $.ajax({ 
      type: "GET",
      async: false,
      url: csvUrl,
    }).responseText;

    /* csv string is parsed and returned */
    return new dataParse.CSVTable(csvString);
  }

  /* data from a csv url and returns an object */
  function Covid19Data(csvUrl) { 
    var c19Table = getC19Data(csvUrl);
    var locationsSet = new Set(c19Table.data.map(function(row){
      return row[1];
    }));

    /* retrieves dates */
    var dates = c19Table.data 
      .map(function(row){
        return row[0];
      })
      .filter(function(value, index, self) {
        return self.indexOf(value) === index;
      })
      .map(function(dateString) {
        return new Date(dateString);
      });

    dates.sort(function(a, b) {
      if (a < b) return -1;
      if (a > b) return 1;
      else return 0;
    });

    /*sets the location asrray*/
    this.locations = Array.from(locationsSet); 

    /* sets the dates array */
    this.dates = dates; 

    /* sets the covid19Table */
    this.data = c19Table.data.map(function(row){
      row[0] = new Date(row[0]);
      return row; 
    }); 
  }

  /* represents the data level (i.e. state, county, eytc)*/
  function DataLevel(name, url) { 
    this.name = name;
    this.url = url;
    this.c19Data = new Covid19Data(url); 
  }

  /* STATES */
  var state = { 
    /* determines the index of what data level you are using*/
    dataLevelIndex: 0,
    regionIndex: 0,
    regions: ["all"] 
  }

  /* CONSTANTS */
  var cnst = { 
    /* data is loaded for each level */
    dataLevels : [ 
      new DataLevel("state", "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv"),
      new DataLevel("county", "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv")
    ],
  }

  /* graphing for for all regions for the latest date using a bar graph*/
  function graphAllGraph() {
    console.log("beginning to graph for all regions for the latest date")
  }

  /* graphing timeline for a specific region using a line graph*/
  function graphRegionGraph() {
    console.log("beginning to graph for all regions for the latest date")
  }

  /* all graphing will occure here */
  function graph() {
    if(state.regionIndex == 0) {
      graphAllGraph();
    } else {
      graphRegionGraph();
    }
  }

  function setupSelectRegion() {
    var locations = cnst.dataLevels[state.dataLevelIndex].c19Data.locations;
    locations.sort()
    var regions = ["all"].concat(locations);
    state.regions = regions;
    state.regionIndex = 0;
    $("#regionDatalist").empty();
    for(var i = 0; i < regions.length; i++) { 
      $("#regionDatalist").append(new Option(regions[i], regions[i]));
    }
    $("#regionDatalist").val(regions[state.regionIndex]);
  }

  /* data should already be loaded */
  $("#loadData").hide(); 
  $(".covidData").show();
  $("#dataSelection").show(); 

  /* sets a data level option */
  for(var i = 0; i < cnst.dataLevels.length; i++) { 
    $('#selectLevel').append(new Option(cnst.dataLevels[i].name, i))
  }

  /* every time a selection is made, the data must then be graphed and the state is updated*/
  $('#selectLevel').change(function(){
    var index = $(this).children("option:selected").val();
    state.dataLevelIndex = index;

    /* since the level has changed the region selector must update as well*/
    setupSelectRegion(); 
    
    /* graph must be updated as well */
    graph();

    var dataLevel = cnst.dataLevels[index];
    console.log(dataLevel);
  });

  /* every time a region is selected the state must update and the data be graphed again */
  $('#decideRegion').click(function(){
    var region = $("#searchRegion").val();
    console.log(region)
    var index = state.regions.indexOf(region);
    if(index < 0) {
      return;
    }
    state.regionIndex = index;
    graph();

    console.log(cnst.dataLevels[state.dataLevelIndex]);
    var data = cnst.dataLevels[state.dataLevelIndex].c19Data.data
      .filter(function(row) {
        return state.regions[index] === row[1];
      });
    console.log(data)
  });

  /* set up default selections */
  setupSelectRegion();
  $('#selectLevel').val(state.regionIndex);
  /* default graph is given */
  graph();

  console.log(cnst.dataLevels[state.dataLevelIndex]);
});
