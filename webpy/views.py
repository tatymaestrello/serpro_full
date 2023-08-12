# -*- coding: UTF-8 -*-
from flask import render_template, request, redirect, url_for, flash
from app import app
import json
from models import NewDashboard


@app.route("/")
def home():
    menu=open("menu.json", mode="r")
    print(menu)
    reports = json.loads(menu)
    #     json.dumps(
    #         [
    #             {"id": "id0", "value": "RLT000", "label": "Relatório Padrao"},
    #             {
    #                 "id": "id1",
    #                 "value": "RLT001",
    #                 "label": "Relatório Raiz",
    #                 "childs": [
    #                     {"id": "id10", "value": "RLT0011", "label": "Parte 2 da raiz"},
    #                     {
    #                         "id": "id11",
    #                         "value": "RLT0011",
    #                         "label": "Parte 1 da raiz",
    #                         "childs": [
    #                             {
    #                                 "id": "id111",
    #                                 "value": "RLT0012",
    #                                 "label": "Parte 2 da parte 1",
    #                             }
    #                         ],
    #                     },
    #                 ],
    #             },
    #         ]
    #     )
    # )
    return render_template("base.html", reports=reports)


@app.route("/add", methods=["POST"])
def add():
    # for debug
    print(request.form)
    newdash=request.form.get("newdash")
    if (newdash=="checked"):
        newdash="S"
    else:
        newdash="N"

    NewDashboard(
        name=request.form.get("name"),
        newdash=newdash,
        options="$".join(request.form.getlist("options")),
    )

    return redirect(url_for("home"))


@app.errorhandler(404)
def not_found(error):
    return render_template("notfound.html", error=error)
