
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

let class_id = 'IoT'

const api_endpoint = "https://tiaa5tbuqi.execute-api.us-east-1.amazonaws.com/v1"

function make_question(question) {
    const card = $("<div class='row question-container'>")
    const question_user = $("<div class='col-3 question-user'>")
    const question_text = $("<div class='col-8 question-text'>")
    const question_votes = $("<div class='col-1 question-votes'>")

    question_user.html(question.student_id)
    question_text.html(question.question_text)
    question_votes.html("")

    card.append(question_user, question_text, question_votes)

    return card
}

function fill_questions(questions) {
    $("#questions-container").empty()
    $.each(questions, function (i, question) {
        $("#questions-container").append(make_question(question))
    })
}

function fill_attendances(attendances) {
    $("#attendance-container").empty()
    $.each(attendances, function(uni, is_present) {
        $("#attendance-container").append($("<div>").html(uni + ':' + is_present))
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
            console.log("Got results", result)
            fill_attendances(result)
        },
        error: function(request, status, error) {
            console.log("Error: ")
            console.log(request)
            console.log(status)
            console.log(error)
        }
    })
}

function get_questions() {
    const questions_endpoint = api_endpoint + "/get_questions"
    const args = { "class_id" : class_id }
    $.ajax({
        type: "GET",
        url: questions_endpoint,
        dataType: "json",
        contentType: "application/json; charset=utf-8",
        data: args,
        success: function(result) {
            console.log("Got results", result)
            fill_questions(result)
        },
        error: function(request, status, error) {
            console.log("Error: ")
            console.log(request)
            console.log(status)
            console.log(error)
        }
    })
}

$(document).ready(function (){
    console.log("Document ready")

    fill_questions(questions)
    fill_attendances(attendances)

    get_attendances()
    get_questions()
})
