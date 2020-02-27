# This Python file use the following encoding: utf-8
from flask import Flask
from flask import render_template, request

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def index():
    # return render('about.html')
    with open(r'templates/index.html', 'rb') as f:
        html_data = f.read()
    return html_data


@app.route('/about', methods=['POST', 'GET'])
def about():
    with open(r'templates/about.html', 'rb') as f:
        html_data = f.read()
    return html_data


@app.route('/process', methods=['POST', 'GET'])
def process():
    return render_template('process.html')


if __name__ == '__main__':
    app.run()
