# This Python file use the following encoding: utf-8
import shutil
import importlib,sys
from PIL import Image
importlib.reload(sys)
from flask import session
import os
from flask import Flask, request
from flask_session import Session
import time
app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = 'filesystem'
Session(app)
notes = []

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'GET':
        with open(r'templates/index.html', 'rb') as f:
            html_data = f.read()
        return html_data
    elif request.method == "POST":
        upload_file = request.files['file']
        old_file_name = upload_file.filename
        file_path = os.path.join('/local/share/DeepLearning', 'new' + old_file_name)

        if upload_file:
            upload_file.save(file_path)
            print("success")
            return 'success'
        else:
            return 'failed'


@app.route('/about', methods=['POST', 'GET'])
def about():
    with open(r'templates/about.html', 'rb') as f:
        html_data = f.read()
    return html_data


@app.route("/my_test", methods=['POST'])
def get_frame():
    upload_file = request.files['file']
    old_file_name = upload_file.filename
    file_path = os.path.join('new' + old_file_name)

    if upload_file:
        upload_file.save('/tmp/1.jpg')
        print("success")
        return 'success'
    else:
        return 'failed'


@app.route('/process', methods=['GET', 'POST'])
def seam():
    if session.get('notes') is None:
        session['notes'] = []
    if request.method == "POST":
        my_file = request.files.get('img')
        if my_file is not None:
            tt = str(int(time.time()))
            file_name = 'static/'+'original' + tt + '.jpg'
            my_file.save(file_name)
            session['notes'].append('static/'+'original' + tt + '.jpg')
            print(my_file)
            img = Image.open(file_name)
            width, height = img.size
            with open(r'templates/process.html', 'rb') as f:
                html_data = f.read().decode('utf-8')
                html_data = html_data.replace('dis_width', str(width))
                html_data = html_data.replace('dis_height', str(height))
                html_data = html_data.replace('original.jpg', file_name)
            return html_data
        wid = request.form.get('the_width')
        hei = request.form.get('the_height')
        if wid is not None:
            tmp_image = 'D://original.jpg'
            print(session['notes'][-1])
            shutil.copyfile('C://Users/whzgo/PycharmProjects/Seam/' + session['notes'][-1], tmp_image)
            print(wid)
            img = Image.open(session['notes'][-1])
            ori_w, ori_h  = img.size
            ddw = str(int(wid)-ori_w)
            ddh = str(int(hei)-ori_h)
            os.system(
                "python SeamCaver_two.py -resize -im " + tmp_image + " -out " + tmp_image +
                " -dy "+ddh+" -dx "+ddw+" -vis")
            tt = str(int(time.time()))
            file_name = 'static/'+'original' + tt + '.jpg'
            session['notes'].append('static/' + 'original' + tt + '.jpg')
            shutil.copyfile('D://original.jpg', 'C://Users/whzgo/PycharmProjects/Seam/' + file_name)
            img = Image.open(session['notes'][-1])
            width, height = img.size
            with open(r'templates/process.html', 'rb') as f:
                html_data = f.read().decode('utf-8')
                html_data = html_data.replace('dis_width', str(width))
                html_data = html_data.replace('dis_height', str(height))
                html_data = html_data.replace('original.jpg', file_name)
            return html_data
        else:
            img = Image.open(session['notes'][-1])
            ori_w, ori_h  = img.size
            with open(r'templates/process.html', 'rb') as f:
                html_data = f.read().decode('utf-8')
                html_data = html_data.replace('dis_width', str(ori_w))
                html_data = html_data.replace('dis_height', str(ori_h))
                html_data = html_data.replace('original.jpg', session['notes'][-1])
            return html_data
    else:
        return 'Please use the post method!'


@app.route('/mask')
def mask():
    with open(r'templates/mask.html', 'rb') as f:
        html_data = f.read().decode('utf-8')
        html_data = html_data.replace('dis_width', str(ori_w))
        html_data = html_data.replace('dis_height', str(ori_h))
        html_data = html_data.replace('original.jpg', session['notes'][-1])
    return html_data


if __name__ == '__main__':
    app.run()
