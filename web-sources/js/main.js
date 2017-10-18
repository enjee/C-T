$("#btn-nearest").click(function () {
    var latitude = $("#input-lat").val();
    var longitude = $("#input-lon").val();
    var price = $("#input-price").val();
    var category = $("#input-cat").val();

    requestNearest(latitude, longitude, price, category);
});

String.prototype.replaceAll = function(search, replacement) {
    var target = this;
    return target.replace(new RegExp(search, 'g'), replacement);
};

var map;
var markers = [];
var mapinfobox = null;

function initMap() {
    var ny = {lat: 40.73, lng: -73.93};
     map = new google.maps.Map(document.getElementById('map'), {
        zoom: 9,
        center: ny
    });
}

function create_marker(lat, lon, title, contentstring) {
    var marker = new google.maps.Marker({
        position: {lat: lat, lng: lon},
        title: toTitleCase(title),
        map: map
    });
    markers.push(marker);
 
     google.maps.event.addListener(marker, 'click', (function (marker, contentstring) {
            return function () {
                setMarkerInfoBox(marker, contentstring);
            };
        })(marker, contentstring));
}

 // Sets the map on all markers in the array.
      function setMapOnAll(map) {
        for (var i = 0; i < markers.length; i++) {
          markers[i].setMap(map);
        }
      }

      // Removes the markers from the map, but keeps them in the array.
      function clearMarkers() {
        setMapOnAll(null);
      }

// Deletes all markers in the array
      function deleteMarkers() {
        clearMarkers();
        markers = [];
      }

function toTitleCase(str) {
    return str.replace(/-/g, " ").replace(/\w\S*/g, function(txt){return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();});
}

$().ready(function () {
    $("#container-error").hide();
    $("#btn-close-alert").click(function () {
        $("#container-error").finish().hide();
    });
});

function showErrorPopup(message) {
    $("#msg-error").html(message);
    $("#container-error").finish().show(300).delay(3000).fadeOut(4000);
}

function setMarkerInfoBox(marker, content) {

    if (mapinfobox) {
        mapinfobox.close();
    }

    mapinfobox = new google.maps.InfoWindow({
        content: content
    });

    mapinfobox.open(map, marker);
}