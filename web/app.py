import os

from flask import Flask, request, render_template, redirect, url_for
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)

mongo_uri  = os.environ.get("MONGO_URI")
db_name    = os.environ.get("DB_NAME")

client = MongoClient(mongo_uri)
mydb = client[db_name]
mycol = mydb["routers"]

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
