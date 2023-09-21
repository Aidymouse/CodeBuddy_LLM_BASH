from BaseUserHandler import *
from datetime import datetime, timedelta

import openai
import re

class LLMHandler(BaseUserHandler):
    #entrypoint = llm

    async def post(self, action, course_id, assignment_id, exercise_id):

        try:
            print(action)

            if action == "generate":
                await self.generate(course_id, assignment_id, exercise_id, 1.2, "generate")
            
            elif action == "retry":
                await self.generate(course_id, assignment_id, exercise_id, 1.4, "retry")

        except Exception as e:
            print(e)


    async def generate(self, course_id, assignment_id, exercise_id, model_temperature, gen_method):
        template_prompt = '''You are a programming assistant that provides C code to beginner programmers. Don't generate more than one code statement.

The problem description is: [[problem_description]]

The provided code is:
[[provided_code]]

Provide code that, when replacing the token marked "CURSOR", completes only the next line. If the provided code completely solves the problem description, provide a short code comment saying so. If the line contains an error other than being incomplete, provide a short comment describing why the line is wrong, followed by the next line of code that helps amend the error. Ignore the CURSOR token when considering if the code is correct. Do not refer to the CURSOR token in comments. Anything you provide that isn't code should be commented out.'''

        #print("Gamer")

        openai.api_key = self.settings["openai_api_key"]
        openai.organization = self.settings["openai_org_id"]

        try:
            user_code = self.get_body_argument("user_code")
            #print(user_code)

            cursor_row = int(self.get_body_argument("cursor_row"))
            cursor_col = int(self.get_body_argument("cursor_column"))

            print(f"Cursor: (row {cursor_row}, col {cursor_col})")

            user_code_lines = re.split("\n", user_code)
            print(user_code_lines)
            #user_code.split("\n")

            # White space not retained on last line if it's only whitespace, but cursor position is correct, so we can fake it
            while cursor_row >= len(user_code_lines)-1:
                user_code_lines.append("".join([" " for i in range(cursor_col)]))
                #cursor_row = len(user_code_lines)
            
            if cursor_col > len(user_code_lines[cursor_row]):
                spaces_to_add = cursor_col - len(user_code_lines[cursor_row])
                user_code_lines[cursor_row] += "".join([" " for i in range(spaces_to_add)])
            
            print(user_code_lines)

            cursor_line = user_code_lines[cursor_row]
            
            '''
            
            # White space is lost at the end of a line
            '''

            print(f"Cursor Pos: {cursor_row}, {cursor_col}")
            print(f"Cursor Line: {cursor_line}")

            co = 1
            co += 1

            # Assemble User Code with CURSOR token
            ammended_user_code = "\n".join(user_code_lines[:cursor_row]) 
            print("===1===")
            print(ammended_user_code)
            
            ammended_user_code += "\n" + cursor_line[:cursor_col] + "CURSOR" + cursor_line[cursor_col:] + "\n"
            print("===2===")
            print(ammended_user_code)
            

            # Append a last line 
            if cursor_row != len(user_code_lines)-1:
                ammended_user_code += "\n".join(user_code_lines[cursor_row+1:])
                print("===3===")
                print(ammended_user_code)


            # Get instruction text
            course_basics = await self.get_course_basics(course_id)
            assignment_basics = self.content.get_assignment_basics(course_basics, assignment_id)
            exercise_details = await self.get_exercise_details(course_basics, assignment_basics, exercise_id)

            # Assemble final prompt
            prompt = template_prompt.replace("[[problem_description]]", exercise_details['instructions']).replace("[[provided_code]]", ammended_user_code)

            print("===Prompt===")
            print(prompt)

            # Call Model
            messages = [{"role": "user", "content": prompt}]
            c = openai.ChatCompletion.create(model="gpt-4", temperature=model_temperature, messages=messages, max_tokens=500)
            generated_code = c.choices[0].message.content

            try:
                print(ammended_user_code)
                print(co)
                self.content.save_llm_generation(course_id, assignment_id, exercise_id, self.get_current_user(), generated_code, ammended_user_code, gen_method)
            except Exception as e:
                print(e)
                self.write({
                    "status": "DB failed",
                    "generated_code": "" 
                })
                return

            self.write({
                "status": "success",
                "generated_code": generated_code,
            })

        except Exception as e:
            print(e)

            self.write({
                "status": "failed",
                "generated_code": ""
            })

    


        