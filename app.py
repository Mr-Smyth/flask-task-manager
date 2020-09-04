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
    # ADD = LIST() TO CONVERT RESULT TO A PROPPER LIST
    # THIS ALLOWS JINGA TO UNPACK MULTIPLE TIMES
    tasks = list(mongo.db.tasks.find())
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
        return redirect(url_for("profile", username=session["user"]))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # CHECK IF USERNAME EXISTS IN DB
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            # IF THE USERNAME MATCHES, THEN WE NEED TO MAKE SURE
            # HASHED PASSWORD MATCHES USER ENTERED PASSWORD.
            if check_password_hash(existing_user["password"], request.form.get(
                "password")):
                    session["user"] = request.form.get("username").lower()
                    flash("Welcome, {}".format(
                        request.form.get("username").capitalize()))
                    return redirect(url_for(
                        "profile", username=session["user"]))
            else:
                # ELSE THE PASSWORD IS WRONG
                flash("Incorrect Username and/or Password")
                return redirect(url_for("login"))

        else:
            # ELSE THE USERNAME IS INCORRECT
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    # SETUP THE USERNAME VARIABLE EQUAL TO THE USERNAME
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]
    # return the rendered template, but pass through the username variable
    # the first username is the variable being passed,
    # the second is the one above.
    # SO USERS CANT FORCE THE URL TO SOMEONE ELSES PROFILE, WE ADD AN IF
    if session["user"]:
        return render_template("profile.html", username=username.capitalize())

    return redirect(url_for("login"))


@app.route("/logout")
def logout():
    # REMOVE USER FROM SESSION COOKIES
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for('login'))


@ app.route("/add_task", methods=["GET", "POST"])
def add_task():
    # IF ANY ATTEMPT TO SUBMIT DATA
    if request.method == "POST":
        # LETS FIRST SETUP THE URGENT SELECTION FOR CHECKING
        # USING A TERNARY IF
        is_urgent = "on" if request.form.get("is_urgent") else "off"

        # SETUP OUR DICTIONARY FOR IMPORTING TO MONGO DB
        # note: .getlist can be used instead of .get, for list items
        task = {
            "category_name": request.form.get("category_name"),
            "task_name": request.form.get("task_name"),
            "task_description": request.form.get("task_description"),
            "is_urgent": is_urgent,
            "due_date": request.form.get("due_date"),
            "created_by": session["user"]
        }
        # ADD THE DICT TO MONGO
        mongo.db.tasks.insert_one(task)
        flash("Task Successfully Added")
        return redirect(url_for("get_tasks"))

    # SETUP LINKS TO THE CATEGORIES FOR THE CATEGORY SELECTION
    # SORT THEM BY NAME - ASCENDING ORDER
    categories = mongo.db.categories.find().sort("category_name", 1)
    # RETURN THE ADD_TASK PAGE
    return render_template("add_task.html", categories=categories)


@app.route("/edit_task/<task_id>", methods=["GET", "POST"])
def edit_task(task_id):
    # THIS IS FOR THE EDIT BUTTON
    # AS WE HAVE IMPORTED OBJECTID WHICH ALLOWS US TO
    # RENDER MONGO DOCUMENTS BY THEIR UNIQUE ID.

    if request.method == "POST":
        # LETS FIRST SETUP THE URGENT SELECTION FOR CHECKING
        # USING A TERNARY IF
        is_urgent = "on" if request.form.get("is_urgent") else "off"

        # SETUP OUR DICTIONARY FOR IMPORTING TO MONGO DB
        # note: .getlist can be used instead of .get, for list items
        submit = {
            "category_name": request.form.get("category_name"),
            "task_name": request.form.get("task_name"),
            "task_description": request.form.get("task_description"),
            "is_urgent": is_urgent,
            "due_date": request.form.get("due_date"),
            "created_by": session["user"]
        }
        # ADD THE DICT TO MONGO
        # USING UPDATE TO FIND THE ID , THEN INSERT THE SUBMIT DICT
        mongo.db.tasks.update({"_id": ObjectId(task_id)}, submit)
        flash("Task Successfully Updated")

    # TARGET THE TASK BY ITS THE ID OF THE TASK ITS CLICKED ON
    # WHICH IS THE task_id BEING PASSED IN. ObjectId WILL FIND THE ID
    # OF THE task_id. 
    task = mongo.db.tasks.find_one({"_id": ObjectId(task_id)})

    # SETUP LINKS TO THE CATEGORIES FOR THE CATEGORY SELECTION
    # SORT THEM BY NAME - ASCENDING ORDER
    categories = mongo.db.categories.find().sort("category_name", 1)

    # RETURN THE edit_task PAGE, BUT OUR EDIT PAGE
    # NEEDS TO KNOW WHICH TASK IS BEING MODIFIED, SO PASS task=task
    return render_template("edit_task.html", task=task, categories=categories)


@app.route("/delete_task/<task_id>")
def delete_task(task_id):
    # FUNCTION TO DELETE A TASK WHEN DONE.
    mongo.db.tasks.remove({"_id": ObjectId(task_id)})
    flash("Task Successfully Deleted")
    return redirect(url_for("get_tasks"))


@app.route("/get_categories")
def get_categories():
    categories = list(mongo.db.categories.find().sort("category_name", 1))
    return render_template("categories.html", categories=categories)


@ app.route("/add_category", methods=["GET", "POST"])
def add_category():
    # IF THE FUNCTION IS CALLED WITH THE POST METHOD
    if request.method == "POST":

        # SETUP OUR DICTIONARY FOR IMPORTING TO MONGO DB
        category = {
            "category_name": request.form.get("category_name"),
        }
        # ADD THE DICT TO MONGO
        mongo.db.categories.insert_one(category)
        flash("New Category Successfully Added")
        return redirect(url_for("get_categories"))


    return render_template("add_category.html")



if __name__ == "__main__":
    # Tell our app, how and where to run our application
    # set the host to the default ip set in env.py
    app.run(host=os.environ.get("IP"),
            # convert the port to an int
            port=int(os.environ.get("PORT")),
            # set this to False at end of development stage
            debug=True)
