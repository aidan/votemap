function draw_map(viewdata, results) {
    var myOptions = {
        center: new google.maps.LatLng(viewdata.centre_lat, viewdata.centre_lon),
        zoom: 14,
        mapTypeId: google.maps.MapTypeId.ROADMAP
    };
    var map = new google.maps.Map(document.getElementById("map_canvas"),
                                  myOptions);

}

$(function() {
      $.getJSON($SCRIPT_ROOT + '/get_candidate_data', {
                  candidate_id:  candidate_id
              }, function(data) {
                  draw_map(data.viewdata, data.result);
              });
      
});

