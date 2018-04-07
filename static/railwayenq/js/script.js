$(document).ready(function () {

    var loader = $('.loader');
    loader.hide();

    var baseUrl = "https://api.railwayapi.com/v2/";

    var apiKey = "rqjexumspi";
    var $input = $("#trainInput");
    var submitBtn = $("#submitBtn");
    var $result = $("#result");
    $result.hide();
    var $error = $("#result-error");
    $error.hide();
    submitBtn.on("click", function () {
        var data = $input.val();
        $error.hide();
        $result.hide();
        $input.val("");
        console.log(data);

        var now = moment().format("DD-MM-YYYY");
        loader.show();

        //var url = baseUrl + "live/train/" + data + "/date/" + now + "/apikey/" + apiKey;
        var url = "http://localhost:8000/api/railway-enquiry/status/"+data+"/";
        console.log(url);

        var settings = {
            "async": true,
            "crossDomain": true,
            "url": url,
            "method": "GET"
        };

        $.ajax(settings).done(function (response) {
            console.log(response);
            loader.hide();
            if (response.position) {
                $("#position-value").text(response.position);
                $("#start-date-value").text(response.start_date);
                $("#station-value").text(response.current_station);
                $("#name-value").text(response.name);
                $("#number-value").text(response.number);
                $result.show();

            } else {
                $error.show();
            }

        }).fail(function () {
            loader.hide();
            $error.show();
        });

    });




});
