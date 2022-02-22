from re import X
from flask import Flask, render_template, url_for, request, jsonify
import joblib
import os
import pandas as pd
from werkzeug.wrappers import Request
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)


phish_model = open('phishing.pkl', 'rb')
phish_model_ls = joblib.load(phish_model)

train = pd.read_csv('url_check.csv')
lst = train.url.tolist()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        url = request.form.get('url')
        X_predict = []
        X_predict.append(str(url))
        if url in lst:
            y_predict = 1
        elif url == 'www.google.co.in' or url == 'https://www.google.co.in/':
            y_predict = 0
        elif url == '':
            y_predict = 2
        else:
            y_predict = phish_model_ls.predict(X_predict)
        return render_template('result.html', prediction=y_predict)


@app.route('/predict1', methods=['POST'])
def predict1():
    if request.method == 'POST':
        url = request.json['url']
        print(url)
        X_predict = []
        X_predict.append(str(url))
        y_predict = phish_model_ls.predict(X_predict)
        
        if url in lst:
            result = {
                "Response":"It is a phishing url",
                "Status":"Success"
                }
        elif url == 'www.google.co.in' or url == 'https://www.google.co.in/':
            result = {
                "Response":"It is not a phishing url",
                "Status":"Error"
                }
        elif url == '':
            result = {
                "Response":"Required fields are missing",
                "Status":"Error"
                }
        elif y_predict == 'bad':
            result = {
                "Response":"It is a phishing url",
                "Status":"Success"
                }
        else:
            result = {
                "Response":"It is not a phishing url",
                "Status":"Error"
                }
        return jsonify(result)


@app.route('/predict2', methods=['POST'])
def predict2():
    if request.method == 'POST':
        url = request.json['url']
        X_predict = []
        X_predict.append(str(url))
        y_predict = phish_model_ls.predict(X_predict)
        if url in lst:
            result = 1 ##phishing url
        elif url == 'www.google.co.in' or url == 'https://www.google.co.in/':
            result = 1 ##phishing url
        elif url == '':
            result = 2 ##required fields misssing
        elif y_predict == 'bad':
            result = 1 ##phishing url
        else:
            result = 0 ##not phishing
        return jsonify(result)


@app.route('/predict3', methods=['POST'])
def predict3():
    if request.method == 'POST':
        url = request.json['url']
        X_predict = []
        X_predict.append(str(url))
        y_predict = phish_model_ls.predict(X_predict)
        if url in lst:
            return json.dumps({'success':True}), 200, {'ContentType':'application/json'}  ##phishing url
        elif url == 'www.google.co.in' or url == 'https://www.google.co.in/':
            return json.dumps({'success':True}), 200, {'ContentType':'application/json'}  ##phishing url
        elif url == '':
            return json.dumps({'error':True}), 200, {'ContentType':'application/json'} ##required fields misssing
        elif y_predict == 'bad':
            return json.dumps({'success':True}), 200, {'ContentType':'application/json'}  ##phishing url
        else:
            return json.dumps({'error':True}), 200, {'ContentType':'application/json'}  ##not phishing
        return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)
