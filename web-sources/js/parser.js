var application_data = {
    locations: [],
    user_location: [40.5, -73.9]
};

function parseData(data) {
    var incoming_data = JSON.parse(data);
    console.info("Data received: ", incoming_data);

    if (incoming_data.nearest_restaurants !== undefined) {
        handle_nearest_restaurants(incoming_data.nearest_restaurants)

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

function handle_nearest_restaurants(nearest_restaurants) {
    initMap();
    if (nearest_restaurants === "{ \"error\": \"None found\" }") {
        $("#output-holder").html("No matches");
        return;
    }
    console.log("Nearest restaurant received: ");
    deleteMarkers();
    for (var i = nearest_restaurants.length - 1; i >= 0; i--) {
        var restaurant = nearest_restaurants[i]

        // Do something with nearest restaurant
        categories = format_json(restaurant['categories']);
        title = restaurant['title'];
        price = restaurant['price'];
        console.info(toTitleCase(title), price, categories);
        cat_string = "";
        for (var j = 0; j < categories.length; j++) {
            cat_string += categories[j]["title"] + "\t"
        }
        $("#output-holder").html("<p>" + toTitleCase(title) + "</p>" +
            "<p>" + price + "</p>" +
            "<p>" + cat_string + "</p>");

        var content = "<div class='marker-content'><h4 class='text-primary'>" + toTitleCase(title) + "</h4>"
            + "<p>Price: " + price + "</p>"
            + "<p>Food: " + cat_string + "</p>"
            + "</div>";

        create_marker(restaurant['latitude'], restaurant['longitude'], title, content);
    }
    create_user_marker(application_data.user_location[0], application_data.user_location[1]);
}

function format_json(string) {
    return JSON.parse(string.replaceAll('u', '').replaceAll("'", '"'));
}