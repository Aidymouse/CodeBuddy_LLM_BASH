from BaseUserHandler import *
from datetime import datetime, timedelta

import openai

class LLMHandler(BaseUserHandler):
    #entrypoint = 'llm_chat'

    '''
    def __init__(self):

        initial_system_message = "You are a programming tutor. Your answers are short and simple, around 1-5 sentences."

        self.messages = [{ "role": "system", "content": initial_system_message }]
    
        openai.api_key = self.application.settings["openai_api_key"];
    '''

    async def get_solution_lines(self, course_id, assignment_id, exercise_id):
        user_code = self.get_body_argument("user code")

        course_basics = await self.get_course_basics(course_id)
        assignment_basics = await self.get_assignment_basics(course_basics, assignment_id)
        exercise_details = await self.get_exercise_details(course_basics, assignment_basics, exercise_id)

        exercise_instructions = exercise_details["instructions"]


        user_code_lines = user_code.split("\n")

        line_index_start = -1
        line_index_end = -1

        COMMENT_CHAR = "//"

        try:

            # Get latest contiguous block of comments that start with designated comment character

            for i in range(len(user_code_lines)-1, -1, -1):
                line = user_code_lines[i]
                
                # Does line start with comment character?
                if line.strip()[:len(COMMENT_CHAR)] == COMMENT_CHAR:
                    print(f"{i}. {line}")

                    if line_index_end != -1:
                        line_index_start = i
                        break
                    else:
                        line_index_end = i


            if line_index_end == -1:
                print("No comments!")
                return {
                    "full_solution": "",
                    "lines": [],
                    "initial_indent": "",
                    "reason": "no comments"
                }
            
            if line_index_start == -1:
                line_index_start = line_index_end

            full_comment = user_code_lines[line_index_start:line_index_end+1]

            # Turn comment into prompt for the model
            comments = " ".join([c.strip()[len(COMMENT_CHAR):].strip() for c in full_comment])

            template_system_message = "You write C programs. You only provide code. You write at most one function, including main."

            prompt = template_system_message + " " + comments

            print(f"Asking: {prompt}")

            messages_from_comment = [{"role": "user", "content": prompt}]

            chat_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages_from_comment)

            message = chat_completion.choices[0].message.content
            print(f"Response: {message}")

            initial_indent = full_comment[0].split(COMMENT_CHAR)[0]


            full_solution = message.split("```")[1]

            self.content.save_llm_generation(course_id, assignment_id, exercise_id, self.get_current_user(), comments, full_solution, exercise_details["llm_interaction_type"])

            return {
                "full_solution": full_solution,
                "lines": full_solution.split("\n")[1:],
                "initial_indent": initial_indent,
                "reason": ""
            }

        except Exception as e:
            print(e)
            return ""

        '''
        message_text = f"The exercise is ${exercise_instructions}. The current code is \"{user_code}\". What is a reasonable next line of code?"
        
        messages = [{"role": "user", "content": message_text}]

        try:
            chat_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
        except Exception as e:
            print(e)

        self.application.messages.append(chat_completion.choices[0].message)

        self.write(chat_completion.choices[0].message.content)
        '''




    def chat_message(self):
        pass

    async def next_line(self, course_id, assignment_id, exercise_id):
        print(":::Next Line:::")

        user_code = self.get_body_argument("user code")

        course_basics = await self.get_course_basics(course_id)
        assignment_basics = await self.get_assignment_basics(course_basics, assignment_id)
        exercise_details = await self.get_exercise_details(course_basics, assignment_basics, exercise_id)

        exercise_instructions = exercise_details["instructions"]

        message_text = f"The exercise is ${exercise_instructions}. The current code is \"{user_code}\". What is a reasonable next line of code?"
        
        messages = [{"role": "user", "content": message_text}]

        try:
            chat_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
        except Exception as e:
            print(e)

        self.application.messages.append(chat_completion.choices[0].message)

        self.write(chat_completion.choices[0].message.content)


    async def whats_useful(self, course_id, assignment_id, exercise_id):
        print(":::Whats Useful:::")

        user_code = self.get_body_argument("user code")

        course_basics = await self.get_course_basics(course_id)
        assignment_basics = await self.get_assignment_basics(course_basics, assignment_id)
        exercise_details = await self.get_exercise_details(course_basics, assignment_basics, exercise_id)

        exercise_instructions = exercise_details["instructions"]

        message_text = f"The exercise is ${exercise_instructions}. The current code is \"{user_code}\". What is useful code component to solve this problem?"
        
        messages = [{"role": "user", "content": message_text}]

        try:
            chat_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
        except Exception as e:
            print(e)

        self.application.messages.append(chat_completion.choices[0].message)

        self.write(chat_completion.choices[0].message.content)


    async def post(self, message_type, course_id, assignment_id, exercise_id):

        openai.api_key = self.application.settings["openai_api_key"]
        
        print(f"Contacting LLM: {message_type}")

        if message_type == "solution_lines":
            user_code = await self.get_solution_lines(course_id, assignment_id, exercise_id)

            self.write(user_code)

        elif message_type == "chat":
            
            print(":::Chat Message:::")

            chat_input = self.get_body_argument("chat_input")
            print(f"Chat Message: {chat_input}")

            self.application.messages.append()


            try:
                chat_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=self.application.messages)
            except Exception as e:
                print(e)

            print(f"ChatGPT Response: {chat_completion.choices[0].message.content}")

            self.application.messages.append(chat_completion.choices[0].message)

            self.write(chat_completion.choices[0].message.content);
    
        elif message_type == "next_line":
            self.next_line(course_id, assignment_id, exercise_id)

        elif message_type == "whats_useful":
            await self.whats_useful(course_id, assignment_id, exercise_id)

        elif message_type == "natural_hint":

            print(":::Natural Hint:::")

            user_code = self.get_body_argument("user code");

            course_basics = await self.get_course_basics(course_id)
            assignment_basics = await self.get_assignment_basics(course_basics, assignment_id)
            exercise_details = await self.get_exercise_details(course_basics, assignment_basics, exercise_id)

            exercise_instructions = exercise_details["instructions"]

            message_text = f"The exercise is {exercise_instructions}. The current code is \"{user_code}\". Without providing code, give a hint for the next step in creating a complete solution."

            messages = [{"role": "user", "content": message_text}]

            try:
                chat_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
            except Exception as e:
                print(e)

            self.application.messages.append(chat_completion.choices[0].message)

            self.write(chat_completion.choices[0].message.content)