from BaseOtherHandler import *
from content import *
from tornado.web import *

class FirebaseLoginHandler(BaseOtherHandler):

    async def post(self):
        try:
            #user_id = self.get_body_argument("user_id")
            #dev_password = self.get_body_argument("dev_password")

            email = self.get_body_argument("email")
            UPI = email.split("@")[0]
            print(UPI)
            
            # Ensure the email is a UoA one
            if email.split("@")[1] != "aucklanduni.ac.nz":
                self.write("Please use a valid university of auckland email")
                return;

            full_name = self.get_body_argument("name")

            first_name = full_name.split(" ")[0]
            last_name = full_name.split(" ")[1]

            user_dict = {'name': full_name, 'given_name': first_name, 'family_name': last_name, 'locale': 'en', 'email_address': email}

            if self.content.user_exists(UPI):
                # Update user with current information when they already exist.
                self.content.update_user(UPI, user_dict)
            else:
                # Store current user information when they do not already exist.
                self.content.add_user(UPI, user_dict)

            self.set_secure_cookie("user_id", UPI, expires_days=30)

            redirect_path = self.get_secure_cookie("redirect_path")
            self.clear_cookie("redirect_path")
            if not redirect_path:
                redirect_path = "/"
            self.redirect(redirect_path)

        except Exception as inst:
            print(inst)
            render_error(self, traceback.format_exc())