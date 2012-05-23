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
      $('#ward').bind('change', change_ward);
      $('#candidate_1').bind('change', change_candidates);
      $('#candidate_2').bind('change', change_candidates);
      $('#party_1').bind('change', change_candidates);
      $('#party_2').bind('change', change_candidates);
      $('#preference_1').bind('change', change_candidates);
      $('#preference_2').bind('change', change_candidates);
      $('#type').bind('change', change_candidates);
      change_ward();
});

function change_ward() {
    $.getJSON($SCRIPT_ROOT + '/get_ward_data', {
                  ward: $('#ward').val()
              }, function (data) {
                  update_ward(data);
              });
}

function update_ward(data) {
    set_candidates("#candidate_1", data.candidates, data.parties);
    set_candidates("#candidate_2", data.candidates, data.parties);
    set_preferences("#preference_1", data.candidates.length);
    set_preferences("#preference_2", data.candidates.length);
    set_polling_stations(data.polling_stations);
    change_candidates();
}

function set_parties(options, parties) {
    $(options).empty();
    $(options).append(new Option("Pick party"));
    for (i in parties) {
        $(options).append(new Option(parties[i]));
    }
}

function set_candidates(options, candidates, parties) {
    $(options).empty();
    $(options).append(new Option("Pick party or candidate"));
    for (i in parties) {
         $(options).append(new Option(parties[i]));
    }
    for (i in candidates) {
        var candidate = candidates[i];
        $(options).append(new Option(candidate.name + " ("+candidate.party+")", candidate.id));
    }
}

function set_polling_stations(polling_stations) {
    $('#stations').empty();
    for (i in polling_stations) {
        $('#stations').append("<div class='row'><div class='span4'>"+polling_stations[i].name+"</div><div class='span4' id='0"+polling_stations[i].id+"'></div><div class='span4' id='1"+polling_stations[i].id+"'></div></div>");
    }
}

function set_preferences(name, size) {
    $(name).empty();
    for (i = 1; i <= size; i++) {
        $(name).append(new Option(i, i - 1));
    }
}

function change_candidates() {
    var type = $('#type').val();
    for (i in circles) {
        circles[i].setMap(null);
    }
    circles = [];
    $.getJSON($SCRIPT_ROOT + '/get_candidate_data', {
                  candidate_id:  $('#candidate_1').val(),
                  preference: $('#preference_1').val(),
                  ward: $('#ward').val()
              }, function(data) {
                  update_candidate(0, data.viewdata, data.results, type);
              });
    $.getJSON($SCRIPT_ROOT + '/get_candidate_data', {
                  candidate_id:  $('#candidate_2').val(),
                  preference: $('#preference_2').val(),
                  ward: $('#ward').val()
              }, function(data) {
                  update_candidate(1, data.viewdata, data.results, type);
              });
    
}

function update_candidate(candidate, viewdata, results, type) {
    for (i in results) {
        var station = results[i];
        add_heat(candidate, station, map, type);
        $("#"+candidate+station.id).text(station.votes["total"] + "  (" + station.votes["percentage"] + "%)");
        $("#"+candidate+station.id).css("background-color", colours[candidate]);
    }
    map.setCenter(new google.maps.LatLng(viewdata.centre_lat, viewdata.centre_lon));
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