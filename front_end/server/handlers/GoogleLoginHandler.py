#from BaseOtherHandler import *
from tornado.web import *
from tornado.auth import GoogleOAuth2Mixin
from content import *

#class GoogleLoginHandler(BaseOtherHandler, GoogleOAuth2Mixin):
class GoogleLoginHandler(RequestHandler, GoogleOAuth2Mixin):
    def prepare(self):
        self.settings_dict = load_yaml_dict(read_file("../Settings.yaml"))
        self.content = Content(self.settings_dict)

    async def get(self):
        try:
            redirect_uri = f"https://{self.settings_dict['domain']}/googlelogin"

            # Examples: https://www.programcreek.com/python/example/95028/tornado.auth
            if self.get_argument('code', False):
                user_dict = await self.get_authenticated_user(redirect_uri = redirect_uri, code = self.get_argument('code'))

                if user_dict:
                    response = urllib.request.urlopen(f"https://www.googleapis.com/oauth2/v1/userinfo?access_token={user_dict['access_token']}").read()

                    if response:
                        user_dict = json.loads(response.decode('utf-8'))
                        user_id = user_dict["email"].split("@")[0]
                        user_dict["email_address"] = user_dict["email"]

                        if self.content.user_exists(user_id):
                            # Update user with current information when they already exist.
                            self.content.update_user(user_id, user_dict)
                        else:
                            # Store current user information when they do not already exist.
                            self.content.add_user(user_id, user_dict)

                        self.set_secure_cookie("user_id", user_id, expires_days=30)

                        redirect_path = self.get_secure_cookie("redirect_path")
                        self.clear_cookie("redirect_path")
                        if not redirect_path:
                            redirect_path = "/"
                        self.redirect(redirect_path)
                    else:
                        self.clear_all_cookies()
                        render_error(self, "Google account information could not be retrieved.")
                else:
                    self.clear_all_cookies()
                    render_error(self, "Google authentication failed. Your account could not be authenticated.")
            else:
                await self.authorize_redirect(
                    redirect_uri = redirect_uri,
                    client_id = self.settings['google_oauth']['key'],
                    scope = ['profile', 'email'],
                    response_type = 'code',
                    extra_params = {'approval_prompt': 'auto'})
        except Exception as inst:
            render_error(self, traceback.format_exc())