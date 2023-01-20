from flask import Flask, jsonify, request
import numpy as np
import pickle

app = Flask(__name__)

linear_model = pickle.load(open("linear_model.pkl", "rb"))
columns_list = pickle.load(open("columns_list.obj", "rb"))
normal_scaler = pickle.load(open("normal_scaler.obj", "rb"))

@app.route("/sepallength", methods = ["POST"])
def sepallength():
    data = request.get_json()
    sepal_width = data["sepal_width"]
    print("sepal_width", sepal_width)

    petal_length = data["petal_length"]
    print("petal_length", petal_length)

    petal_width = data["petal_width"]
    print("petal_width", petal_width)

    species = data["species"]
    print("species", species)

    array = np.zeros(len(columns_list))

    array[0] = sepal_width
    array[1] = petal_length
    array[2] = petal_width
    index = np.where(columns_list == species)[0][0]
    print(index)
    array[index] = 1

    scaled_array = normal_scaler.transform([array])

    prediction = linear_model.predict(scaled_array)
    prediction = prediction[0]

    return jsonify({"Predicted Sepal length" : prediction})


if __name__ == "__main__":
    app.run(debug = True)