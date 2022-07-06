from flask import Flask, request, jsonify
import pickle
import pandas as pd
import numpy as np

app = Flask(__name__)

# label
LABEL = ["Basic", "Deluxe", "King"]

# pipeline
with open("pipeline_pre.pkl", "rb") as f1:
    pipeline = pickle.load(f1)

# model
with open("model_class.pkl", "rb") as f2:
    model = pickle.load(f2)

# drop features
feat_imp_drop = [5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25]


# home page
@app.route("/")
def welcome():
    return "<h3>Selamat Datang di Program Backend Travelry</h3>"

# predict page
@app.route("/predict", methods=["GET", "POST"])
def predict_class():
    if request.method == "POST":
        content = request.json
        try:
            new_data = {'Age': content['age'],
                        'CityTier': 1,
                        'Occupation':'Salaried',
                        'Gender': 'Female',
                        'NumberOfPersonVisiting': content['person'],
                        'PreferredPropertyStar': 4,
                        'MaritalStatus': 'Married',
                        'NumberOfTrips': content['trip'],
                        'Passport':1,
                        'OwnCar': 0,
                        'NumberOfChildrenVisiting': content['children'],
                        'Designation': 'Executive',
                        'MonthlyIncome_rp': content['monthly_income']}
            new_data = pd.DataFrame([new_data])
            new_data_final = pipeline.transform(new_data)
            new_data_final = np.delete(new_data_final, np.s_[feat_imp_drop], axis=1)
            res = model.predict(new_data_final)
            result = {'class':str(res[0]),
                      'class_name':LABEL[res[0]]}
            response = jsonify(success=True,
                               result=result)
            return response, 200
        except Exception as e:
            response = jsonify(success=False,
                               message=str(e))
            return response, 400
    # return dari method get
    return "<p>Silahkan gunakan method POST untuk mode <em>inference model</em></p>"

# app.run(debug=True)