function createMetadata(sample) {

  // assemble the General List of Music panel 
  // display songs # pending showing still

    var panel = d3.select("#chart-metadata");

    d3.json(`/metadata/${sample}`).then(function (data) {
      console.log(data);

    //clear any existing metadata
      panel.html("");
   
    panel.selectAll("h6")
          .data(d3.keys(data))
          .enter()
          .append("h6")
          .text(function (data) {
            return data});
    console.log(data);

  });
}

function buildChart(sample) {
  // Grabd and assigned data in the json for data visual 
  // Consists of all but Song Name
    var sample = d3.select("#selDataset").property("value");
     d3.json(`/samples/${sample}`).then(function (data){
           var entryPosition = data.entryPosition;
           var entryDate = data.entryDate;
           var currentWeekPosition = data.currentWeekPosition;
           var artist = data.artist;
           var sample_values = data.sample_values;
            console.log(data.artist);

    /** Build Chart using the json data
     * Set layout and chart for view 
     * temp view just to view data for now 
     *
    */
       var builtLayout = {
        margin: {t: 2},
        hoverinfo: "text+label+value",

        xaxis: {title: "Charts "}
       };
       var chartData = [{
         x: artist, y: entryDate,
         text: sample_values,
         mode: "markers",
         marker: {
           text: artist,
           size: currentWeekPosition,
           color: entryPosition,
          colorscale: "Greys"
         }}];
         console.log(data)
       Plotly.newPlot("chartView", chartData, builtLayout );

      });
}

function init() {
  // Grab a reference to the dropdown select element
  var selector = d3.select("#selDataset");

  // Use the list of sample names to populate the select options
    d3.json("/names").then(function (samples){
    selector.selectAll("option").data(samples)
    .enter()
    .append("option")
    .text(function (data){return data;})
    .property("value", function (data) {return data;})
    //console.log(samples[5]);
  }).then(function (){
  

  // Use the first sample from the list to build the initial plots
  const viewGenerated = selector.property("value");
    console.log(viewGenerated);
change(viewGenerated)
    })
}

function change(newSelection) {
  // Fetch new data each time a new sample is selected
  buildChart(newSelection);
  createMetadata(newSelection);
}

// Initialize the dashboard
init();