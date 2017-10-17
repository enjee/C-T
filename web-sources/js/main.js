$("#btn-nearest").click(function () {
    var latitude = $("#input-lat").val();
    var longitude = $("#input-lon").val();
    console.log(latitude, longitude);
    requestNearest(latitude, longitude);
});


function initMap() {
    var ny = {lat: 40.73, lng: -73.93};
    var map = new google.maps.Map(document.getElementById('map'), {
        zoom: 9,
        center: ny
    });

    locations = application_data.locations;
    for (var i in locations) {
        loc = locations[i];
        lat = loc['lat'];
        lon = loc['lon'];
        title = loc['title'];
        var marker = create_marker(lat, lon, title, map);
    }
}

function create_marker(lat, lon, title, map) {
    var marker = new google.maps.Marker({
        position: {lat: lat, lng: lon},
        title: toTitleCase(title.replace(/-/g, " ")),
        map: map
    });
    return marker;
}

function toTitleCase(str)
{
    return str.replace(/\w\S*/g, function(txt){return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();});
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