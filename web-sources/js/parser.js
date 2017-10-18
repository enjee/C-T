var application_data = {
  locations: []
};

function parseData(data) {
    var incoming_data = JSON.parse(data);
    console.log("Data received: " +incoming_data);

    if (incoming_data.nearest_restaurant !== undefined) {
        console.log("Nearest restaurant received: " + incoming_data.nearest_restaurant);
        $("#output-holder").html(incoming_data.nearest_restaurant);
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