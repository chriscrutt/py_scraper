# importing flask module
from flask import Flask

from apy import eh

# initializing a variable of Flask
app = Flask(__name__)


# decorating index function with the app.route
@app.route('/')
def index():
    return eh(1613189949857)

# og restart 1611297693597
# new 1613189949857


if __name__ == "__main__":
    app.run("104.9.116.163", 80)
