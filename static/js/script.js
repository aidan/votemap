$(function() {
      $.getJSON($SCRIPT_ROOT + '/get_candidate_data', {
                  candidate_id:  candidate_id
              }, function(data) {
                  draw_map(data.viewdata, data.results);
              });
      
});

function draw_map(viewdata, results) {
    var myOptions = {
        center: new google.maps.LatLng(viewdata.centre_lat, viewdata.centre_lon),
        zoom: 14,
        mapTypeId: google.maps.MapTypeId.ROADMAP
    };
    var map = new google.maps.Map(document.getElementById("map_canvas"),
                                  myOptions);
    for (i in results) {
        add_heat(results[i], map);
    }
}

function add_heat(result, map) {
    // Construct the circle. 
    var populationOptions = {
      strokeColor: "#FF0000",
      strokeOpacity: 0.8,
      strokeWeight: 2,
      fillColor: "#FF0000",
      fillOpacity: 0.35,
      map: map,
      center: new google.maps.LatLng(result.lat,
                                     result.lon),
      radius: result.total
    };
    cityCircle = new google.maps.Circle(populationOptions);
}