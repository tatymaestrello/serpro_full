# -*- coding: UTF-8 -*-
from flask import render_template, request, redirect, url_for
from app import app
import json
from api import process_client
from reader import readOptions


@app.route("/")
def home():
    menu = open("menu.json", mode="r").read()
    print(menu)
    reports = json.loads(menu)
    return render_template("base.html", reports=reports)


@app.route("/add", methods=["POST"])
def add():
    print(request.form)
    createfolder = request.form.get("createfolder")
    if createfolder == "checked":
        createfolder = "S"
    else:
        createfolder = "N"
    options = request.form.getlist("options")
    dashboards = readOptions(options)

    requestData = {
        "cliente": request.form.get("name"),
        "criar_pasta": createfolder,
        "dashboards": dashboards,
    }
    print("Sending request")
    print(requestData)
    result = process_client(requestData)
    print("Receiving response")
    print(result)
    return render_template("added.html", result=result)


@app.errorhandler(404)
def not_found(error):
    return render_template("notfound.html", error=error)
