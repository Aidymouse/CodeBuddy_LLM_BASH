from BaseUserHandler import *
import datetime as dt

class ViewAssignmentScoresHandler(BaseUserHandler):
    def get(self, course, assignment):
        try:
            if self.is_administrator or self.is_instructor_for_course(course) or self.is_assistant_for_course(course):
                course_basics = self.get_course_basics(course)
                assignment_basics = self.content.get_assignment_basics(course_basics, assignment)

                self.render("view_assignment_scores.html", courses=self.courses, course_basics=course_basics, assignments=self.content.get_assignments(course_basics), assignment_basics=assignment_basics, assignment_details=self.get_assignment_details(course_basics, assignment), exercise_statuses=self.content.get_exercise_statuses(course, assignment, self.get_current_user()), scores=self.content.get_assignment_scores(course_basics, assignment_basics), have_timers_expired=self.content.get_all_user_assignment_expired(course, assignment), curr_datetime=dt.datetime.utcnow(), download_file_name=get_scores_download_file_name(assignment_basics), user_info=self.user_info, is_administrator=self.is_administrator)
            else:
                self.render("permissions.html")
        except Exception as inst:
            render_error(self, traceback.format_exc())