var backgroundColor = '#231e1f'


$(document).ready(function() {

    loadDataCharts();

    $(".light-toggle-btn").click(function() {
        var id = $(this).attr('id');
        var id = id.split('-');
        var light = id[0];
        var state = id[1];
        toggleLight(light, parseInt(state));
        $(this).closest('.btn-group').children().removeClass("active");
        $(this).addClass("active");
    });

    passwordKeyUps();

});


function openSettings() {
    return;
}

function navHome() {
    $('.pageContainer:visible').fadeOut(700, function() {
        $('#homeBtnsContainer').fadeIn(700);
    });
}


function navPage(element, destination) {
    container = element.closest('.pageContainer');
    $(container).fadeOut("slow", function() {
        $('#' + destination).fadeIn('slow')
        loadSettings();
    });
}


function toggleLight(light, state) {
    var data = {}
    data.state = state;
    data.light = light;
    $.ajax({
        type: "POST",
        url: "API/toggleLight",
        data: JSON.stringify(data),
        ContentType: "application/json",
        success: function(status) {
            console.log(status);
        }
    });
}


function updateCycleSettings() {

    data = {
        'threshold': $("#sensorThreshold").val(),
        'drainTime': $("#drainTime").val() * 1000,
        'errorTime': $("#waterRunInTime").val() * 1000,
        'dryTime': $("#airrationTime").val() * 1000,
        'password': $("#password").val(),
        'dcPulse': $('#dcPulse').val() * 1000
    };
    $.ajax({
        type: "POST",
        url: "API/updateCycleSettings",
        data: JSON.stringify(data),
        ContentType: "application/json",
        success: function(data) {
            if (data.status == 'success') {
                $('.responseInput').css('color', '#5cc36e');
                $('#response').val('Success');
            } else {
                $('.responseInput').css('color', 'red');
                $('#response').val('Incorrect');
            }
            $('#passwordContainer').fadeOut(700, function() {
                $('#responseContainer').fadeIn(1000, function() {
                    $('#responseContainer').fadeOut(700, function() {
                        $('#passwordContainer').fadeIn(500);
                    });
                });
            });
        },
        error: function(status) {
            alert('Server Error');
        }
    });
}


function loadSettings() {
    $.ajax({
        type: "POST",
        url: "API/loadSettings",
        ContentType: "application/json",
        success: function(data) {
            console.log(data);
            lightStatuses = data.lightStatuses
            lightStatuses.forEach(function(status) {
                $('#' + status['lightName'] + "-" + status['mode']).addClass('active');
            });
            configuration = data.configuration
            $("#sensorThreshold").val(configuration.threshold);
            $("#drainTime").val(configuration.drainTime / 1000);
            $("#waterRunInTime").val(configuration.errorTime / 1000);
            $("#airrationTime").val(configuration.dryTime / 1000);
            $("#dcPulse").val(configuration.dcPulse / 1000);
        }
    });
}




function loadDataCharts() {
    $.ajax({
        type: "POST",
        url: "API/temperatureHumidityChart",
        //data : JSON.stringify(data),
        ContentType: "application/json",
        success: function(response) {

            var temperature = response['temperature'];
            for (var i = 0; i < temperature.length; i++) {
                temperature[i].x = moment.unix(temperature[i].x).toDate();
            }
            var humidity = response['humidity'];
            for (var i = 0; i < humidity.length; i++) {
                humidity[i].x = moment.unix(humidity[i].x).toDate();
            }



            var tempCtx = document.getElementById("temperature-chart").getContext('2d');
            var humidityCtx = document.getElementById("humidity-chart").getContext('2d');

            var gradient = tempCtx.createLinearGradient(0, 300, 0, 0);
            gradient.addColorStop(0, backgroundColor);
            gradient.addColorStop(1, "#4c959f");
            tempCtx.fillStyle = gradient;
            tempCtx.fillRect(10, 10, 200, 100);



            var temperatureConfig = {

                type: 'line',
                data: {
                    datasets: [
                        //
                        {
                            label: 'Temperature',
                            lineTension: 0.1,
                            data: temperature,
                            backgroundColor: gradient,
                            borderColor: "#4c959f",
                            fill: true,
                            pointBackgroundColor: 'white',
                            pointRadius: 1,
                            pointHoverRadius: 2,
                        }
                    ]
                },
                options: {
                    responsive: true,
                    title: {
                        display: false
                    },
                    scales: {
                        xAxes: [{
                            min: 10,
                            type: 'time',
                            display: true,
                            time: {
                                unit: 'day'
                            },
                            scaleLabel: {
                                display: false,
                            },
                            ticks: {
                                major: {
                                    fontStyle: 'bold',
                                    fontColor: '#FF0000'
                                }
                            }

                        }],
                        yAxes: [{
                            display: true,
                            scaleLabel: {
                                display: true,
                                labelString: 'Seconds'
                            },
                            ticks: {

                            }
                        }]
                    }
                },
            };


            var humidityConfig = {

                type: 'line',
                data: {
                    datasets: [
                        {
                            label: 'Humidity',
                            lineTension: 0,
                            data: humidity,
                            borderColor: "#e5766d",
                            fill: false,
                            pointBackgroundColor: 'white',
                            pointRadius: 0,
                            borderWidth: 1,
                        }

                    ]
                },
                options: {
                    responsive: true,
                    title: {
                        display: false
                    },
                    scales: {
                        xAxes: [{
                            min: 10,
                            type: 'time',
                            display: true,
                            time: {
                                unit: 'day'
                            },
                            scaleLabel: {
                                display: false,
                            },
                            ticks: {
                                major: {
                                    fontStyle: 'bold',
                                    fontColor: '#FF0000'
                                }
                            }

                        }],
                        yAxes: [{
                            display: true,
                            scaleLabel: {
                                display: true,
                                labelString: 'Seconds'
                            },
                            ticks: {

                            }
                        }]
                    }
                },
            };

            var tempChart = new Chart(tempCtx, temperatureConfig);
            var humidChart = new Chart(humidityCtx, humidityConfig);

        }
    });

    $.ajax({
        type: "POST",
        url: "API/cycleTimeRatios",
        ContentType: "application/json",
        success: function(response) {
            airTime = response['air_time'];
            DrainTime = response['drain_time'];
            fillTime = response['fill_time'];
            var doughnutConfig = {
                type: 'doughnut',
                data: {
                    datasets: [{
                        data: [
                            fillTime,DrainTime,airTime,
                        ],
                        backgroundColor: [
                            '#4C959F','#FF8278','#5cc36e'
                        ],
                        label: 'Dataset 1',
                        borderColor: backgroundColor,
                        borderWidth: 10,
                    }],
                    labels: [
                        'Watering',
                        'Draining',
                        'Airrate'
                    ]
                },
                options: {
                    responsive: true,
                    legend: {
                        display: false
                    },
                    title: {
                        display: false
                    },
                    animation: {
                        animateScale: true,
                        animateRotate: true
                    },
                    rotation: -0.8 * Math.PI,
                }
            };

        var doughnutCtx = document.getElementById('doughnut-chart').getContext('2d');
        window.myDoughnut = new Chart(doughnutCtx, doughnutConfig);
        }
    });
}

function passwordKeyUps() {
    $('#password').keypress(function(e) {
        console.log('23');
        if (e.which == 13) {
            updateCycleSettings();
            return;
        }
        return;
    });
}