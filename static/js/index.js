var map;
var circles = [];

$(function() {
      var myOptions = {
          zoom: 14,
          mapTypeId: google.maps.MapTypeId.ROADMAP
      };
      map = new google.maps.Map(document.getElementById("map_canvas"),
                                    myOptions);
      $('#candidate').bind('change', change_details);
      $('#type').bind('change', change_details);
});

function change_details() {
    var candidate_id = $('#candidate').val();
    var type = $('#type').val();
    $.getJSON($SCRIPT_ROOT + '/get_candidate_data', {
                  candidate_id:  candidate_id
              }, function(data) {
                  draw_map(data.viewdata, data.results, type);
              });
    
}

function draw_map(viewdata, results, type) {
    for (i in circles) {
        circles[i].setMap(null);
    }
    circles = [];
    map.setCenter(new google.maps.LatLng(viewdata.centre_lat, viewdata.centre_lon));
    for (i in results) {
        var station = results[i];
        add_heat(station, map, type);
        $("#"+station.id).text(station.votes["total"] + "  (" + station.votes["percentage"] + "%)");
    }
}

function add_heat(result, ma, type) {
    // Construct the circle. 
    var heatOptions = {
        strokeColor: "#FF0000",
        strokeOpacity: 0.8,
        strokeWeight: 2,
        fillColor: "#FF0000",
        fillOpacity: 0.35,
        map: map,
        radius: result.votes[type],
        center: new google.maps.LatLng(result.lat,
                                       result.lon)
    };
    if (type == "percentage") {
        heatOptions.radius = heatOptions.radius * 10;
    }
    circles.push(new google.maps.Circle(heatOptions));
}