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










let template_system_message = "You are a programming tutor. Your answers are short and simple, around 1-5 sentences."

                let initial_system_message = template_system_message.replace("[[code]]", "")
                let llm_messages = [{ "role": "system", "content": "You are a programming tutor. Your answers are short and simple, around 1-5 sentences." }]

                let solution_lines = [];
                let lines_index = 0;
                let indent = "";

                function get_whole_solution() {

                    let user_code = get_user_code();
                    let init_button_text = $("#full-solution-button")[0].innerHTML 
                    $("#full-solution-button")[0].innerHTML = '<img class="llm-button-loader" src="/static/spin-load.gif">';

                    $.ajax({

                        type: 'POST',
                        url: "/llm/solution_lines/{{ course_basics['id'] }}/{{ assignment_basics['id'] }}/{{ exercise_basics['id'] }}",
                        data: { "user code": user_code },
                        async: true


                    }).done(result => {
                        
                        hideInfoMessage();
                        
                        if (result.reason == "no comments") {
                            showInfoMessage("Could not find comment");
                            $("#full-solution-button")[0].innerHTML = init_button_text;
                            return;
                        }


                        let new_editor_value = editor.getValue()
                        result.lines.forEach(line => {
                            new_editor_value += "\n" + line;
                        })
                        
                        editor.setValue( new_editor_value );
                        editor.clearSelection();
                        

                        $("#full-solution-button")[0].innerHTML = init_button_text;
                    })



                }

                function get_solution_by_lines() {

                    let user_code = get_user_code();
                    let init_button_html = $("#lines-solution-button")[0].innerHTML
                    
                    $("#lines-solution-button")[0].innerHTML = '<img class="llm-button-loader" src="/static/spin-load.gif">';


                    $.ajax({

                        type: 'POST',
                        url: "/llm/solution_lines/{{ course_basics['id'] }}/{{ assignment_basics['id'] }}/{{ exercise_basics['id'] }}",
                        data: { "user code": user_code },
                        async: true

                    }).done(result => {

                        //solution_lines = result

                        hideInfoMessage();
                        
                        if (result.reason == "no comments") {
                            showInfoMessage("Could not find comment");
                            console.log(init_button_html);
                            $("#lines-solution-button")[0].innerHTML = init_button_html;
                            return;
                        }
                        
                        
                        console.log(result);

                        solution_lines = result.lines;
                        lines_index = 0;
                        indent = result.initial_indent;

                        active_solution_id = result.llm_generation_id;

                        $("#lines-solution-button")[0].innerHTML = init_button_html;

                        $("#next-line-button").attr("disabled", false);
                        show_next_line();
                    })


                }

                function show_next_line() {

                    let next_line = solution_lines[lines_index]
                    lines_index += 1

                    
                    // TODO: detect when console has been edited
                    
                    
                    // If the line is only whitespace, give it and the next non whitespace line
                    /*
                    let next_line_output = next_line
                    while (next_line.trim() === "") {
                        lines_index += 1
                        let next_line = solution_lines[lines_index]
                        next_line_output += "\n" + next_line
                    }
                    */
                    
                    console.log(next_line)
                    
                    ace_edited_by_llm_counter = 2;

                    let cur_editor_text = editor.getValue()
                   
                    editor.setValue( cur_editor_text + "\n" + indent + next_line )
                    editor.clearSelection();
                    
                    if (lines_index == solution_lines.length-1) {
                        
                        update_llm_lines_used()
                        
                        solution_lines = [];
                        lines_index = 0;

                        $("#next-line-button").attr("disabled", true);
                    }


                }

                function update_llm_lines_used() {