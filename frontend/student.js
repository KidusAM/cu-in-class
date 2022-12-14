
const urlParams = new URLSearchParams(window.location.search)

let class_id = urlParams.get('class_id')
let student_id = urlParams.get('student_id')


const api_endpoint = "https://tiaa5tbuqi.execute-api.us-east-1.amazonaws.com/v1"

$(document).ready(function (){
    console.log("Document ready")
    if (!class_id || !class_id.length) {
        $("body").html("class_id not specified in URL")
        return
    }
    if (!student_id || !student_id.length) {
        $("body").html("student_id not specified in URL")
        return
    }

    $('#submit-question').click(function () {
        submit_question_endpoint = api_endpoint + "/post_question"
        const question_text = $("#ask-question-text").val()
        const args = {
            "class_id" : class_id,
            "student_id" : student_id,
            "question_text" : question_text
        }

        $.ajax({
            type: "POST",
            url: submit_question_endpoint,
            dataType: "json",
            contentType: "application/json; charset=utf-8",
            data: JSON.stringify(args),
            success: function(result) {
                console.log("Got results", result)
                $("#submit-question-success").html("Question submitted successfully")
                $("#submit-question-success").show()
                $("#submit-question-failure").hide()
            },
            error: function(request, status, error) {
                $("#submit-question-success").hide()
                $("#submit-question-failure").html("Question failed to submit")
                $("#submit-question-failure").show()
                console.log("Error: ")
                console.log(request)
                console.log(status)
                console.log(error)
            }
        })
    })
    $("#submit-question-failure").hide()
    $("#submit-question-success").hide()

    get_questions()

})
