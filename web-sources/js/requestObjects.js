function requestNearest(latitude, longitude) {
    var request = {
        type: "nearest",
        latitude: latitude,
        longitude: longitude
    };
    sendObject(request)
}

function requestLocations() {
    var request = {
        type: "locations"
    };
    sendObject(request)
}

function sendObject(object) {
    if (connected) {
        var json_object = JSON.stringify(object);
        websocket.send(json_object);
    }
}


