$("#btn-nearest").click(function () {
    var latitude = $("#input-lat").val();
    var longitude = $("#input-lon").val();
    console.log(latitude, longitude);
    requestNearest(latitude, longitude);
});