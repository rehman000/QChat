$(document).ready(function () {
  dataUrls = {
    stateLevelUrl:
      "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv" /*url for state level data*/,
    countyLevelUrl:
      "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv" /*url for countylevel data*/,
  };

  function gatherCsv(csvUrl) {
    /* retrieves csv from a URL */ $.ajax({
      url: csvUrl,
      success: function (result) {
        /* result is a csv string */
        var csvData = csvToObject(
          result
        ); /* formats csv string into an object */
        console.log(csvData);
        /*we may use this data for visualization*/
      },
    });
  }

  console.log("retrieving url from state level data");
  gatherCsv(dataUrls.stateLevelUrl);

  console.log("retrieving url from county level data");
  gatherCsv(dataUrls.countyLevelUrl);
});
