import time, re, random, datetime, telepot
from subprocess import call
import subprocess, os, sys
from telepot.loop import MessageLoop
from flask import Flask, request, make_response, render_template, url_for, g, send_file
from flask import send_from_directory, jsonify
from flask_restful import Resource, Api

# #Vars for Selenium covid kids approval
# v_UserId = os.getenv('USER_ID')
# v_UserKey = os.getenv('USER_KEY') 
# v_KidTotal = os.getenv('KIDS_NUM')
# #Auto Commmand List


app = Flask(__name__)
api = Api(app)
app.config['v_UserId']=os.getenv('USER_ID')
app.config['v_UserKey']=os.getenv('USER_KEY')
app.config['v_KidTotal']=os.getenv('KIDS_NUM')


@app.route('/sign')
def sign():
    try:
        for file in os.listdir("/opt"):
            if file.endswith(".png"):
                Image = os.path.join("/opt", file)
                os.remove(str(Image))
         subprocess.check_output('/usr/bin/python Health_Staytments.py  -u ' + app.config['v_UserId'] +  '-p ' + app.config['v_UserKey'] + ' -n ' +  str(app.config['v_KidTotal']) , shell=True)
        return jsonify('{"success":"1","data":""}')
        # bot.sendPhoto(chat_id=chat_id, photo=open(str(Image), 'rb'))
    except Exception as e:
        return jsonify('{"success":"1","data":"' + str(e) + '"}')


@app.route('/statement')
def getStatement():
    for file in os.listdir("/opt"):
        if file.endswith(".png"):
            Image = os.path.join("/opt", file)
            return send_file(str(Image), mimetype='image/png')



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=6700)

