
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
            // console.log("Got results", result)
            fill_questions(result)
        },
        error: function(request, status, error) {
            console.log("Error: ")
            console.log(request)
            console.log(status)
            console.log(error)
        },
        complete: function() {
            setTimeout(get_questions, 5000)
        }
    })
}

