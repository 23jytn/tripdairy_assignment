$(document).ready(function () {

    // hide elements initially
    var $loader = $('.loader');
    var $result = $("#result");
    var $error = $("#result-error");
    reset();
    
    // Initialize Date picker with min and max date
    $('#date-picker').datepicker({
        uiLibrary: 'bootstrap4',
        minDate: moment().subtract(2, 'days').toDate(),
        maxDate: moment().add(2, 'months').toDate(),
        format: 'dd-mm-yyyy'
    });

    // Get Form Input Field
    var trainInput = $("#train-input");
    var dateInput = $("#date-picker");
    var srcInput = $("#source-input");
    var destInput = $("#destination-input");


    // Submit Btn
    var enqBtn = $("#enquiry-btn");
    var seatBtn = $("#seat-btn");


    var baseUrl = "http://localhost:8000/api/railway-enquiry/";

    // click handler for train status btn
    enqBtn.on("click", function() {

        reset();

        // get input data
        var trainNumber = trainInput.val();
        var travelDate = dateInput.val();

        var valid = true;
        
        // validation logic
        if (!(new RegExp($(trainInput).attr("pattern")).test(trainNumber))) {
            alert("Please enter valid train number");
            valid = false;
        }
        if (valid && !(new RegExp($(dateInput).attr("pattern")).test(travelDate))) {
            alert("Please enter valid date of travel");
            valid = false;
        }

        if(valid) {
            var url = baseUrl + trainNumber + "/?type=train-status";
            url += "&date=" + travelDate;

            callApi(url);

            console.log(url);
        }
     

    });

    // click handler for seat enquiry btn
    seatBtn.on("click", function() {

        reset();
        // get train input data

        // get input data
        var trainNumber = trainInput.val();
        var travelDate = dateInput.val();
        var srcStation = srcInput.val();
        var destStation = destInput.val();

        var valid = true;

        // validation logic
        if (!(new RegExp($(trainInput).attr("pattern")).test(trainNumber))) {
            alert("Please enter valid train number");
            valid = false;
        }
        if (valid && !(new RegExp($(dateInput).attr("pattern")).test(travelDate))) {
            alert("Please enter valid date of travel");
            valid = false;
        }
        if (valid && !(new RegExp($(srcInput).attr("pattern")).test(srcStation))) {
            alert("Please enter valid source station");
            valid = false;
        }
        if (valid && !(new RegExp($(destInput).attr("pattern")).test(destStation))) {
            alert("Please enter valid destination station");
            valid = false;
        }

        if (valid) {
            var url = baseUrl + trainNumber + "/?type=seat-enquiry";
            url += "&date=" + travelDate + "&src="+srcStation +"&dest="+destStation;

            callApi(url);

            console.log(url);
        }


    });
    

    function callApi(url) {
        $loader.show();
        $.getJSON(url)
            .done(function (response) {
                showResult(response)
            })
            .fail(function (jqXHR) {
                showError(jqXHR.responseJSON);
            })
            .always(function () {
                $loader.hide();
            });
    }

    function reset(){
        $loader.hide();
        $result.hide();
        $error.hide();

        $(".result-box").empty();
        $(".error-msg").empty();

    }

    function showResult(response) {
        console.log(response);

        var container = $(".result-box");

        $.each(response, function (key, value) {
            var title = key.replace(/_/g, " ").toUpperCase();
            
            container.append("<li class='list-group-item'>" + title + " : <span class='font-weight-bold'>" + value + "</span></li>");
        });

        $result.show();
    }

    function showError(error) {
        console.log(error);
        var container = $(".error-msg");
        container.append("<p>" + error.msg +"</p>")
        $error.show();
    }

});