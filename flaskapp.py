from flask import Flask, render_template, url_for, request, redirect, flash
from forms import RegistrationForm
from irc_register import ircregister
import os

app = Flask(__name__)

# to prevent CSRF attacks
# KEEP SECRET
app.config["SECRET_KEY"] = os.getenv("FLASK_CSRF_SECRET_KEY")
webchat_url = os.getenv("WEBCHAT_URL")
home_url = os.getenv("HOME_URL")

# getting the remote ip of user can be highly specific to your environment
# https://stackoverflow.com/questions/3759981/get-ip-address-of-visitors-using-flask-for-python

user_ip = request.environ.get("HTTP_X_REAL_IP", request.remote_addr)

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if request.method == "POST":
        userip = user_ip
        username = request.form.get("username")
        password = request.form.get("password")

        response = ircregister(userip, username, password)
        if response == "disconnected":
            flash("Server Unavailable")
        elif response == "WebIRC bad password":
            flash("Bad Config. Please contact server administrators")
        elif response == "ERR_ERRONEUSNICKNAME":  # shouldn't happen if sanitized in the form
            flash("Illegal Character in Username. Please choose a different one one.")
        elif response == "ERR_NICKNAMEINUSE":
            flash("Username already taken. Please choose a different one!")
        elif response == "CAP_REFUSED":
            flash("This IRCd doesn't support the draft/account-registration capability")
            return redirect(webchat_url)
        elif response == "SUCCESS":
            return redirect(webchat_url)
        else:
            return redirect(home_url)
    elif request.method == "GET":
        return render_template('register.xhtml', title='Register', form=form)



if __name__ == '__main__':
    app.run(debug=True)