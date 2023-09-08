/* old functions once used in exercise_llm.html template */

function submit_to_llm() {

    if ($("#chat-input").val() == "") return;

    console.log("Contacting LLM")

    console.log("{{course_basics['id']}}")

    let chat_input = $("#chat-input").val();
    $("#chat-history").html($("#chat-history").html() + `<div class="chat-message" id="user-message">${chat_input}</div>`);

    $("#chat-input").val("");

    $.ajax({
        type: 'POST',
        url: "/llm_chat/chat/{{ course_basics['id'] }}/{{ assignment_basics['id'] }}/{{ exercise_basics['id'] }}",
        data: { "chat_input": chat_input },
        async: true
    }).done(result => {
        let response_message = result

        // Update html to match
        $("#chat-history").html($("#chat-history").html() + `<div class="chat-message" id="llm-message">${response_message}</div>`);

    })


    return;


}

function whats_useful_llm() {

    let user_code = get_user_code();

    $.ajax({
        type: 'POST',
        url: "/llm_chat/whats_useful/{{ course_basics['id'] }}/{{ assignment_basics['id'] }}/{{ exercise_basics['id'] }}",
        data: { "user code": user_code },
        async: true
    }).done(result => {
        console.log(result)

        //llm_messages.push(response_message)

        // Update html to match
        $("#chat-history").html($("#chat-history").html() + `<div class="chat-message" id="llm-message">${result}</div>`);

    })

}

function hint_llm() {

    let user_code = get_user_code();

    $.ajax({
        type: 'POST',
        url: "/llm_chat/natural_hint/{{ course_basics['id'] }}/{{ assignment_basics['id'] }}/{{ exercise_basics['id'] }}",
        data: { "user code": user_code },
        async: true
    }).done(result => {
        console.log(result)

        //llm_messages.push(response_message)

        // Update html to match
        $("#chat-history").html($("#chat-history").html() + `<div class="chat-message" id="llm-message">${result}</div>`);

    })

}

function next_line_of_code_llm() {

    let user_code = get_user_code()

    $.ajax({
        type: 'POST',
        url: "/llm_chat/next_line/{{ course_basics['id'] }}/{{ assignment_basics['id'] }}/{{ exercise_basics['id'] }}",
        data: { "user code": user_code },
        async: true
    }).done(result => {
        console.log(result)

        //llm_messages.push(response_message)

        // Update html to match
        $("#chat-history").html($("#chat-history").html() + `<div class="chat-message" id="llm-message">${result}</div>`);

    })

}