# This Python file use the following encoding: utf-8
# Linux version
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
            upload_file.save('/home/www/flask/'+file_path)
            print("success")
            return 'success'
        else:
            return 'failed'


@app.route('/about', methods=['POST', 'GET'])
def about():
    with open(r'templates/about.html', 'rb') as f:
        html_data = f.read()
    return html_data


@app.route('/process', methods=['GET', 'POST'])
def seam():
    if session.get('notes') is None:
        session['notes'] = []
    if request.method == "POST":
        my_file = request.files.get('img')
        remove_img = request.files.get('remove_img')
        pro_img = request.files.get('pro_img')
        if remove_img is not None and remove_img.filename != '':
            ori_img = Image.open('/home/www/flask/'+session['notes'][-1])
            ori_w, ori_h = ori_img.size
            tt = str(int(time.time()))
            file_name = 'static/' + 'original' + tt + '.jpg'
            remove_img.save('/home/www/flask/'+file_name)
            session['notes'].append('static/' + 'original' + tt + '.jpg')
            time.sleep(2)
            img = Image.open('/home/www/flask/'+file_name)
            width, height = img.size
            if ori_h != height or ori_w != width:
                img = img.resize((ori_w, ori_h), Image.ANTIALIAS)
                img.save('/home/www/flask/'+file_name)
            wid = request.form.get('the_width3')
            hei = request.form.get('the_height3')
            tmp_image = '/tmp/original.jpg'
            mask_image = '/tmp/mask.jpg'
            print(session['notes'][-1])
            shutil.copyfile('/home/www/flask/' + session['notes'][-2], tmp_image)
            shutil.copyfile('/home/www/flask/' + session['notes'][-1], mask_image)
            if wid is None:
                wid = ori_w
            if hei is None:
                hei = ori_h
            ddw = str(int(wid) - ori_w)
            ddh = str(int(hei) - ori_h)
            if wid is not None or hei is not None:
                os.system(
                    "python SeamCaver_two.py -remove -im " + tmp_image + " -out " + tmp_image + ' -rmask ' + mask_image
                    + " -dy " + ddh + " -dx " + ddw)
                tt = str(int(time.time()))
                file_name = 'static/' + 'original' + tt + '.jpg'
                session['notes'].append('static/' + 'original' + tt + '.jpg')
                shutil.copyfile('/tmp/original.jpg', '/home/www/flask/' + file_name)
                img = Image.open('/home/www/flask/'+session['notes'][-1])
                width, height = img.size
                print("remove")
                with open(r'templates/process.html', 'rb') as f:
                    html_data = f.read().decode('utf-8')
                    html_data = html_data.replace('dis_width', str(width))
                    html_data = html_data.replace('dis_height', str(height))
                    html_data = html_data.replace('original.jpg', file_name)
                return html_data
            else:
                os.system(
                    "python SeamCaver_two.py -remove -im " + tmp_image + " -out " + tmp_image + ' -rmask ' + mask_image)
                tt = str(int(time.time()))
                file_name = 'static/' + 'original' + tt + '.jpg'
                session['notes'].append('static/' + 'original' + tt + '.jpg')
                shutil.copyfile('/tmp/original.jpg', '/home/www/flask/' + file_name)
                img = Image.open('/home/www/flask/'+session['notes'][-1])
                width, height = img.size
                print("remove")
                with open(r'templates/process.html', 'rb') as f:
                    html_data = f.read().decode('utf-8')
                    html_data = html_data.replace('dis_width', str(width))
                    html_data = html_data.replace('dis_height', str(height))
                    html_data = html_data.replace('original.jpg', file_name)
                return html_data

        if pro_img is not None and pro_img.filename != '':
            ori_img = Image.open('/home/www/flask/'+session['notes'][-1])
            ori_w, ori_h = ori_img.size
            tt = str(int(time.time()))
            file_name = 'static/' + 'original' + tt + '.jpg'
            pro_img.save('/home/www/flask/'+file_name)
            session['notes'].append('static/' + 'original' + tt + '.jpg')
            time.sleep(2)
            img = Image.open('/home/www/flask/'+file_name)
            width, height = img.size
            if ori_h != height or ori_w != width:
                img = img.resize((ori_w, ori_h), Image.ANTIALIAS)
                img.save('/home/www/flask/'+file_name)
            wid = request.form.get('the_width2')
            hei = request.form.get('the_height2')
            tmp_image = '/tmp/original.jpg'
            mask_image = '/tmp/mask.jpg'
            print(session['notes'][-1])
            shutil.copyfile('/home/www/flask/' + session['notes'][-2], tmp_image)
            shutil.copyfile('/home/www/flask/' + session['notes'][-1], mask_image)
            if wid is not None or hei is not None:
                if wid is None or wid == '':
                    wid = ori_w
                    ddw = '0'
                else:
                    ddw = str(int(wid) - ori_w)
                if hei is None or hei == '':
                    hei = ori_h
                    ddh = '0'
                else:
                    ddh = str(int(hei) - ori_h)
                os.system(
                    "python SeamCaver_two.py -resize -im " + tmp_image + " -out " + tmp_image + ' -mask ' + mask_image
                    + " -dy " + ddh + " -dx " + ddw)
                tt = str(int(time.time()))
                file_name = 'static/' + 'original' + tt + '.jpg'
                session['notes'].append('static/' + 'original' + tt + '.jpg')
                shutil.copyfile('/tmp/original.jpg', '/home/www/flask/' + file_name)
                img = Image.open('/home/www/flask/'+session['notes'][-1])
                width, height = img.size
                print("resize")
                with open(r'templates/process.html', 'rb') as f:
                    html_data = f.read().decode('utf-8')
                    html_data = html_data.replace('dis_width', str(width))
                    html_data = html_data.replace('dis_height', str(height))
                    html_data = html_data.replace('original.jpg', file_name)
                return html_data
            else:
                os.system(
                    "python SeamCaver_two.py -resize -im " + tmp_image + " -out " + tmp_image + ' -mask ' + mask_image)
                tt = str(int(time.time()))
                file_name = 'static/' + 'original' + tt + '.jpg'
                session['notes'].append('static/' + 'original' + tt + '.jpg')
                shutil.copyfile('/tmp/original.jpg', '/home/www/flask/' + file_name)
                img = Image.open('/home/www/flask/'+session['notes'][-1])
                width, height = img.size
                print("resize")
                with open(r'templates/process.html', 'rb') as f:
                    html_data = f.read().decode('utf-8')
                    html_data = html_data.replace('dis_width', str(width))
                    html_data = html_data.replace('dis_height', str(height))
                    html_data = html_data.replace('original.jpg', file_name)
                return html_data

        if my_file is not None:
            if my_file.filename == '':
                file_name = 'static/'+'original1.jpg'
                session['notes'].append('static/' + 'original1.jpg')
                time.sleep(2)
                img = Image.open(file_name)
                width, height = img.size
                with open(r'templates/process.html', 'rb') as f:
                    html_data = f.read().decode('utf-8')
                    html_data = html_data.replace('dis_width', str(width))
                    html_data = html_data.replace('dis_height', str(height))
                    html_data = html_data.replace('original.jpg', file_name)
                return html_data
            else:
                tt = str(int(time.time()))
                file_name = 'static/' + 'original' + tt + '.jpg'
                my_file.save('/home/www/flask/' + file_name)
                session['notes'].append('static/' + 'original' + tt + '.jpg')
                print(my_file)
                time.sleep(2)
                img = Image.open('/home/www/flask/' + file_name)
                width, height = img.size
                with open(r'templates/process.html', 'rb') as f:
                    html_data = f.read().decode('utf-8')
                    html_data = html_data.replace('dis_width', str(width))
                    html_data = html_data.replace('dis_height', str(height))
                    html_data = html_data.replace('original.jpg', file_name)
                return html_data
        wid = request.form.get('the_width1')
        hei = request.form.get('the_height1')
        if wid is not None or hei is not None:
            tmp_image = '/tmp/original.jpg'
            print(session['notes'][-1])
            shutil.copyfile('/home/www/flask/' + session['notes'][-1], tmp_image)
            print(wid)
            img = Image.open('/home/www/flask/'+session['notes'][-1])
            ori_w, ori_h  = img.size
            if wid is None or wid == '':
                wid = ori_w
                ddw = '0'
            else:
                ddw = str(int(wid) - ori_w)
            if hei is None or hei == '':
                hei = ori_h
                ddh = '0'
            else:
                ddh = str(int(hei) - ori_h)
            print(wid)
            print(ori_w)
            os.system(
                "python SeamCaver_two.py -resize -im " + tmp_image + " -out " + tmp_image +
                " -dy "+ddh+" -dx "+ddw)
            tt = str(int(time.time()))
            file_name = 'static/'+'original' + tt + '.jpg'
            session['notes'].append('static/' + 'original' + tt + '.jpg')
            shutil.copyfile('/tmp/original.jpg', '/home/www/flask/' + file_name)
            img = Image.open('/home/www/flask/'+session['notes'][-1])
            width, height = img.size
            with open(r'templates/process.html', 'rb') as f:
                html_data = f.read().decode('utf-8')
                html_data = html_data.replace('dis_width', str(width))
                html_data = html_data.replace('dis_height', str(height))
                html_data = html_data.replace('original.jpg', file_name)
            return html_data
        else:
            img = Image.open('/home/www/flask/'+session['notes'][-1])
            ori_w, ori_h  = img.size
            with open(r'templates/process.html', 'rb') as f:
                html_data = f.read().decode('utf-8')
                html_data = html_data.replace('dis_width', str(ori_w))
                html_data = html_data.replace('dis_height', str(ori_h))
                html_data = html_data.replace('original.jpg', session['notes'][-1])
            return html_data
    else:
        return 'Please use the post method!'


if __name__ == '__main__':
    app.run()
