var application_data = {
    locations: []
};

function parseData(data) {
    var incoming_data = JSON.parse(data);
    console.info("Data received: " + incoming_data);

    if (incoming_data.nearest_restaurants !== undefined) {
        if (incoming_data.nearest_restaurants === "{ \"error\": \"None found\" }") {
            $("#output-holder").html("No matches");
            return;
        }
        console.log("Nearest restaurant received: ");
        console.info(incoming_data.nearest_restaurants);
        nearest_restaurants = incoming_data.nearest_restaurants;
        deleteMarkers();
        for (var i = nearest_restaurants.length - 1; i >= 0; i--) {
           var restaurant = nearest_restaurants[i]

    // Do something with nearest restaurant
    categories = format_json(restaurant['categories']);
    title = restaurant['title'];
    price = restaurant['price'];
    console.info(toTitleCase(title), price, categories);
    cat_string = "";
    for (var i = 0; i < categories.length; i++) {
        cat_string += categories[i]["title"] + "\t"
    }
    $("#output-holder").html("<p>" + title + "</p>" +
        "<p>" + price + "</p>" +
        "<p>" + cat_string + "</p>");
    
    var content = "<div class='marker-content'><h4 class='text-primary'>" + title + "</h4>" 
    + "<p>Price: " + price + "</p>" 
    + "<p>Food: " + cat_string + "</p>" 
    + "</div>";

    create_marker(restaurant['latitude'], restaurant['longitude'], title,content);
}



} else if (incoming_data.connection !== undefined) {
    console.log("Connection to websocket opened.");
    requestLocations();

} else if (incoming_data.locations !== undefined) {
    console.log("Received all restaurant locations");
    application_data.locations = incoming_data.locations;
}
else {
    console.error("Unexpected value in parser.js" + incoming_data);
}
}

function format_json(string) {
    return JSON.parse(string.replaceAll('u', '').replaceAll("'", '"'));
}