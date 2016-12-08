/* Define base layers */
var cycleURL='http://{s}.tile.thunderforest.com/cycle/{z}/{x}/{y}.png';
var cycleAttrib='Map data © OpenStreetMap contributors';
var opencyclemap = new L.TileLayer(cycleURL, {attribution: cycleAttrib}); 

var osmUrl='http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
var osmAttrib='Map data © openstreetmap contributors';
var osm = new L.TileLayer(osmUrl, {attribution: osmAttrib}); 

/* create new layer group */
var layer_sell = new L.LayerGroup();
var array_markers = new Array();

/* create custom marker which will represent apartments in layer 'layer_sell' */
customMarker = L.Marker.extend({
   options: { 
      title: 'Home Property',
   }
});

/* define function which adds markers from array to layer group */
function AddPointsToLayer() {
    for (var i=0; i<array_markers.length; i++) {
        array_markers[i].addTo(layer_sell);
    }
} 

/* Get all apartments from DB and add them to layer:_apartments */
$.ajax({
	url: '/map/get-properties/',
	type: 'GET',
	success: function(response) {
        $.each(eval(response), function(key, val) {	  
        	//fields in JSON that was returned      	
        	var fields = val.fields; 

        	// parse point field to get values of latitude and longitued
        	var regExp = /\(([^)]+)\)/;
			var matches = regExp.exec(fields.geom);
			var point = matches[1];
			var lon=point.split(' ')[0];
			var lat=point.split(' ')[1];

        	//function which creates and adds new markers based on filtered values
        	marker = new customMarker([lat, lon], {
			    title: fields.id,
			    opacity: 1.0  
			}); 
			marker.bindPopup("<strong>Name: </strong>" + fields.id + "<br><strong>House Type: </strong>"
				+ fields.house_type + "<br><strong>Price: </strong>"+ fields.price + "<br><strong>Beds: </strong>"
				+ fields.beds + "<br><strong>Baths: </strong>"+ fields.baths);
        	marker.addTo(map);
        	array_markers.push(marker);
        });

        // add markers to layer and add it to map
        AddPointsToLayer();
    }
});

/* create map object */
var map = L.map('map', {
	center: [-1.2921, 36.8219],
	zoom: 7,
	fullscreenControl: true,
	fullscreenControlOptions: {
		position: 'topleft'
	},
	layers: [osm, layer_sell]
});

var baseLayers = {
	"OpenCycleMap": opencyclemap,
	"OpenStreetMap": osm
};

var overlays = {
	"Home Property": layer_sell
};

L.control.layers(baseLayers, overlays).addTo(map);


/* S I D E B A R   F I L T E R */
var sidebar = L.control.sidebar('sidebar', {
    position: 'left'
});
map.addControl(sidebar);

setTimeout(function () {
    sidebar.show();
}, 300);

$('#filter_control').click(function() {
    sidebar.show();
});


$(document).ready(function() {  
   // setting default min and max value for slider - price attribute
   $("#slider_price").data("value", "(0,50000000)");

   $("#slider_price").slider(
   {
    range: true,
    step: 50,
    min: 0,
    max: 50000000,
    values: [0, 50000000],
    slide: function( event, ui ) {
      $('#lbl').html(ui.values[0] + " $ - " + ui.values[1]+" $");
      var selected_price = '('+ui.values[0]+','+ui.values[1]+')';
      $("#slider_price").data("value",selected_price );
      
      getResult();
    }
  });
});

/* getResult function is called every time when user filters map objects using sidebar filter */
function getResult() {
	// fetch value of all filter fields
	var selected_sale_rent = $("#select_sale_rent").val();
	var selected_price = $("#slider_price").data("value");
	var selected_house_type = $("#select_house_type").val();
	var selected_beds = $("#select_beds").val();
	var selected_baths = $("#select_baths").val();

	// get fields where value is not 'all' so that you later filter only those fields
	var fields = new Array();

	if (selected_sale_rent !== 'all') {
		fields.push("sale_rent");
	}

	if (selected_house_type !== 'all') {
		fields.push("house_type");
	}
	if (selected_beds !== 'all') {
		fields.push("beds");
	}
	if (selected_baths !== 'all') {
		fields.push("baths");
	}

	// price field doesn't have value 'all' so it will be filtered in any case
	fields.push("price");

	/* ajax call to get all apartments with defined filter values */
	$.ajax({
		url: '/map/properties/filter/',
		type: 'GET',
		data: "sale_rent=" + selected_sale_rent + "&price=" + selected_price + "&house_type=" 
		+ selected_house_type + "&beds=" + selected_beds + "&baths=" + selected_baths +"&fields=" + fields,
		success: function(response) {
			// first delete all markers from layer apartments
			array_markers.length=0;
	        layer_sell.clearLayers();

	        $.each(eval(response), function(key, val) {	  
	        	//fields in JSON that was returned      	
	        	var fields = val.fields; 

	        	// parse point field to get values of latitude and longitued
	        	var regExp = /\(([^)]+)\)/;
				var matches = regExp.exec(fields.geom);
				var point = matches[1];
				var lon=point.split(' ')[0];
				var lat=point.split(' ')[1];

	        	//function which creates and adds new markers based on filtered values
	        	marker = new customMarker([lat, lon], {
				    title: fields.name,
				    opacity: 1.0  
				}); 
	        	marker.addTo(map);
	        	marker.bindPopup("<strong>Name: </strong>" + fields.id + "<br><strong>House Type: </strong>"
				+ fields.house_type + "<br><strong>Price: </strong>"+ fields.price + "<br><strong>Beds: </strong>"
				+ fields.beds + "<br><strong>Baths: </strong>"+ fields.baths);
	        	array_markers.push(marker);
	        });

	        // add markers to layer and add it to map
	        AddPointsToLayer();
	    }
	});
}



