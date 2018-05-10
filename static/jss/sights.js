"use strict";

function showOrderResults(result) {
    alert(result);
}

function showSights(evt) {
    evt.preventDefault();

    var formInputs = {
        "type": $("#type-field").val(),
        "amount": $("#amount-field").val(),
    };

    $.post("/new-order", 
           formInputs,
           showOrderResults);
}

$("#sights").on("submit", showSights);