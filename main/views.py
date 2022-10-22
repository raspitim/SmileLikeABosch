from django.http import HttpResponse
from django.shortcuts import render
from main.models import *
import pandas as pd
import numpy as np
from main.pr import *
# Create your views here.

translation = {
    "Produktpreis": "price",
    "Lieferzeit": "delivery",
    "Komponentenlänge": "length",
    "Komponentendurchmesser": "diameter",
    "Komponentenmasse": "weight",
    "Biegespannung": "bow",
    "Bauteilhärte": "hardness",
    "Fügekraft": "join"
}

def index(request):
    return render(request, "page2.html")


def internal(request, raw=False):
    if len(request.GET) == 0:
        return render(request, "internal.html")


    input_names = ["Bauteilhärte", "Komponentenlänge", "Komponentendurchmesser", "Komponentenmasse", "Biegespannung", "Fügekraft", "Lieferzeit", "Produktpreis"]
    output_names = ["Betriebsstunden", "Werkzeugstandzeit", "Durchlaufzeit"]

    components = Component.objects.all()

    train_in = np.array([np.array([component.properties.get(name=i).value for i in input_names]) for component in components])
    train_out = np.array([np.array([component.properties.get(name=i).value for i in output_names]) for component in components])

    price = request.GET["price"]
    delivery = request.GET["delivery"]
    length = request.GET["length"]
    weight = request.GET["weight"]
    diameter = request.GET["diameter"]
    bow = request.GET["bow"]
    hardness = request.GET["hardness"]
    join = request.GET["join"]

    dict_get = {
        "price": float(price),
        "delivery": float(delivery),
        "length": float(length),
        "diameter": float(diameter),
        "weight": float(weight),
        "bow": float(bow),
        "hardness": float(hardness),
        "join": float(join),
    }


    model = train(train_in, train_out)

    inputs = [float(request.GET[translation[i]]) for i in input_names]

    prediction = predict(model, np.array([inputs]))

    for (pred, output_name) in zip(prediction[0], output_names):
        print(pred.round(2))
        dict_get[output_name] = pred.round(2)

    print(dict_get)

    if raw:
        return dict_get

    return render(request, "internal_results.html", dict_get)





def correlation(request):
    data = [[component.properties.get(name="Bauteilhärte").value, component.properties.get(name="Werkzeugstandzeit").value, component.properties.get(name="Durchlaufzeit").value, component.properties.get(name="Komponentenlänge").value, component.properties.get(name="Komponentendurchmesser").value, component.properties.get(name="Komponentenmasse").value, component.properties.get(name="Biegespannung").value, component.properties.get(name="Fügekraft").value, component.properties.get(name="Betriebsstunden").value, component.properties.get(name="Lieferzeit").value, component.properties.get(name="Produktpreis").value] for component in Component.objects.all()]

    df = pd.DataFrame(data, columns=["Bauteilhärte", "Werkzeugstandzeit", "Durchlaufzeit", "Komponentenlänge", "Komponentendurchmesser", "Komponentenmasse", "Biegespannung", "Fügekraft", "Betriebsstunden", "Lieferzeit", "Produktpreis"])

    corr = df.corr()

    print(corr)

    ind = list(corr.index)

    data = {}

    for i in corr.index:
        x = ind.index(i)
        for j in corr[i].index:
            y = ind.index(j)
            data[f"c{x}_{y}"] = "red" if corr[i][j] < 0 else "green"
            data[f"o{x}_{y}"] = abs(corr[i][j])
            print(x, y)


    return render(request, "correlations.html", data)

def get_given_properties(request):
    price = request.GET["price"]
    delivery = request.GET["delivery"]
    length = request.GET["length"]
    weight = request.GET["weight"]
    diameter = request.GET["diameter"]
    bow = request.GET["bow"]
    hardness = request.GET["hardness"]
    join = request.GET["join"]

    inputs = []
    input_names = []
    output_names = []

    if price.replace('.', '', 1).isdigit():
        inputs.append(float(price))
        input_names.append("Produktpreis")
    else:
        output_names.append("Produktpreis")
    if delivery.replace('.', '', 1).isdigit():
        inputs.append(float(delivery))
        input_names.append("Lieferzeit")
    else:
        output_names.append("Lieferzeit")
    if length.replace('.', '', 1).isdigit():
        inputs.append(float(length))
        input_names.append("Komponentenlänge")
    else:
        output_names.append("Komponentenlänge")
    if diameter.replace('.', '', 1).isdigit():
        inputs.append(float(diameter))
        input_names.append("Komponentendurchmesser")
    else:
        output_names.append("Komponentendurchmesser")
    if weight.replace('.', '', 1).isdigit():
        inputs.append(float(weight))
        input_names.append("Komponentenmasse")
    else:
        output_names.append("Komponentenmasse")
    if bow.replace('.', '', 1).isdigit():
        inputs.append(float(bow))
        input_names.append("Biegespannung")
    else:
        output_names.append("Biegespannung")
    if hardness.replace('.', '', 1).isdigit():
        inputs.append(float(hardness))
        input_names.append("Bauteilhärte")
    else:
        output_names.append("Bauteilhärte")
    if join.replace('.', '', 1).isdigit():
        inputs.append(float(join))
        input_names.append("Fügekraft")
    else:
        output_names.append("Fügekraft")

    components = Component.objects.all()

    train_in = np.array([np.array([component.properties.get(name=i).value for i in input_names]) for component in components])
    train_out = np.array([np.array([component.properties.get(name=i).value for i in output_names]) for component in components])

    model = train(train_in, train_out)

    prediction = predict(model, np.array([inputs]))

    dict_get = {
        "price": price,
        "delivery": delivery,
        "length": length,
        "diameter": diameter,
        "weight": weight,
        "bow": bow,
        "hardness": hardness,
        "join": join,
    }

    for (pred, output_name) in zip(prediction[0], output_names):
        print(pred, output_name)
        dict_get[translation[output_name]] = pred.round(2)

    class Request:
        GET = request.GET

    if internal(Request, raw=True)["Werkzeugstandzeit"] < 0:
        return render(request, "page2.html", {"error": "true"})


    return render(request, "page3.html", dict_get)

