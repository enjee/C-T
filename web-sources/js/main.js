$( document ).ready(function() {
    setTimeout(requestCategories,2000);
});

$("#btn-nearest").click(function () {
    var latitude = $("#input-lat").val();
    var longitude = $("#input-lon").val();
    var price = $("#input-price").val();
    var category = $("#input-cat").val();
    console.log(category);
    application_data.user_location = [parseFloat(latitude), parseFloat(longitude)];
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
    var user_loc;
    if (application_data.user_location === undefined) {
        user_loc = {lat: 40.77, lng: -73.93};
    } else {
        user_loc = {lat: application_data.user_location[0], lng: application_data.user_location[1]}
    }
     map = new google.maps.Map(document.getElementById('map'), {
        zoom: 11,
        center: user_loc
    });
}

function create_marker(lat, lon, title, yelp_id, contentstring, pinImage) {
    var marker = new google.maps.Marker({
        position: {lat: lat, lng: lon},
        title: toTitleCase(title),
        map: map,
        icon: pinImage,
        yelp_id: yelp_id
    });
    markers.push(marker);
 
     google.maps.event.addListener(marker, 'click', (function (marker, contentstring) {
            return function () {
                setMarkerInfoBox(marker, contentstring);
            };
        })(marker, contentstring));
}

function create_user_marker(lat, lon) {
    console.log(lat, lon)
    var marker = new google.maps.Marker({
        position: {lat: parseFloat(lat), lng: parseFloat(lon)},
        title: "Your current location",
        map: map,
        icon: {
            path: google.maps.SymbolPath.BACKWARD_CLOSED_ARROW,
            scale: 4
        }
    });
    markers.push(marker);
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
        console.log(marker);
     $("#restaurant-info").html("<h4 class='text-primary'>" + toTitleCase(marker.title) + "</h4>");
     LoadReviewsForRestaurant(marker.yelp_id);
}

function showEqualRestaurants(clicked_button) {
    requestEqual(clicked_button.id, 5);
}

function LoadReviewsForRestaurant(yelp_id) {
    requestYelpReviews(yelp_id);
}

