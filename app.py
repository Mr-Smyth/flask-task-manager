import os
from flask import Flask

# We need to import env.py, but because env.py wont
# exist on Heroku, we must check if it exists first.
# That way the program wont crash when looking for it on heroku.
# Heroku will have these variables set internally
if os.path.exists("env.py"):
    import env


app = Flask(__name__)


# Test function to check our setup
# "/" refers to the default route
@app.route("/")
def hello():
    return "Hello world .... Again!"


# Tell our app, how and where to run our application
if __name__ == "__main__":
    # set the host to the default ip set in env.py
    app.run(host=os.environ.get("IP"),
            # convert the port to an int
            port=int(os.environ.get("PORT")),
            # set this to False at end of development stage
            debug=True)
