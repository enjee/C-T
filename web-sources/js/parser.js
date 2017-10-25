var application_data = {
    restaurants: [],
    user_location: [40.77, -73.98]
};

/**
 *  Parse incoming data
 */
function parseData(data) {
    var incoming_data = JSON.parse(data);
    console.info("Data received: ", incoming_data);

    if (incoming_data.nearest_restaurants !== undefined) {
        handle_nearest_restaurants(incoming_data.nearest_restaurants)

    } else if (incoming_data.connection !== undefined) {
        console.log("Connection to websocket opened.");

    } else if (incoming_data.all_restaurants !== undefined) {
        console.log("Received all restaurant locations");
        application_data.restaurants = incoming_data.all_restaurants;

    } else if (incoming_data.equal_restaurants !== undefined) {
        console.log("Received equal restaurants");
        equal_restaurants = incoming_data.equal_restaurants;
        handle_equal_restaurants(equal_restaurants);
    }
    else if (incoming_data.categories !== undefined) {
        console.log("Received categories");
        categories = incoming_data.categories.sort().reverse();
        handle_categories(categories);
    }
    else {
        console.error("Unexpected value in parser.js" + incoming_data);
    }
}


/**
 *  Helper methods that actually do the parsing
 */
function handle_nearest_restaurants(nearest_restaurants) {
    initMap();
    deleteMarkers();
    if (nearest_restaurants === "{ \"error\": \"None found\" }") {
        $("#output-holder").html("No matches");
        return;
    }
    for (var i = nearest_restaurants.length - 1; i >= 0; i--) {
        var restaurant = nearest_restaurants[i];
        create_marker_from_restaurant(restaurant, "FE7569");
    }
    create_user_marker(application_data.user_location[0], application_data.user_location[1]);
}

function handle_equal_restaurants(equal_restaurants) {
    for (var i = equal_restaurants.length - 1; i >= 0; i--) {
        var restaurant = equal_restaurants[i];
        create_marker_from_restaurant(restaurant, "009900");
    }
}

function create_marker_from_restaurant(restaurant, pinColor) {
    var pinImage = new google.maps.MarkerImage("http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=%E2%80%A2|" + pinColor,
        new google.maps.Size(21, 34),
        new google.maps.Point(0, 0),
        new google.maps.Point(10, 34));

    // Do something with nearest restaurant
    categories = format_json(restaurant['categories']);
    title = restaurant['title'];
    id = restaurant['id'];
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
        + "<button id='" + id + "' type='button' class='btn btn-success' onclick='showEqualRestaurants(this)'>Show restaurants like this one</button>"
        + "</div>";

    create_marker(restaurant['latitude'], restaurant['longitude'], title, content, pinImage);
}

function format_json(string) {
    return JSON.parse(string.replaceAll('u', '').replaceAll("'", '"'));
}


function handle_categories(categories) {
    for (var i = categories.length - 1; i >= 0; i--) {
         var cat = categories[i];
          $('#input-cat')
         .append($("<option></option>")
                    .attr("value",cat)
                    .text(cat)); 
    }
}

