$("document").ready(function(){
    console.log("jfdhjfd")
	var api_data;
        var message = $("#message").val();
	//ajax for API requesst
        $.ajax({
            url: "http://localhost:5000/api/",
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify({"message": message})
        }).done(function(data) {
	console.log(data[0][0]);
	var geoJSON = {
	    "type": "FeatureCollection",
	    "features":[
		{
		    "type":"Feature",
		    "geometry":{
		        "type":"Polygon",
		        "coordinates":data
		    },
		}
	    ]
	}
var path = d3.geo.path();
//Defaults to Projection. You might want to set a different one
var width = 960, height = 600;
//Create the svg to render the polygon inside of
var svg = d3.select("body").append("svg")
    .attr("width", width)
    .attr("height", height);
//Bind the geoJSON the path elements in the svg
//Use the enter selection (new elements) and draw the paths using the geo path generator
svg.selectAll("path")
    .data(geoJSON.features)
 .enter().append("path")
    .attr("d",path)
    .attr("fill");
	 
      //  console.log(data.length);
        });
});
