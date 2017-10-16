function parseData(data) {
    var incoming_data = JSON.parse(data);

    if (incoming_data.nearest_restaurant !== undefined) {
        console.log("Nearest restaurant received: " + incoming_data.nearest_restaurant);
        $("#output-holder").html(incoming_data.nearest_restaurant);

    } else {
        console.error("Unexpected value in parser.js");
    }
}