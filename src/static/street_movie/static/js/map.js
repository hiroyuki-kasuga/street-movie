var googlemap = (function () {
    var markerList = new google.maps.MVCArray(),
        latlng = new google.maps.LatLng(35.681382, 139.766084),
        geocoder = new google.maps.Geocoder(),
        opts = {
            zoom: 16,
            mapTypeId: google.maps.MapTypeId.ROADMAP,
            center: latlng,
            mapTypeControl: false,
            panControl: false,
            streetViewControl: false
        },
        samplestyle = [
            {
                "stylers": [
                    {"visibility": "on"},
                    {"weight": 1.2},
                    {"saturation": 22},
                    {"lightness": 26},
                    {"gamma": 1.51}
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
        markerA, markerB, streetViewLayer, movieLatLngList = [], circle, isEnableCreateMovie = false, startName, endName;

    return {
        init: function () {
            $(window).resize(function () {
                if (windowResizeTimer !== false) {
                    clearTimeout(windowResizeTimer);
                }
                windowResizeTimer = setTimeout(function () {
                    map.setCenter(currentCenter);
                    googlemap.showCircle();
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

            $('.cmd-open-twitter').on('click', function (e) {
                e.preventDefault();
                var title = $(this).prop('title'),
                    loc = $(this).prop('href');
                window.open('http://twitter.com/share?url=' + loc + '&text=' + title + '&', 'twitterwindow', 'height=450, width=550, top=' + ($(window).height() / 2 - 225) + ', left=' + $(window).width() / 2 + ', toolbar=0, location=0, menubar=0, directories=0, scrollbars=0');
            });

            $('.cmd-open-facebook').on('click', function (e) {
                e.preventDefault();
                FB.ui({
                    method: 'share',
                    href: $(this).prop('href'),
                    redirect_uri: $(this).prop('href')
                }, function (response) {

                });
            });

            $('.cmd-over-settings').on('click', function (e) {
                e.preventDefault();
                $('.operation-area').addClass('move');
                googlemap.showCircle();
            });

            $('.cmd-hide-operation-area').on('click', function (e) {
                e.preventDefault();
                $('.operation-area').removeClass('move');
                googlemap.hideCircle();
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
                var $videoContainer = $('.video-container'),
                    $videoWrapper = $('.video-wrapper'),
                    $video = $('.video');
                $video.hide();
                $videoWrapper.hide();
                $videoContainer.hide();
            });

            $('.cmd-open-term').on('click', function(e){
                e.preventDefault();
                var $termContainer = $('.term-container'),
                    $wrapper = $('.term-wrapper');
                $wrapper.show();
                $termContainer.addClass('visible');
            });

            $('.cmd-hide-term-wrapper').on('click', function (e) {
                e.preventDefault();
                var $termContainer = $('.term-container'),
                    $wrapper = $('.term-wrapper');
                $wrapper.hide();
                $termContainer.removeClass('visible');
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
                    endLon = markerBLatLon.lng().toFixed(6),
                    $btnFb = $('.cmd-open-facebook'),
                    $btnTw = $('.cmd-open-twitter'),
                    $caution = $('.caution');

                if (!isEnableCreateMovie) {
                    alert("開始地点と終了地点を指定してください。");
                    return;
                }

                $loading.show();
                $.ajax(url, {
                    data: {
                        latLng: latLng,
                        csrfmiddlewaretoken: csrfToken,
                        start_lat: startLat,
                        start_lon: startLon,
                        end_lat: endLat,
                        end_lon: endLon,
                        start_name: startName,
                        end_name: endName,
                        center_lat: currentCenter.lat().toFixed(6),
                        center_lon: currentCenter.lng().toFixed(6)
                    },
                    dataType: 'json',
                    type: 'POST'
                }).done(function (data) {
                    $loading.hide();
                    if (data.status === 1) {
                        $video.prop('src', data.data.movie);
                        $wrapper.show();
                        $btnFb.prop('href', data.data.sns_url);
                        $btnTw.prop('href', data.data.sns_url);
                        $btnTw.prop('title', data.data.sns_title);
                        $video.parents().find('.video').show();
                        $video.parents().find('.video-container').show();
                        $caution.html(data.data.count);
                    }
                });
            });

            $('.cmd-over-settings').trigger('click');
            googlemap.showCircle();
            googlemap.createMarkerA();
            googlemap.createMarkerB();
        },
        hideCircle: function () {
            //if(circle){
            //    circle.setMap(null);
            //}
        },
        showCircle: function () {
            //googlemap.hideCircle();
            //circle = new google.maps.Circle({
            //    strokeColor: "#FF0000",
            //    strokeOpacity: 0.8,
            //    strokeWeight: 2,
            //    fillColor: "#FF0000",
            //    fillOpacity: 0.35,
            //    map: map,
            //    center: currentCenter,
            //    radius: 1000
            //});
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
                googlemap.showCircle();
                googlemap.hideAddress();
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
                googlemap.getAddress();
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
                googlemap.getAddress();
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
        hideAddress: function () {
            var $startAddressArea = $('#start-address-area'),
                $endAddressArea = $('#end-address-area');
            $startAddressArea.hide();
            $endAddressArea.hide();
        },
        getAddress: function () {
            var $startAddressArea = $('#start-address-area'),
                $endAddressArea = $('#end-address-area'),
                $startAddress = $('#start-address'),
                $endAddress = $('#end-address');
            new google.maps.Geocoder().geocode({latLng: markerALatLon}, function (results, status) {
                if (status == google.maps.GeocoderStatus.OK) {
                    // results.length > 1 で返ってくる場合もありますが・・・。
                    if (results[0].geometry) {
                        startName = results[0].formatted_address.replace(/^日本, /, '');
                        $startAddress.html(startName);
                        $startAddressArea.show();
                    }
                }
            });
            new google.maps.Geocoder().geocode({latLng: markerBLatLon}, function (results, status) {
                if (status == google.maps.GeocoderStatus.OK) {
                    // results.length > 1 で返ってくる場合もありますが・・・。
                    if (results[0].geometry) {
                        endName = results[0].formatted_address.replace(/^日本, /, '');
                        $endAddress.html(endName);
                        $endAddressArea.show();
                    }
                }
            });
        },
        startRoute: function () {
            var d = Math.round(google.maps.geometry.spherical.computeDistanceBetween(markerALatLon, markerBLatLon));
            if (d > 1500) {
                alert("1500m以内を選択してください。");
                return false;
            }
            isEnableCreateMovie = true;
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
                        var latLng1 = new google.maps.LatLng(v.lat(), v.lng()), latLng2, meter, formatMeter, radius;

                        if (response.routes[0].overview_path.length - 1 == k) {
                            var tmpLatLng = movieLatLngList[movieLatLngList.length - 1];
                            radius = tmpLatLng.radius;
                        } else {
                            latLng2 = new google.maps.LatLng(response.routes[0].overview_path[k + 1].lat(), response.routes[0].overview_path[k + 1].lng());
                            meter = google.maps.geometry.spherical.computeDistanceBetween(latLng1, latLng2);
                            formatMeter = meter.toFixed(0);
                            radius = googlemap.geoDirection(latLng1.lat(), latLng1.lng(), latLng2.lat(), latLng2.lng());
                        }

                        if (k !== 0) {
                            movieLatLngList.push({
                                lat: latLng1.lat(),
                                lng: latLng1.lng(),
                                radius: radius
                            });

                            for (var i = 100; i < formatMeter; i++) {
                                var latLng3 = google.maps.geometry.spherical.computeOffset(latLng1, i, radius);
                                movieLatLngList.push({
                                    lat: latLng3.lat(),
                                    lng: latLng3.lng(),
                                    radius: radius
                                });
                            }

                        } else {
                            movieLatLngList.push({
                                lat: v.lat(),
                                lng: v.lng(),
                                radius: radius
                            });
                        }
                    });

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