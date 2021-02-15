# importing flask module
from flask import Flask

from apy import eh

# initializing a variable of Flask
app = Flask(__name__)


# decorating index function with the app.route
@app.route('/')
def index():
    return eh(1613361662, "s_s")

# og restart first trade 1611908665000
# new first trade 1613361662

if __name__ == "__main__":
    app.run("104.9.116.163", 82)
