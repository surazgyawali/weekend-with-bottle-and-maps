var markerClusterer = null;
var map = null;
function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
        zoom: 4.5,
        center: new google.maps.LatLng(-25.363, 131.044),
        mapTypeId: google.maps.MapTypeId.ROADMAP
    });
}


function locate_offices() {
    // refreshMap()
    selectElement = document.getElementById("serviceName")
    serviceId = selectElement.value
    httpGetAsync('/getoffices?serviceid=' + serviceId, show_marker_clusters)

}


function show_marker_clusters(responseText) {

    if (markerClusterer) {
        markerClusterer.clearMarkers();
    }

    var markers = [];
    jObj = JSON.parse(responseText)

    jObj.data.forEach(function (data) {

        lat = parseFloat(data[5])
        lng = parseFloat(data[6])
        title = data[1]

        contactName=data[1]
        suburb=data[2]
        phoneNumber=data[3]
        emailAddress=data[4]

        var latLng = new google.maps.LatLng(lat, lng)
        var contentString = '<h1 id="firstHeading" class="firstHeading">'+ contactName +'</h1>'+
        '<div><b><p>'+suburb+'<br>'+phoneNumber+'<br>'+
        "<a href=mailto:"+emailAddress+">"+emailAddress+"</a>"+
        '</p></b></div>'

        var infowindow = new google.maps.InfoWindow({
            content: contentString
        });

        var marker = new google.maps.Marker({
            position: latLng,
            draggable: false,
            animation: google.maps.Animation.DROP,
            title: title
        });

        marker.addListener('click', function () {
            infowindow.open(map, marker);
        });

        markers.push(marker);

    })

    markerClusterer = new MarkerClusterer(map, markers, {
        zoom: 6,
        imagePath: '/static/images/m'
    });

}


function httpGetAsync(theUrl, callback) {
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function () {
        if (xmlHttp.readyState == 4 && xmlHttp.status == 200)
            callback(xmlHttp.responseText);
    }
    xmlHttp.open("GET", theUrl, true); // true for asynchronous
    xmlHttp.send(null);
}


function clearClusters(e) {
    e.preventDefault();
    e.stopPropagation();
    markerClusterer.clearMarkers();
}