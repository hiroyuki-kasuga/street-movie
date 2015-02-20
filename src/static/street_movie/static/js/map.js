var googlemap = (function () {
    var markerList = new google.maps.MVCArray(),
        latlng = new google.maps.LatLng(35.681382, 139.766084),
        geocoder = new google.maps.Geocoder(),
        opts = {zoom: 16, mapTypeId: google.maps.MapTypeId.ROADMAP, center: latlng, mapTypeControl: false, panControl: false, streetViewControl: false},
        samplestyle = [
            {
                "stylers": [
                    { "visibility": "on" },
                    { "weight": 1.2 },
                    { "saturation": 22 },
                    { "lightness": 26 },
                    { "gamma": 1.51 }
                ]
            }
        ],
        samplestyleOptions = {name: "シンプル"},
        sampleMapType = new google.maps.StyledMapType(samplestyle, samplestyleOptions),
        map = new google.maps.Map(document.getElementById("map"), opts),
        m = map.mapTypes.set('simple', sampleMapType),
        n = map.setMapTypeId('simple'),
        currentCenter = latlng,
        windowResizeTimer = false,
        directionsDisplay = new google.maps.DirectionsRenderer({
            suppressMarkers: true,
            polylineOptions: {
                strokeColor: '#000000',
                strokeWeight: 7,
                strokeOpacity: 0.7
            }
        }),
        markerAImg = 'http://chart.apis.google.com/chart?chst=d_map_pin_letter_withshadow&chld=S%7CFFFFFF%7C000000',
        markerBImg = 'http://chart.apis.google.com/chart?chst=d_map_pin_letter_withshadow&chld=E%7CFFFFFF%7C000000',
        directionsService = new google.maps.DirectionsService(),
        markerALatLon = currentCenter,
        markerBLatLon = new google.maps.LatLng(35.681382 - 0.001, 139.766084),
        markerA, markerB, streetViewLayer, movieLatLngList = [];

    return {
        init: function () {
            $(window).resize(function () {
                if (windowResizeTimer !== false) {
                    clearTimeout(windowResizeTimer);
                }
                windowResizeTimer = setTimeout(function () {
                    map.setCenter(currentCenter);
                }, 200);
            });

            google.maps.event.addListener(map, 'dragend', function (e) {
                currentCenter = map.getCenter();
            });

            google.maps.event.addListener(map, 'zoom_changed', function () {
                var zoomLevel = map.getZoom();
//                directionsDisplay.setDottedPolylineOptions({
//                    icon: {
//                        fillColor: 'red', //or hexadecimal color such as: '#FF0000'
//                        fillOpacity: 0.8,
//                        scale: 3,
//                        strokeColor: 'blue',
//                        strokeWeight: 1,
//                        strokeOpacity: 0.8,
//                        path: google.maps.SymbolPath.CIRCLE
//                    },
//                    repeat: '10px'
//                });
            });

            $('.cmd-over-settings').on('click', function (e) {
                e.preventDefault();
                $('.operation-area').addClass('move');
            });

            $('.cmd-hide-operation-area').on('click', function (e) {
                e.preventDefault();
                $('.operation-area').removeClass('move');
            });

            $('.cmd-search').on('click', function (e) {
                e.preventDefault();
                googlemap.search();
            });

            $('#search_spot').on('keydown', function (e) {
                if (e.keyCode == 13) {
                    googlemap.search();
                    return false;
                }
            });

            $('.cmd-hide-wrapper').on('click', function (e) {
                e.preventDefault();
                var $videoWrapper = $('.video-wrapper'),
                    $video = $('.video');
                $video.hide();
                $videoWrapper.hide();

            });

            $('.cmd-make-movie').on('click', function (e) {
                e.preventDefault();
                var latLng = JSON.stringify(movieLatLngList, null, ""),
                    csrfToken = $('input[name="csrfmiddlewaretoken"]').val(),
                    url = $(this).data('url'),
                    $loading = $('.loading'),
                    $video = $('#video'),
                    $wrapper = $('.video-wrapper'),
                    startLat = markerALatLon.lat().toFixed(6),
                    startLon = markerALatLon.lng().toFixed(6),
                    endLat = markerBLatLon.lat().toFixed(6),
                    endLon = markerBLatLon.lng().toFixed(6);
                $loading.show();
                $.ajax(url, {
                    data: {latLng: latLng, csrfmiddlewaretoken: csrfToken, start_lat: startLat, start_lon: startLon, end_lat: endLat, end_lon: endLon},
                    dataType: 'json',
                    type: 'POST'
                }).done(function (data) {
                    $loading.hide();
                    if (data.status === 1) {
                        $video.prop('src', data.data.movie);
                        $wrapper.show();
                        $video.parents().find('.video').show();
                    }
                });
            });

            $('.cmd-over-settings').trigger('click');
            googlemap.createMarkerA();
            googlemap.createMarkerB();
        },
        search: function () {
            var searchSpot = $('#search_spot').val(),
                searchWord = $.trim(searchSpot);
            if (searchWord.length === 0) {
                return false;
            }

            geocoder.geocode({address: searchWord}, function (results, status) {
                if (results.length == 0) {
                    return;
                }
                //$('.operation-area').removeClass('move');
                markerALatLon = new google.maps.LatLng(results[0].geometry.location.lat(), results[0].geometry.location.lng());
                markerBLatLon = new google.maps.LatLng(results[0].geometry.location.lat(), results[0].geometry.location.lng() - 0.001);
                currentCenter = markerALatLon;
                map.setCenter(currentCenter);
                googlemap.createMarkerA();
                googlemap.createMarkerB();

            });
        },
        createMarkerA: function () {

            if (markerA) {
                markerA.setMap(null);
            }

            markerA = new google.maps.Marker({
                position: markerALatLon,
                title: "Start Point",
                draggable: true,
                icon: markerAImg
            });
            google.maps.event.addListener(markerA, 'dragstart', function (e) {
                googlemap.showStreetViewLayer();
            });
            google.maps.event.addListener(markerA, 'dragend', function (e) {
                map.overlayMapTypes.pop();
                markerALatLon = new google.maps.LatLng(e.latLng.lat(), e.latLng.lng());
                googlemap.startRoute();
            });
            markerA.setMap(map);
        },
        createMarkerB: function () {

            if (markerB) {
                markerB.setMap(null);
            }

            markerB = new google.maps.Marker({
                position: markerBLatLon,
                title: "End Point",
                draggable: true,
                icon: markerBImg
            });
            google.maps.event.addListener(markerB, 'dragstart', function (e) {
                googlemap.showStreetViewLayer();
            });
            google.maps.event.addListener(markerB, 'dragend', function (e) {
                map.overlayMapTypes.pop();
                markerBLatLon = new google.maps.LatLng(e.latLng.lat(), e.latLng.lng());
                googlemap.startRoute();
            });
            markerB.setMap(map);
        },
        showStreetViewLayer: function () {
            streetViewLayer = new google.maps.ImageMapType({
                getTileUrl: function (coord, zoom) {
                    var X = coord.x % (1 << zoom);
                    return "http://mt1.googleapis.com/vt?hl=ja&lyrs=svv|cb_client:apiv3&style=40,18&x=" + X + "&y=" + coord.y + "&z=" + zoom;
                },
                tileSize: new google.maps.Size(256, 256),
                isPng: true
            });
            map.overlayMapTypes.push(streetViewLayer);
        },
        startRoute: function () {
            var request = {
                origin: markerALatLon,
                destination: markerBLatLon,
                travelMode: google.maps.DirectionsTravelMode.DRIVING,
                provideRouteAlternatives: true,
                avoidHighways: false,
                avoidTolls: false
            };
            directionsService.route(request, function (response, status) {
                if (status == google.maps.DirectionsStatus.OK) {
                    var numOfRoutes = response.routes.length;
                    movieLatLngList = [];
                    $.each(response.routes[0].overview_path, function (k, v) {
                        //console.log('http://maps.googleapis.com/maps/api/streetview?size=600x300&location=' + v.lat() + ',%20' + v.lng() + '&sensor=false');
                        if (k !== 0) {
                            var latLng1 = new google.maps.LatLng(v.lat(), v.lng()),
                                latLng2 = new google.maps.LatLng(response.routes[0].overview_path[k - 1].lat(), response.routes[0].overview_path[k - 1].lng()),
                                meter = google.maps.geometry.spherical.computeDistanceBetween(latLng1, latLng2);
//                                formatMeter = meter.toFixed(0),
//                                radius = googlemap.geoDirection(latLng1.lat(), latLng1.lng(), latLng2.lat(), latLng2.lng());
                            movieLatLngList.push({
                                lat: latLng1.lat(),
                                lng: latLng1.lng()
                            });

//                            for (var i = 5; i < formatMeter; i++) {
//                                var latLng3 = google.maps.geometry.spherical.computeOffset(latLng1, i, radius);
//                                movieLatLngList.push({
//                                    lat: latLng3.lat(),
//                                    lng: latLng3.lng()
//                                });
//                            }

                        } else {
                            movieLatLngList.push({
                                lat: v.lat(),
                                lng: v.lng()
                            });
                        }
                    });
                    console.log(movieLatLngList);

                    directionsDisplay.setMap(map);
                    directionsDisplay.setDirections(response);
                    directionsDisplay.setRouteIndex(0);
                }
            });
        },
        geoDirection: function (lat1, lng1, lat2, lng2) {
            // 緯度経度 lat1, lng1 の点を出発として、緯度経度 lat2, lng2 への方位
            // 北を０度で右回りの角度０～３６０度
            var Y = Math.cos(lng2 * Math.PI / 180) * Math.sin(lat2 * Math.PI / 180 - lat1 * Math.PI / 180);
            var X = Math.cos(lng1 * Math.PI / 180) * Math.sin(lng2 * Math.PI / 180) - Math.sin(lng1 * Math.PI / 180) * Math.cos(lng2 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180 - lat1 * Math.PI / 180);
            var dirE0 = 180 * Math.atan2(Y, X) / Math.PI; // 東向きが０度の方向
            if (dirE0 < 0) {
                dirE0 = dirE0 + 360; //0～360 にする。
            }
            var dirN0 = (dirE0 + 90) % 360; //(dirE0+90)÷360の余りを出力 北向きが０度の方向
            return dirN0;
        }
    };
})();

google.maps.event.addDomListener(window, "load", googlemap.init);