var map;
var circles = [];
var colours = ["#FF0000", "#00FF00"];

$(function() {
      var myOptions = {
          zoom: 14,
          mapTypeId: google.maps.MapTypeId.ROADMAP
      };
      map = new google.maps.Map(document.getElementById("map_canvas"),
                                    myOptions);
      $('#candidate_1').bind('change', change_details);
      $('#candidate_2').bind('change', change_details);
      $('#preference_1').bind('change', change_details);
      $('#preference_2').bind('change', change_details);
      $('#type').bind('change', change_details);
});

function change_details() {
    var type = $('#type').val();
    for (i in circles) {
        circles[i].setMap(null);
    }
    circles = [];
    $.getJSON($SCRIPT_ROOT + '/get_candidate_data', {
                  candidate_id:  $('#candidate_1').val(),
                  preference: $('#preference_1').val()
              }, function(data) {
                  update_candidate(0, data.viewdata, data.results, type);
              });
    $.getJSON($SCRIPT_ROOT + '/get_candidate_data', {
                  candidate_id:  $('#candidate_2').val(),
                  preference: $('#preference_2').val()
              }, function(data) {
                  update_candidate(1, data.viewdata, data.results, type);
              });
    
}

function update_candidate(candidate, viewdata, results, type) {
    map.setCenter(new google.maps.LatLng(viewdata.centre_lat, viewdata.centre_lon));
    for (i in results) {
        var station = results[i];
        add_heat(candidate, station, map, type);
        $("#"+candidate+station.id).text(station.votes["total"] + "  (" + station.votes["percentage"] + "%)");
        $("#"+candidate+station.id).css("background-color", colours[candidate]);
    }
}

function add_heat(colour_index, result, ma, type) {
    // Construct the circle. 
    var heatOptions = {
        strokeColor: colours[colour_index],
        strokeOpacity: 0.8,
        strokeWeight: 2,
        fillColor: colours[colour_index],
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