from flask import Flask, render_template
from pymongo import MongoClient
from common.config import CONNECTION_STRING

app = Flask(__name__)

Client = MongoClient(CONNECTION_STRING)

print("DB:", db := Client.TestDB)
print("All Collections for TestDB:", db.list_collection_names())
test_collection = db.TestCollection

print(test_collection.find_one({"Email": "santosh"}))


@app.route("/")
def Index():

    return render_template("index.html")


@app.route("/register")  # , methods=["post"])
def register():

    return render_template("register.html")


@app.route("/login")  # , methods=["post"])
def login():

    return render_template("login.html")


@app.route("/choose-templates")
def choose_template():
    return "<h1>This page is going to be customizing the pdf!</h1>"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
