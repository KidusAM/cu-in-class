
const questions = [
    {
        "question" : "What does the 'o' in IoT stand for?",
        "votes" : 12,
        "user" : "km3533"
    },
    {
        "question" : "What is the worst development board, and why is it the ESP8266?",
        "votes" : 21,
        "user" : "km3533"

    }
]

const attendances = {
    "km3533" : 0,
    "mdg1249" : 1,
    "sd2124" : 1
}

function make_question(question) {
    const card = $("<div class='row question-container'>")
    const question_user = $("<div class='col-3 question-user'>")
    const question_text = $("<div class='col-8 question-text'>")
    const question_votes = $("<div class='col-1 question-votes'>")

    question_user.html(question.user)
    question_text.html(question.question)
    question_votes.html(question.votes)

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

$(document).ready(function (){
    console.log("Document ready")

    fill_questions(questions)
    fill_attendances(attendances)
})
