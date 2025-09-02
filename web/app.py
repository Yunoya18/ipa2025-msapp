import os

from flask import Flask, request, render_template, redirect, url_for
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)

mongo_uri  = os.environ.get("MONGO_URI")
db_name    = os.environ.get("DB_NAME")

client = MongoClient(mongo_uri)
mydb = client[db_name]
routers = mydb["routers"]
interface_status = mydb["interface_status"]

@app.route("/")
def main():
    return render_template("index.html", data=routers.find({}))

@app.route("/add", methods=["POST"])
def add_ip():
    ip = request.form.get("ip")
    username = request.form.get("username")
    password = request.form.get("password")

    if ip and username and password:
        routers.insert_one({'ip': ip, 'username': username, 'password': password})
    return redirect("/")

@app.route("/delete", methods=["POST"])
def delete_ip():
    try:
        idx = request.form.get("idx")
        myquery = {'_id': ObjectId(idx)}
        routers.delete_one(myquery)
    except Exception:
        pass
    return redirect(url_for("main"))

@app.route("/router/<ip>", methods=["GET"])
def get_router(ip):
    router_details = interface_status.find({"router_ip": ip}).sort("timestamp", -1).limit(3)
    return render_template("router_details.html", router_ip=ip, router_details=router_details)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
