import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
# Import flask_pymongo -
# Note the underscore, rather than hyphen in the install.
from flask_pymongo import PyMongo
# So we can find bson objects from MongoDB
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash


# We need to import env.py, but because env.py wont
# exist on Heroku, we must check if it exists first.
# That way the program wont crash when looking for it on heroku.
# Heroku will have these variables set internally
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

# Get the MONGO DBNAME
app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
# Get the MONGO URI OR CONNECTION STRING
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
# Get the Secret Key, which is required for some of flask.
app.secret_key = os.environ.get("MONGO_DBNAME")

# Setup an instance of PyMongo, and add the app into that
# Using a constructor method
mongo = PyMongo(app)


# Test function to check our setup
# "/" refers to the default route
@app.route("/")
@app.route("/get_tasks")
def get_tasks():
    # Find all documents from the tasks collection
    tasks = mongo.db.tasks.find()
    return render_template("tasks.html", tasks=tasks)
    # first tasks is a new variable we pass to the html
    # equal to the above tasks.


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # CHECK TO SEE IF USER ALREADY EXISTS IN MONGO DB
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            # IF USER ALREADY EXISTS IN DB
            # REDIRECT BACK TO REGISTER PAGE
            flash("Username already exists")
            return redirect(url_for("register"))

        password = request.form.get("password")
        check = request.form.get("password-check")

        if password != check:
            flash("Passwords do not match!")
            return redirect(url_for("register"))

        # GATHER THE DATA FROM THE FORM
        # ACTS AS AN IF STATEMENT
        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password"))
        }
        # INSERT THE ABOVE DICTIONARY
        mongo.db.users.insert_one(register)

        # PUT THE NEW USER INTO 'SESSION' COOKIE
        session["user"] = request.form.get("username").lower()
        flash("Registration Successful!")

    return render_template("register.html")


# Tell our app, how and where to run our application
if __name__ == "__main__":
    # set the host to the default ip set in env.py
    app.run(host=os.environ.get("IP"),
            # convert the port to an int
            port=int(os.environ.get("PORT")),
            # set this to False at end of development stage
            debug=True)
