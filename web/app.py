from flask import Flask
from flask import request
from flask import render_template
from flask import redirect
from flask import url_for
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)

client = MongoClient("mongodb://mongo:27017/")
mydb = client["ipa-msapp"]
mycol = mydb["router"]

@app.route("/")
def main():
    return render_template("index.html", data=mycol.find({}))

@app.route("/add", methods=["POST"])
def add_ip():
    ip = request.form.get("ip")
    username = request.form.get("username")
    password = request.form.get("password")

    if ip and username and password:
        mycol.insert_one({'ip': ip, 'username': username, 'password': password})
    return redirect("/")

@app.route("/delete", methods=["POST"])
def delete_ip():
    try:
        idx = request.form.get("idx")
        myquery = {'_id': ObjectId(idx)}
        mycol.delete_one(myquery)
    except Exception:
        pass
    return redirect(url_for("main"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
