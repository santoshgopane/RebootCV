from flask import Flask, render_template
from pymongo import MongoClient
from config import CONNECTION_STRING

app = Flask(__name__)


@app.route("/")
def Index():

    Client = MongoClient(CONNECTION_STRING)

    print("DB:", Client.test)

    return render_template("index.html", DB=Client.test)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
