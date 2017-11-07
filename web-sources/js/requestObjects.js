function requestNearest(latitude, longitude, price, categories) {
    var request = {
        type: "nearest",
        latitude: latitude,
        longitude: longitude,
        price: price,
        limit: 5
    };
    if (categories !== null && categories) {
        request.categories = categories;
    }
    console.log(request);
    sendObject(request);
}

function requestAll() {
    var request = {
        type: "all_restaurants"
    };
    sendObject(request);
}

function requestEqual(restaurant_id, limit) {
    var request = {
        type: "equal",
        restaurant: parseInt(restaurant_id),
        limit: limit
    };
    sendObject(request);
}

function requestCategories() {
   var request = {
       type: "categories"
   };
   sendObject(request);
}

function requestYelpReviews(yelp_id) {
    var request = {
        type: "reviews",
        yelp_id: yelp_id
    };
    sendObject(request);
}


function sendObject(object) {
    if (connected) {
        var json_object = JSON.stringify(object);
        websocket.send(json_object);
    }
}


