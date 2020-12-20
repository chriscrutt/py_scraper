# importing flask module
from flask import Flask

from delete import eh

# initializing a variable of Flask
app = Flask(__name__)


# decorating index function with the app.route
@app.route('/')
def index():
    return eh()


if __name__ == "__main__":
    app.run()
