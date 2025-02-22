from BaseUserHandler import *

class ImportAssignmentHandler(BaseUserHandler):
    async def post(self, course_id):
        result = ""

        try:
            course_basics = await self.get_course_basics(course_id)

            if not course_basics["exists"]:
                return self.write(f"Error: The specified course ID ({course_id}) is invalid.")

            file_text = self.get_body_argument("file_text")
            # This package is needed because the base json package does not escape HTML characters.
            assignment_dict = ujson.loads(file_text)

            for x in ["basics", "details", "exercises"]:
                if x not in assignment_dict:
                    return self.write(f"Error: The contents of the uploaded file are invalid ({x} is missing at level 1).")

            assignment_basics = assignment_dict["basics"]
            assignment_details = assignment_dict["details"]

            # Make sure assignment with that title doesn't already exist.
            if self.content.has_duplicate_title(self.content.get_assignments(course_basics), None, assignment_basics["title"]):
                return self.write("Error: An assignment with that title already exists.")

            for exercise_title in assignment_dict["exercises"]:
                for x in ["basics", "details"]:
                    if x not in assignment_dict:
                        return self.write(f"Error: The contents of the uploaded file are invalid ({x} is missing at level 2).")

            assignment_basics["exists"] = False
            assignment_basics["course"] = {"id": course_id}
            assignment_id = self.content.save_assignment(assignment_basics, assignment_details)
            assignment_basics["id"] = assignment_id

            for exercise_title in assignment_dict["exercises"]:
                exercise_basics = assignment_dict["exercises"][exercise_title]["basics"]
                exercise_details = assignment_dict["exercises"][exercise_title]["details"]
                exercise_basics["exists"] = False
                exercise_basics["assignment"] = assignment_basics

                self.content.save_exercise(exercise_basics, exercise_details)
        except Exception as inst:
            self.write(f"Error: {traceback.format_exc()}")