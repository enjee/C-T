$( document ).ready(function() {
    setTimeout(requestCategories,2000);
});

$("#btn-nearest").click(function () {
    var latitude = $("#input-lat").val();
    var longitude = $("#input-lon").val();
    var price = $("#input-price").val();
    var category = $("#input-cat").val();
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
var userMarker = null;

function initMap() {
    var user_loc;
    if (application_data.user_location === undefined) {
        userMarker = {lat: 40.77, lng: -73.93};
    } else {
        userMarker = {lat: application_data.user_location[0], lng: application_data.user_location[1]}
    }
     map = new google.maps.Map(document.getElementById('map'), {
        zoom: 11,
        center: userMarker
    });
}

function create_marker(lat, lon, title, yelp_id, rating,cat_string,address_string,contentstring, pinImage) {
    var marker = new google.maps.Marker({
        position: {lat: lat, lng: lon},
        title: toTitleCase(title),
        map: map,
        icon: pinImage,
        yelp_id: yelp_id,
        rating: rating,
        cat_string: cat_string,
        address_string: address_string
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
    
    loadInfoForRestaurant(marker);
    loadReviewsForRestaurant(marker.yelp_id);
}

function showEqualRestaurants(clicked_button) {
    requestEqual(clicked_button.id, 5);
}

function loadInfoForRestaurant(marker)
{
    var html = "";
    html += "<h4 class='text-primary'>" + toTitleCase(marker.title) + "</h4>";

    for(i = 1; i <= 5; i++)
    {
        if(i <= parseInt(marker.rating))
        {
            html += "<span class='glyphicon glyphicon-star' aria-hidden='true'></span>";
        }
        else
        {
            html += "<span class='glyphicon glyphicon-star-empty' aria-hidden='true'></span>";
        }
    }
    html += "<h5 class='text-primary'>Food: " + marker.cat_string + "</h5>";
    html += "<h5 class='text-primary'>Address: " + marker.address_string + "</h5>";
    html += "<button id='btn-showRoute' data-id='"+ marker.yelp_id +"' type='button' onclick='showRoute(this)' class='btn btn-success'>Show route</button>";
    $("#restaurant-info").html(html);
     
}

function loadReviewsForRestaurant(yelp_id) {
    requestYelpReviews(yelp_id);
}

function showRoute(clicked_button) {
    var selectedmarker =  $.grep(markers, function(e){ return e.yelp_id == $(clicked_button).attr('data-id') });
    calculateAndDisplayRoute(selectedmarker[0]);
}

function calculateAndDisplayRoute(pointRestaurant) {
      var directionsService = new google.maps.DirectionsService();
       var directionsDisplay = new google.maps.DirectionsRenderer({
            map: map
        });
    directionsService.route({
        origin: new google.maps.LatLng(userMarker.lat,userMarker.lng),
        destination: new google.maps.LatLng(pointRestaurant.getPosition().lat(),pointRestaurant.getPosition().lng()),
        avoidTolls: true,
        avoidHighways: false,
        travelMode: google.maps.TravelMode.DRIVING
    }, function (response, status) {
        if (status == google.maps.DirectionsStatus.OK) {
            directionsDisplay.setDirections(response);
        } else {
            window.alert('Directions request failed due to ' + status);
        }
    });
}

