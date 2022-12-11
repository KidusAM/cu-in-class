
const questions = {
    "q1key" : {
        "question_text" : "What does the 'o' in IoT stand for?",
        "student_id" : "km3533"
    },
    "q2key" : {
        "question_text" : "What is the worst development board, and why is it the ESP8266?",
        "student_id" : "km3533"

    }
}

const attendances = {
    "km3533" : 0,
    "mdg1249" : 1,
    "sd2124" : 1
}

const urlParams = new URLSearchParams(window.location.search)

let class_id = urlParams.get('class_id')

const api_endpoint = "https://tiaa5tbuqi.execute-api.us-east-1.amazonaws.com/v1"


function fill_attendances(attendances) {
    $("#attendance-container").empty()
    $.each(attendances, function(uni, is_present) {
        const container_row = $("<div class='row'>")
        container_row.append($("<div class='col-8'>").html(uni))
        container_row.append($("<div class='col-4'>").html(is_present))
        $("#attendance-container").append(container_row)
    })
}

function get_attendances() {
    const attendances_endpoint = api_endpoint + "/get_attendances"
    const args = { "class_id" : class_id }
    $.ajax({
        type: "GET",
        url: attendances_endpoint,
        dataType: "json",
        contentType: "application/json; charset=utf-8",
        data: args,
        success: function(result) {
            // console.log("Got results", result)
            fill_attendances(result)
        },
        error: function(request, status, error) {
            console.log("Error: ")
            console.log(request)
            console.log(status)
            console.log(error)
        },
        complete: function() {
            setTimeout(get_attendances, 5000)
        }
    })
}

$(document).ready(function (){
    console.log("Document ready")
    if (!class_id || !class_id.length) {
        $("body").html("Class id not specified")
        return
    }

    fill_questions(questions)
    fill_attendances(attendances)

    get_attendances()
    get_questions()
})
