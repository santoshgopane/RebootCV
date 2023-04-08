from flask import Flask, render_template, request, session, redirect, url_for
from pymongo import MongoClient
from common.config import CONNECTION_STRING
import bcrypt

app = Flask(__name__)

app.secret_key = "dev"

Client = MongoClient(CONNECTION_STRING)

print("DB:", db := Client.TestDB)
print("All Collections for TestDB:", db.list_collection_names())
test_collection = db.TestCollection

print(">>", test_collection.find_one({"Email": "santosh@gmail.com1"}))


@app.route("/")
def Index():
    # if "Email" in session:
    #     return render_template(
    #         "dashboard.html", ses_message="yes" if "Email" in session else "no"
    #     )

    return render_template(
        "index.html" if "Email" not in session else "dashboard.html",
        ses_message="yes" if "Email" in session else "no",
    )


@app.route("/register", methods=["get", "post"])
def register():
    print(">>", request)
    message = ""
    if "Email" in session:
        return render_template(
            "dashboard.html", ses_message="yes" if "Email" in session else "no"
        )

    if request.method == "POST":
        username = request.form.get("Email")
        first_name = request.form.get("FirstName")
        last_name = request.form.get("LastName")
        pwd = request.form.get("Pass")

        resp = test_collection.find_one({"Email": username})
        if resp:
            message = "Email address alredy in use!"
        else:
            hashed_pwd = bcrypt.hashpw(pwd.encode("utf-8"), bcrypt.gensalt())
            item = {
                "Email": username,
                "FirstName": first_name,
                "LastName": last_name,
                "Password": hashed_pwd,
            }
            print("item:", item)
            test_collection.insert_one(item)
            message = "User has been registered, please login to use app!"

            return render_template("login.html", message=message)

        print("this is a post request!!!!!!!")
        # return redirect(url_for("choose_template"))
    else:
        print("This is a GET request!!!!!!")
    return render_template(
        "register.html", ses_message="yes" if "Email" in session else "no"
    )


@app.route("/login", methods=["get", "post"])
def login():
    message = ""

    if "Email" in session:
        return render_template(
            "dashboard.html", ses_message="yes" if "Email" in session else "no"
        )

    if request.method == "POST":
        username = request.form.get("Email")
        pwd = request.form.get("Password")

        resp = test_collection.find_one({"Email": username}, {"Password": 1})
        print("resp:", resp)
        if resp:
            pass_stored = resp["Password"]

            if bcrypt.checkpw(pwd.encode("utf-8"), pass_stored):
                session["Email"] = username
                return redirect(url_for("dashboard"))

            message = pass_stored

    return render_template(
        "login.html", ses_message="yes" if "Email" in session else "no"
    )


@app.route("/logout", methods=["get"])
def logout():
    if "Email" in session:
        session.pop("Email", None)
        return render_template("login.html")
    else:
        return render_template("login.html")


@app.route("/dashboard", methods=["get"])
def dashboard():

    # if "Email" in session:
    #     print(session)
    #     return render_template(
    #         "dashboard.html", ses_message="yes" if "Email" in session else "no"
    #     )
    # else:
    return render_template(
        "login.html" if "Email" not in session else "dashboard.html",
        ses_message="yes" if "Email" in session else "no",
    )


@app.route("/choose-templates")
def choose_template():
    return "<h1>This page is going to be customizing the pdf!</h1>"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
