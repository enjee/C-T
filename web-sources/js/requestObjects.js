function requestNearest(latitude, longitude, price, categories) {
    var request = {
        type: "nearest",
        latitude: latitude,
        longitude: longitude,
        price: price
    };
    if (categories !== null && categories) {
        request.categories = categories;
    }
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


