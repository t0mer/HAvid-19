from loguru import logger
import time, re, random, datetime
from subprocess import call
import subprocess, os, sys, shutil, yaml
from flask import Flask, request, make_response, render_template, url_for, g, send_file
from flask import send_from_directory, jsonify
from flask_restful import Resource, Api
 
configfile="/opt/dockerbot/config/config.yml"
original_configfile = r'/etc/config.yml'
edu_Image = '/opt/dockerbot/images/edu_approval.png'
default_Image = '/opt/dockerbot/please_sign.jpg'
webtop_Image = '/opt/dockerbot/images/webtop_approval.png'
infogan_Image = '/opt/dockerbot/images/infogan_approval.png'

def CopyConfig():
    if not os.path.exists(configfile):
        shutil.copyfile(original_configfile, configfile)

CopyConfig()

def ReadConfig():
    with open(configfile, 'r') as stream:
        try:
            logger.info("Reading Configuration")
            list = yaml.safe_load(stream)
            return list
        except yaml.YAMLError as ex:
            logger.error("Error Reading Configuration, Msg: " + str(ex))
            return ""


app = Flask(__name__)

@app.route('/edu/sign')
def sign_edu():
    list = ReadConfig()
    if list['edu']['USER_ID'] and list['edu']['USER_KEY'] != None:
        try:
            logger.info("Starting Sign process at https://parents.education.gov.i")
            import Health_Statements
            if Health_Statements.sign(str(list['edu']['USER_ID']), list['edu']['USER_KEY'], edu_Image) == 1:
                return jsonify('{"signed":"1","data":""}')
            else:
                return jsonify('{"signed":"0","data":""}')
        except Exception as ex:
            logger.error(str(ex))
            return jsonify('{"signed":"0","data":"' + str(ex) + '"}')

    return jsonify('{"signed":"0","data":"Edu is not configured"}')

@app.route('/edu/statement')
def edu_statement():
    if os.path.exists(edu_Image):
        return send_file(str(edu_Image), mimetype='image/png', cache_timeout=-1)
    else:
        return send_file(str(default_Image), mimetype='image/jpeg',cache_timeout=-1)


@app.route('/webtop/sign')
def sign_webtop():
    list = ReadConfig()
    if list['webtop']['USER_ID'] and list['webtop']['USER_KEY'] != None:
        try:
            logger.info("Starting Sign process at https://parents.education.gov.i")
            import Webtop_Health_Statements
            if Webtop_Health_Statements.sign(list['webtop']['USER_ID'], list['webtop']['USER_KEY'], webtop_Image) == 1:
                return jsonify('{"signed":"1","data":""}')
            else:
                return jsonify('{"signed":"0","data":""}')
        except Exception as ex:
            logger.error(str(ex))
            return jsonify('{"signed":"0","data":"' + str(ex) + '"}')

    return jsonify('{"signed":"0","data":"Webtop is not configured"}')

@app.route('/webtop/statement')
def webtop_statement():
    if os.path.exists(webtop_Image):
        return send_file(str(webtop_Image), mimetype='image/png', cache_timeout=-1)
    else:
        return send_file(str(default_Image), mimetype='image/jpeg',cache_timeout=-1)


@app.route('/infogan/sign')
def sign_infogan():
    list = ReadConfig()
    if list['infogan']['BASE_URL'] and list['infogan']['KID_ID'] and list['infogan']['PARENT_NAME'] and list['infogan']['KID_NAME'] and list['infogan']['PARENT_ID']  != None:
        try:
            logger.info("Starting Sign process at https://parents.education.gov.i")
            import Infogan_Health_Statements
            if Infogan_Health_Statements.sign(list['infogan']['PARENT_NAME'], str(list['infogan']['PARENT_ID']),  list['infogan']['KID_NAME'], str(list['infogan']['KID_ID']), list['infogan']['BASE_URL'], infogan_Image) == 1:
                return jsonify('{"signed":"1","data":""}')
            else:
                return jsonify('{"signed":"0","data":""}')
        except Exception as ex:
            logger.error(str(ex))
            return jsonify('{"signed":"0","data":"' + str(ex) + '"}')

    return jsonify('{"signed":"0","data":"Infogan is not configured"}')

@app.route('/infogan/statement')
def infogan_statement():
    if os.path.exists(infogan_Image):
        return send_file(str(infogan_Image), mimetype='image/png', cache_timeout=-1)
    else:
        return send_file(str(default_Image), mimetype='image/jpeg',cache_timeout=-1)



@app.route('/mashov/sign')
def mashov_sign():
    list = ReadConfig()
    v_MASHOV_NUMBER_OF_KIDS = len(list['mashov'])
    if v_MASHOV_NUMBER_OF_KIDS >= 1 and list['mashov']['kid1']['MASHOV_USER_ID_KID'] != None:
        v_MASHOV_NUMBER_OF_KIDS = v_MASHOV_NUMBER_OF_KIDS + 1

    Image = '/opt/dockerbot/images/mashov_approval_'
    if v_MASHOV_NUMBER_OF_KIDS >= 1 and list['mashov']['kid1']['MASHOV_USER_ID_KID'] != None:
        try:
            import Mashov_Health_Statements
            if v_MASHOV_NUMBER_OF_KIDS >= 1 and list['mashov']['kid1']['MASHOV_USER_ID_KID'] != None:
                for Mashov_Kid_Number in range(1, v_MASHOV_NUMBER_OF_KIDS, 1):
                    if list['mashov']['kid'+str(Mashov_Kid_Number)]['MASHOV_USER_ID_KID'] and list['mashov']['kid'+str(Mashov_Kid_Number)]['MASHOV_USER_PWD_KID'] and list['mashov']['kid'+str(Mashov_Kid_Number)]['MASHOV_SCHOOL_ID_KID'] != None:
                        logger.info("Starting Sign process at https://web.mashov.info/students/login for Kid Number: " + str(Mashov_Kid_Number))
                        Prep_Switch_MASHOV_USER_DICT_ID_KID = list['mashov']['kid'+str(Mashov_Kid_Number)]['MASHOV_USER_ID_KID']
                        Prep_Switch_MASHOV_USER_DICT_ID_PWD = list['mashov']['kid'+str(Mashov_Kid_Number)]['MASHOV_USER_PWD_KID']
                        Prep_Switch_MASHOV_USER_DICT_ID_SCHOOL_ID = list['mashov']['kid'+str(Mashov_Kid_Number)]['MASHOV_SCHOOL_ID_KID']                     
                        Mashov_Health_Statements.sign(Prep_Switch_MASHOV_USER_DICT_ID_KID, Prep_Switch_MASHOV_USER_DICT_ID_PWD, Prep_Switch_MASHOV_USER_DICT_ID_SCHOOL_ID, str(Mashov_Kid_Number), Image + str(Mashov_Kid_Number) + ".png")
            else:
                return jsonify('{"signed":"0","data":"Mashov is not configured"}')
                config_mashov = 0
        except Exception as ex:
            logger.exception("Faild to sign Mashov, Msg: " + str(ex))
            return jsonify('{"signed":"0","data":"' + str(ex) + '"}')
        return jsonify('{"signed":"1","data":""}')
            
    else:
        return jsonify('{"signed":"0","data":"Mashov is not configured"}')

@app.route('/mashov/statement')
def hbinov_statement():
    Image = '/opt/dockerbot/images/mashov_approval_' + str(request.args.get('kid')) + '.png'
    if os.path.exists(Image):
        return send_file(str(Image), mimetype='image/png', cache_timeout=-1)
    else:
        return send_file(str(default_Image), mimetype='image/jpeg',cache_timeout=-1)




#### Not Operational Yet ######
@app.route('/hbinov/sign')
def sign_hbinov():
    list = ReadConfig()
    if list['hbinov']['URL'] and list['hbinov']['USER_NAME'] and list['hbinov']['PASSWORD'] != None:
        try:
            logger.info("Starting Sign process at " + list['hbinov']['URL'])
            import Hbinov_Health_Statements
            if Hbinov_Health_Statements.sigשמn() == 1:
                return jsonify('{"signed":"1","data":""}')
            else:
                return jsonify('{"signed":"0","data":""}')
        except Exception as ex:
            logger.error(str(ex))
            return jsonify('{"signed":"0","data":"' + str(ex) + '"}')

    return jsonify('{"signed":"0","data":"Edu is not configured"}')




if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=6700)
