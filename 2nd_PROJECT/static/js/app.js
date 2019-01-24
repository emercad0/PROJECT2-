function buildMetadata(sample) {

  // @TODO:   // assemble the General List of Music panel 
  // display songs # pending showing still`

  var panel = d3.select("#sample-metadata");

  d3.json(`/metadata/${sample}`).then(function (data) {
    console.log(data);

    // Use `.html("") to clear any existing metadata
    panel.html("");


    panel.selectAll("h4")
      .data(Object.entries(data))
      //.data(data)
      .enter()
      .append("h4")
      .text(function (data) {
        return `${data[0]} : ${data[1]}`
        //return  data.artist

      });


  });


}

function buildCharts(positions) {

  // Grab and assigned data in the json for data visual 
  // Consists of all but Song Name
  var positions = d3.select("#selPositions").property("value");

  d3.json(`/positions/${positions}`).then(function (data) {
    //var entryPosition = data.entryPosition;
    //var entryDate = data.entryDate;
    // var weekPosition = data.weekPosition;
    var artist = data.artist;
    var sample_values = data.sample_values;
    var WeekOf = data.WeekOf;
    var songs = data.songs;
    var sampleMeanttWeeks = data.sampleMeanttWeeks;
    var sampleArtist = data.sampleArtist;
    var sampleSongs = data.sampleSongs;
    var sample_smdata = data.sample_smdata;
    var sampleMeanWeeksP = data.sampleMeanWeeksP;
    var topArtist_values = data.topArtist_values;
    var topArtist_artist = data.topArtist_artist;
    var topArtist_pp = data.topArtist_pp;
    var topArtist_wP = data.topArtist_wP;
    var rank = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
    console.log("Sample of 100 " + data.sample_smdata)
    console.log(data.sample_values);


    // @TODO: Build sample data
    var builtLayout = {
      margin: { t: 0 },
      hoverinfo: "text+label+value+percent",
      xaxis: { title: "Charts " }
    };


    var scatterdata = [{
      x: Date(WeekOf), y: sample_values,
      text: songs,
      mode: "lines",
      //  marker: {
      // text: songs,
      //size: weekPosition,
      // color: artist,
      // colorscale: "Greys"
      // }
    }];
    console.log("Artist" + artist)
    //console.log("Current Week" + weekPosition.slice(0, 10))
    console.log("Selection" + sample_values.slice(0, 10) + artist.slice(0, 10))
    Plotly.newPlot("scatterplot", scatterdata, builtLayout);

    // @TODO: 


    var pieLayout = {
      margin: { l: 0.5, r: 10, b: 10, t: 0.5, pad: 5 }
    };


    var pieData = [{
      values: topArtist_values.reverse(),
      //countInArray(sample_values,1),
      //sample_values.reduce((a, b) => a + b, 0)

      labels: topArtist_artist,
      hovertext: topArtist_wP,
      hoverinfo: "text+label+value",
      textinfo: sampleSongs,
      type: "pie",
      marker: {
        color: topArtist_artist,
        colorscale: "Viridis"
      }
    }];


    Plotly.newPlot("pie", pieData, pieLayout);


  });
}

function init() {
  // Grab a reference to the dropdown select element
  var selector = d3.select("#selDataset");
  var selP = d3.select("#selPositions");


  // Use the list of sample names to populate the select options
  d3.json("/names").then(function (samples) {
    selector.selectAll("option").data(samples)
      .enter()
      .append("option")
      .text(function (data) {
        return data;
      })
      .property("value", function (data) {
        return data;
      })

  }).then(function () {


    // Use the first sample from the list to build the initial plots

    const firstSample = selector.property("value");
    console.log(firstSample);

    optionChanged(firstSample)
  })


  d3.json("/listofpositions").then(function (samples) {
    selP.selectAll("option").data(samples)
      .enter()
      .append("option")
      .text(function (data) {
        return data;
      })
      .property("value", function (data) {
        return data;
      })
    console.log(samples[5]);
  }).then(function () {




    const firstSample = selP.property("value");
    console.log(firstSample);

    positionChange(firstSample)
  })

}



function optionChanged(newSample) {
  // Fetch new data each time a new sample is selected

  //buildCharts(newSample);
  buildMetadata(newSample);
}

function positionChange(newSample) {
  // Fetch new data each time a new sample is selected

  buildCharts(newSample);

}




// Initialize the dashboard
init();
