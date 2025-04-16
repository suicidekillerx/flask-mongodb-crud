from flask import Flask, render_template, request, redirect, url_for
from bson import ObjectId
from pymongo import MongoClient
import os
import pymongo

app = Flask(__name__)
cf_port = os.getenv("PORT")

title = "TODO sample application with Flask and MongoDB"
heading = "TODO Reminder with Flask and MongoDB"

client = pymongo.MongoClient("mongodb://mongodb:27017")
db = client.S6qOHHSP44Ux7RXa
todos = db.todo

def redirect_url():
    return request.args.get('next') or request.referrer or url_for('index')

@app.route("/list")
def lists():
    todos_l = todos.find()
    a1 = "active"
    return render_template('index.html', a1=a1, todos=todos_l, t=title, h=heading)

@app.route("/")
@app.route("/uncompleted")
def tasks():
    todos_l = todos.find({"done": "no"})
    a2 = "active"
    return render_template('index.html', a2=a2, todos=todos_l, t=title, h=heading)

@app.route("/completed")
def completed():
    todos_l = todos.find({"done": "yes"})
    a3 = "active"
    return render_template('index.html', a3=a3, todos=todos_l, t=title, h=heading)

@app.route("/done")
def done():
    id = request.values.get("_id")
    task = todos.find_one({"_id": ObjectId(id)})
    if task["done"] == "yes":
        todos.update_one({"_id": ObjectId(id)}, {"$set": {"done": "no"}})
    else:
        todos.update_one({"_id": ObjectId(id)}, {"$set": {"done": "yes"}})
    return redirect(redirect_url())

@app.route("/action", methods=['POST'])
def action():
    name = request.values.get("name")
    desc = request.values.get("desc")
    date = request.values.get("date")
    pr = request.values.get("pr")
    todos.insert_one({
        "name": name,
        "desc": desc,
        "date": date,
        "pr": pr,
        "done": "no"
    })
    return redirect("/list")

@app.route("/remove")
def remove():
    key = request.values.get("_id")
    todos.delete_one({"_id": ObjectId(key)})
    return redirect("/")

@app.route("/update")
def update():
    id = request.values.get("_id")
    task = todos.find({"_id": ObjectId(id)})
    return render_template('update.html', tasks=task, h=heading, t=title)

@app.route("/action3", methods=['POST'])
def action3():
    name = request.values.get("name")
    desc = request.values.get("desc")
    date = request.values.get("date")
    pr = request.values.get("pr")
    id = request.values.get("_id")
    todos.update_one(
        {"_id": ObjectId(id)},
        {'$set': {
            "name": name,
            "desc": desc,
            "date": date,
            "pr": pr
        }}
    )
    return redirect("/")

@app.route("/search", methods=['GET'])
def search():
    key = request.values.get("key")
    refer = request.values.get("refer")
    if key == "_id":
        todos_l = todos.find({refer: ObjectId(key)})
    else:
        todos_l = todos.find({refer: key})
    return render_template('searchlist.html', todos=todos_l, t=title, h=heading)

if __name__ == '__main__':
    if cf_port is None:
        app.run(host='0.0.0.0', port=5000, debug=True)
    else:
        app.run(host='0.0.0.0', port=int(cf_port), debug=True)
