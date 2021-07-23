from re import X
from flask import Flask, render_template, url_for, request
import joblib
import os
import pandas as pd


app = Flask(__name__)

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
        else:
            y_predict = phish_model_ls.predict(X_predict)
        return render_template('result.html', prediction=y_predict)


if __name__ == '__main__':
    app.run(debug=True)
