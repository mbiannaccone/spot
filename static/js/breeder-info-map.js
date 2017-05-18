// JavaScript for Google Maps API on breeder info page. 

function initMap() {
  var map = new google.maps.Map(document.getElementById('map'), {
    zoom: 8,
    center: {lat: 37.5100571, lng: -117.967836}
  });
  var geocoder = new google.maps.Geocoder();

  var address = document.getElementById("address").innerText;

  geocodeAddress(geocoder, map, address);
}

function geocodeAddress(geocoder, resultsMap, address) {
  geocoder.geocode({'address': address}, function(results, status) {
    if (status === 'OK') {
      resultsMap.setCenter(results[0].geometry.location);
      var marker = new google.maps.Marker({
        position: results[0].geometry.location,
        map: resultsMap
      });
    } else {
      alert('Geocode was not successful for the following reason: ' + status);
    }
  });
}