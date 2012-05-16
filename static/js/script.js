$(function() {
      alert("getting "+$SCRIPT_ROOT + '/get_candidate_data' + " for "+candidate_id);
      $.getJSON($SCRIPT_ROOT + '/get_candidate_data', {
                  candidate_id:  candidate_id
              }, function(data) {
                  alert(data.results);
              });
      
      var myOptions = {
          center: new google.maps.LatLng(),
          zoom: 8,
          mapTypeId: google.maps.MapTypeId.ROADMAP
      };
//      var map = new google.maps.Map(document.getElementById("map_canvas"),
//                                    myOptions);
});

