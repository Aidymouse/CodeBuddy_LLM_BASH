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
        
        if message_type == "chat":
            
            print(":::Chat Message:::")

            chat_input = self.get_body_argument("chat_input")
            print(f"Chat Message: {chat_input}")

            self.application.messages.append({ "role": "user", "content": chat_input })


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