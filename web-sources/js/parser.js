var application_data = {
    locations: []
};

function parseData(data) {
    var incoming_data = JSON.parse(data);
    console.info("Data received: " + incoming_data);

    if (incoming_data.nearest_restaurant !== undefined) {
        if (incoming_data.nearest_restaurant === "{ \"error\": \"None found\" }") {
            $("#output-holder").html("No matches");
            return;
        }
        console.log("Nearest restaurant received: ");
        console.info(incoming_data.nearest_restaurant);
        nearest_restaurant = incoming_data.nearest_restaurant;

        // Do something with nearest restaurant
        categories = format_json(nearest_restaurant['categories']);
        title = nearest_restaurant['title'];
        price = nearest_restaurant['price'];
        console.info(toTitleCase(title), price, categories);
        cat_string = "";
        for (var i = 0; i < categories.length; i++) {
            cat_string += categories[i]["title"] + "\t"
        }
        $("#output-holder").html("<p>" + title + "</p>" +
            "<p>" + price + "</p>" +
            "<p>" + cat_string + "</p>");


    } else if (incoming_data.connection !== undefined) {
        console.log("Connection to websocket opened.");
        requestLocations();

    } else if (incoming_data.locations !== undefined) {
        console.log("Received all restaurant locations");
        application_data.locations = incoming_data.locations;
        initMap();
    }
    else {
        console.error("Unexpected value in parser.js" + incoming_data);
    }
}

function format_json(string) {
    return JSON.parse(string.replaceAll('u', '').replaceAll("'", '"'));
}