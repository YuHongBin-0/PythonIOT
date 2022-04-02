# code to control OSpace devices
# by hongbin
from ctypes import pythonapi
from datetime import date, datetime
from os import stat
from sre_parse import State
import sys
import ssl
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import json
import time
from flask import ( Flask, g, redirect, render_template,Response, request, session,url_for)
app = Flask(__name__)

#login code
class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __repr__(self):
        return f'<User: {self.username}>'

users = []
users.append(User(id=1, username='test1', password='password1'))
users.append(User(id=2, username='test2', password='password2'))
users.append(User(id=3, username='test3', password='password3'))
app.secret_key = 'somesecretkeythatonlyishouldknow'

@app.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        user = [x for x in users if x.id == session['user_id']][0]
        g.user = user
        
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.pop('user_id', None)
        username = request.form['username']
        password = request.form['password']
        
        user = [x for x in users if x.username == username][0]
        if user and user.password == password:
            session['user_id'] = user.id
            return redirect(url_for('home'))
        return redirect(url_for('login'))
    return render_template('login.html')

class state:
    TOPIC_OF_SUBSCRIBE = "Nil"
    TOPIC_OF_PUBLISH = "Nil"
    connected = 'false'
    disconnected = 'true'
    location = "Nil"
    locationDetail = "Nil"
    isGateway = 'false'
    isDoor = 'false'
    choice = "any"
    choiceEndp = "any"
    TVpl1 = "TVPlug1"
    TVSta1 = "Click to Reload"
    TVAct1 = 'false'
    TVpl2 = "TVPlug2"
    TVSta2 = "Click to Reload"
    TVAct2 = 'false'
    TVpl3 = "TVPlug3"
    TVSta3 = "Click to Reload"
    TVAct3 = 'false'
    AC1 = "Aircon1"
    ACSta1 = "Click to Reload"
    ACAct1 = 'false'
    AC2 = "Aircon2"
    ACSta2 = "Click to Reload"
    ACAct2 = 'false'
    DEpl1 = "DehumidPlug1"
    DESta1 = "Click to Reload"
    DEAct1 = 'false'
    DEpl2 = "DehumidPlug2"
    DESta2 = "Click to Reload"
    DEAct2 = 'false'
    LT1 = "Light1L11R12"
    LTSta11 = "Click to Reload"
    LTAct11 = 'false'
    LTSta12 = "Click to Reload"
    LTAct12 = 'false'
    LT2 = "Light2L21R22"
    LTSta21 = "Click to Reload"
    LTAct21 = 'false'
    LTSta22 = "Click to Reload"
    LTAct22 = 'false'

    def customCallback(mqttc, userdata, message):

        TVpl1 = "TVPlug1"
        TVpl2 = "TVPlug2"
        TVpl3 = "TVPlug3"
        AC1 = "Aircon1"
        AC2 = "Aircon2"
        DEpl1 = "DehumidPlug1"
        DEpl2 = "DehumidPlug2"
        light1 = "Light1L11R12"
        light2 = "Light2L21R22"
        payload = str(message.payload)
        print(payload)

        if '"ZwCmd": "NODE_RENAME", "Name": "' + TVpl1 + '"' in payload:
            start = payload.find('"NodeID": "') + len('"NodeID": "')
            end = payload.find('", "ZwClass"')
            NodeId = payload[start:end]
            state.TVpl1 = NodeId
            state.TVAct1 = 'true'

        if '"ZwCmd": "NODE_RENAME", "Name": "' + TVpl2 + '"' in payload:
            start = payload.find('"NodeID": "') + len('"NodeID": "')
            end = payload.find('", "ZwClass"')
            NodeId = payload[start:end]
            state.TVpl2 = NodeId
            state.TVAct2 = 'true'

        if '"ZwCmd": "NODE_RENAME", "Name": "' + TVpl3 + '"' in payload:
            start = payload.find('"NodeID": "') + len('"NodeID": "')
            end = payload.find('", "ZwClass"')
            NodeId = payload[start:end]
            state.TVpl3 = NodeId
            state.TVAct3 = 'true'

        if '"ZwCmd": "NODE_RENAME", "Name": "' + AC1 + '"' in payload:
            start = payload.find('"NodeID": "') + len('"NodeID": "')
            end = payload.find('", "ZwClass"')
            NodeId = payload[start:end]
            state.AC1 = NodeId
            state.ACAct1 = 'true'

        if '"ZwCmd": "NODE_RENAME", "Name": "' + AC2 + '"' in payload:
            start = payload.find('"NodeID": "') + len('"NodeID": "')
            end = payload.find('", "ZwClass"')
            NodeId = payload[start:end]
            state.AC2 = NodeId
            state.ACAct2 = 'true'

        if '"ZwCmd": "NODE_RENAME", "Name": "' + DEpl1 + '"' in payload:
            start = payload.find('"NodeID": "') + len('"NodeID": "')
            end = payload.find('", "ZwClass"')
            NodeId = payload[start:end]
            state.DEpl1 = NodeId
            state.DEAct1 = 'true'

        if '"ZwCmd": "NODE_RENAME", "Name": "' + DEpl2 + '"' in payload:
            start = payload.find('"NodeID": "') + len('"NodeID": "')
            end = payload.find('", "ZwClass"')
            NodeId = payload[start:end]
            state.DEpl2 = NodeId
            state.DEAct2 = 'true'

        if '"ZwCmd": "NODE_RENAME", "Name": "' + light1 + '"' in payload:
            start = payload.find('"NodeID": "') + len('"NodeID": "')
            end = payload.find('", "ZwClass"')
            NodeId = payload[start:end]
            state.LT1 = NodeId

        if '"ZwCmd": "NODE_RENAME", "Name": "' + light2 + '"' in payload:
            start = payload.find('"NodeID": "') + len('"NodeID": "')
            end = payload.find('", "ZwClass"')
            NodeId = payload[start:end]
            state.LT2 = NodeId

        if '"ProtoType": 0, "NodeID": "' + state.TVpl1 + '", "Endpoint": "0", "ZwClass": "CLASS_SWITCH_BINARY"' in payload:
            start = payload.find('"CurrSts": "') + len('"CurrSts": "')
            end = payload.find('", "TgtSts"')
            NodeStatus = payload[start:end]
            state.TVSta1 = NodeStatus

        if '"ProtoType": 0, "NodeID": "' + state.TVpl2 + '", "Endpoint": "0", "ZwClass": "CLASS_SWITCH_BINARY"' in payload:
            start = payload.find('"CurrSts": "') + len('"CurrSts": "')
            end = payload.find('", "TgtSts"')
            NodeStatus = payload[start:end]
            state.TVSta2 = NodeStatus

        if '"ProtoType": 0, "NodeID": "' + state.TVpl3 + '", "Endpoint": "0", "ZwClass": "CLASS_SWITCH_BINARY"' in payload:
            start = payload.find('"CurrSts": "') + len('"CurrSts": "')
            end = payload.find('", "TgtSts"')
            NodeStatus = payload[start:end]
            state.TVSta3 = NodeStatus

        if '"ProtoType": 0, "NodeID": "' + state.DEpl1 + '", "Endpoint": "0", "ZwClass": "CLASS_SWITCH_BINARY"' in payload:
            start = payload.find('"CurrSts": "') + len('"CurrSts": "')
            end = payload.find('", "TgtSts"')
            NodeStatus = payload[start:end]
            state.DESta1 = NodeStatus

        if '"ProtoType": 0, "NodeID": "' + state.DEpl2 + '", "Endpoint": "0", "ZwClass": "CLASS_SWITCH_BINARY"' in payload:
            start = payload.find('"CurrSts": "') + len('"CurrSts": "')
            end = payload.find('", "TgtSts"')
            NodeStatus = payload[start:end]
            state.DESta2 = NodeStatus

        if '"ProtoType": 0, "NodeID": "' + state.LT1 + '", "Endpoint": "1", "ZwClass": "CLASS_SWITCH_BINARY", "ZwCmd": "SWITCH_BINARY_REPORT", "' in payload:
            start = payload.find('"CurrSts": "') + len('"CurrSts": "')
            end = payload.find('", "TgtSts"')
            NodeStatus = payload[start:end]
            state.LTSta11 = NodeStatus
            state.LTAct11 = 'true'

        if '"ProtoType": 0, "NodeID": "' + state.LT1 + '", "Endpoint": "2", "ZwClass": "CLASS_SWITCH_BINARY", "ZwCmd": "SWITCH_BINARY_REPORT", "' in payload:
            start = payload.find('"CurrSts": "') + len('"CurrSts": "')
            end = payload.find('", "TgtSts"')
            NodeStatus = payload[start:end]
            state.LTSta12 = NodeStatus
            state.LTAct12 = 'true' 

        if '"ProtoType": 0, "NodeID": "' + state.LT2 + '", "Endpoint": "1", "ZwClass": "CLASS_SWITCH_BINARY", "ZwCmd": "SWITCH_BINARY_REPORT", "' in payload:
            start = payload.find('"CurrSts": "') + len('"CurrSts": "')
            end = payload.find('", "TgtSts"')
            NodeStatus = payload[start:end]
            state.LTSta21 = NodeStatus
            state.LTAct21 = 'true'

        if '"ProtoType": 0, "NodeID": "' + state.LT2 + '", "Endpoint": "2", "ZwClass": "CLASS_SWITCH_BINARY", "ZwCmd": "SWITCH_BINARY_REPORT", "' in payload:
            start = payload.find('"CurrSts": "') + len('"CurrSts": "')
            end = payload.find('", "TgtSts"')
            NodeStatus = payload[start:end]
            state.LTSta22 = NodeStatus
            state.LTAct22 = 'true' 

        if '"ProtoType": 0, "NodeID": "' + state.AC1 + '"' in payload:
            start = payload.find('"CurrVal": "') + len('"CurrVal": "')
            end = payload.find('", "TgtVal"')
            NodeStatusNumber = payload[start:end]
            if NodeStatusNumber == '0':
                state.ACSta1 = "Off"
            if NodeStatusNumber == '255':
                state.ACSta1 = "On"

        if '"ProtoType": 0, "NodeID": "' + state.AC2 + '"' in payload:
            start = payload.find('"CurrVal": "') + len('"CurrVal": "')
            end = payload.find('", "TgtVal"')
            NodeStatusNumber = payload[start:end]
            if NodeStatusNumber == '0':
                state.ACSta2 = "Off"
            if NodeStatusNumber == '255':
                state.ACSta1 = "On"

        if '"FailedList": [ ' + state.TVpl1+' ]' in payload:
            state.TVSta1 = "failed"
        if '"FailedList": [ ' + state.TVpl2+' ]' in payload:
            state.TVSta2 = "failed"
        if '"FailedList": [ ' + state.TVpl3+' ]' in payload:
            state.TVSta3 = "failed"
        if '"FailedList": [ ' + state.DEpl1+' ]' in payload:
            state.DESta1 = "failed"
        if '"FailedList": [ ' + state.DEpl2+' ]' in payload:
            state.DESta2 = "failed"
        if '"FailedList": [ ' + state.LT1+' ]' in payload:
            state.LTSta11 = "failed"
        if '"FailedList": [ ' + state.LT2+' ]' in payload:
            state.LTSta21 = "failed"
        if '"FailedList": [ ' + state.AC1 + ' ]' in payload:
            state.ACSta1 = "failed"
        if '"FailedList": [ ' + state.AC2 + ' ]' in payload:
            state.ACSta2 = "failed"

# connecting to locations
@app.route('/Angmokio', methods=["POST", "GET"])
def angmokioGW():
    state.TOPIC_OF_SUBSCRIBE = "InsertTopict"
    state.TOPIC_OF_PUBLISH = "InsertTopic"
    state.isGateway = 'true'
    state.isDoor = 'false'
    mqttc.connect()
    mqttc.subscribe(state.TOPIC_OF_SUBSCRIBE, 0, state.customCallback)
    state.disconnected = 'false'
    state.connected = 'true'
    state.location = 'Ang Mo Kio'
    state.locationDetail = 'Ang Mo Kio Gateway'
    return state.TOPIC_OF_PUBLISH

@app.route('/AngmokioDoor', methods=["POST", "GET"])
def angmokioDoor():
    state.TOPIC_OF_SUBSCRIBE = "InsertTopic"
    state.TOPIC_OF_PUBLISH = "InsertTopic"
    state.isGateway = 'false'
    state.isDoor = 'true'
    mqttc.connect()
    mqttc.subscribe(state.TOPIC_OF_SUBSCRIBE, 0, state.customCallback)
    state.disconnected = 'false'
    state.connected = 'true'
    state.location = 'Ang Mo Kio'
    state.locationDetail = 'Ang Mo Kio Door'
    return state.TOPIC_OF_PUBLISH

@app.route('/Tampines', methods=["POST", "GET"])
def tampinesGW():
    state.TOPIC_OF_SUBSCRIBE = "InsertTopic"
    state.TOPIC_OF_PUBLISH = "InsertTopic"
    state.isGateway = 'true'
    state.isDoor = 'false'
    mqttc.connect()
    mqttc.subscribe(state.TOPIC_OF_SUBSCRIBE, 0, state.customCallback)
    state.disconnected = 'false'
    state.connected = 'true'
    state.location = 'Tampines'
    state.locationDetail = 'Tampines Gateway'
    return state.TOPIC_OF_PUBLISH

@app.route('/TampinesDoor', methods=["POST", "GET"])
def tampinesDoor():
    state.TOPIC_OF_SUBSCRIBE = "InsertTopic"
    state.TOPIC_OF_PUBLISH = "InsertTopic"
    state.isGateway = 'false'
    state.isDoor = 'true'
    mqttc.connect()
    mqttc.subscribe(state.TOPIC_OF_SUBSCRIBE, 0, state.customCallback)
    state.disconnected = 'false'
    state.connected = 'true'
    state.location = 'Tampines'
    state.locationDetail = 'Tampines Door'
    return state.TOPIC_OF_PUBLISH

@app.route('/Bedoknorth', methods=["POST", "GET"])
def bedokNorthGW():
    state.TOPIC_OF_SUBSCRIBE = "InsertTopic"
    state.TOPIC_OF_PUBLISH = "InsertTopic"
    state.isGateway = 'true'
    state.isDoor = 'false'
    mqttc.connect()
    mqttc.subscribe(state.TOPIC_OF_SUBSCRIBE, 0, state.customCallback)
    state.disconnected = 'false'
    state.connected = 'true'
    state.location = 'Bedok North'
    state.locationDetail = 'Bedok North Gateway'
    return state.TOPIC_OF_PUBLISH

@app.route('/BedoknorthDoor', methods=["POST", "GET"])
def bedokNorthDoor():
    state.TOPIC_OF_SUBSCRIBE = "InsertTopic"
    state.TOPIC_OF_PUBLISH = "InsertTopic"
    state.isGateway = 'false'
    state.isDoor = 'true'
    mqttc.connect()
    mqttc.subscribe(state.TOPIC_OF_SUBSCRIBE, 0, state.customCallback)
    state.disconnected = 'false'
    state.connected = 'true'
    state.location = 'Bedok North'
    state.locationDetail = 'Bedok North Door'
    return state.TOPIC_OF_PUBLISH

@app.route('/Tanglinhalt', methods=["POST", "GET"])
def tanglinHaltGW():
    state.TOPIC_OF_SUBSCRIBE = "InsertTopic"
    state.TOPIC_OF_PUBLISH = "InsertTopic"
    state.isGateway = 'true'
    state.isDoor = 'false'
    mqttc.connect()
    mqttc.subscribe(state.TOPIC_OF_SUBSCRIBE, 0, state.customCallback)
    state.disconnected = 'false'
    state.connected = 'true'
    state.location = 'Tanglin Halt'
    state.locationDetail = 'Tanglin Halt Gateway'
    return state.TOPIC_OF_PUBLISH

@app.route('/TanglinhaltDoor', methods=["POST", "GET"])
def tanglinHaltDoor():
    state.TOPIC_OF_SUBSCRIBE = "InsertTopic"
    state.TOPIC_OF_PUBLISH = "InsertTopic"
    state.isGateway = 'false'
    state.isDoor = 'true'
    mqttc.connect()
    mqttc.subscribe(state.TOPIC_OF_SUBSCRIBE, 0, state.customCallback)
    state.disconnected = 'false'
    state.connected = 'true'
    state.location = 'Tanglin Halt'
    state.locationDetail = 'Tanglin Halt Door'
    return state.TOPIC_OF_PUBLISH

# disconnect from locations
@app.route('/Disconnect', methods=["POST", "GET"])
def disconnect():
    mqttc.disconnect()
    resetWebsite()
    return state.TOPIC_OF_PUBLISH

@app.route('/getNodeListFunction')
def getNodeListFunction():
    raw_data = {"EVENT": "GET_NODE_LIST"}
    message = json.dumps(raw_data)
    send(message)
    return raw_data

def onPlug():
    raw_data = {"EVENT": "ZW_SWITCH_BINARY_SET", "NODE_ID": state.choice, "ENDPOINT_ID": 0, "SWITCH": "ON"}
    message = json.dumps(raw_data)
    send(message)
    return raw_data

def offPlug():
    raw_data = {"EVENT": "ZW_SWITCH_BINARY_SET", "NODE_ID": state.choice, "ENDPOINT_ID": 0, "SWITCH": "OFF"}
    message = json.dumps(raw_data)
    send(message)
    return raw_data

@app.route('/onTV1Function')
def onTV1Plug():
    state.choice = state.TVpl1
    onPlug()

@app.route('/offTV1Function')
def offTV1Plug():
    state.choice = state.TVpl1
    offPlug()

@app.route('/onTV2Function')
def onTV2Plug():
    state.choice = state.TVpl2
    onPlug()

@app.route('/offTV2Function')
def offTV2Plug():
    state.choice = state.TVpl2
    offPlug()

@app.route('/onTV3Function')
def onTV3Plug():
    state.choice = state.TVpl3
    onPlug()

@app.route('/offTV3Function')
def offTV3Plug():
    state.choice = state.TVpl3
    offPlug()

def onAC():
    raw_data = {"EVENT": "ZW_BASIC_SET", "NODE_ID": state.choice, "ENDPOINT_ID": 0, "BASIC_VALUE": 255}
    message = json.dumps(raw_data)
    send(message)
    time.sleep(3)
    getAC()
    return message

def offAC():
    raw_data = {"EVENT": "ZW_BASIC_SET", "NODE_ID": state.choice, "ENDPOINT_ID": 0, "BASIC_VALUE": 0}
    message = json.dumps(raw_data)
    send(message)
    time.sleep(3)
    getAC()
    return message

def getAC():
    raw_data = {"EVENT": "ZW_BASIC_GET", "NODE_ID": state.choice, "ENDPOINT_ID": 0}
    message = json.dumps(raw_data)
    send(message)

@app.route('/onAC1Function')
def onAC1():
    state.choice = state.AC1
    onAC()

@app.route('/offAC1Function')
def offAC1():
    state.choice = state.AC1
    offAC()

@app.route('/onAC2Function')
def onAC2():
    state.choice = state.AC2
    onAC()

@app.route('/offAC2Function')
def offAC2():
    state.choice = state.AC2
    offAC()

@app.route('/onDE1Function')
def onDE1Plug():
    state.choice = state.DEpl1
    onPlug()

@app.route('/offDE1Function')
def offDE1Plug():
    state.choice = state.DEpl1
    offPlug()

@app.route('/onDE2Function')
def onDE2Plug():
    state.choice = state.DEpl2
    onPlug()

@app.route('/offDE2Function')
def offDE2Plug():
    state.choice = state.DEpl2
    offPlug()

def onLT():
    raw_data = {"EVENT": "ZW_SWITCH_BINARY_SET", "NODE_ID": state.choice, "ENDPOINT_ID": state.choiceEndp, "SWITCH": "ON"}
    message = json.dumps(raw_data)
    send(message)
    time.sleep(4)
    getLT()
    return raw_data

def offLT():
    raw_data = {"EVENT": "ZW_SWITCH_BINARY_SET", "NODE_ID": state.choice, "ENDPOINT_ID": state.choiceEndp, "SWITCH": "OFF"}
    message = json.dumps(raw_data)
    send(message)
    time.sleep(4)
    getLT()
    return raw_data

def getLT():
    raw_data = {"EVENT": "ZW_SWITCH_BINARY_GET", "NODE_ID": state.choice, "ENDPOINT_ID": state.choiceEndp}
    message = json.dumps(raw_data)
    send(message)
    return raw_data

@app.route('/onLT11Function')
def onLT11():
    state.choice = state.LT1
    state.choiceEndp = 1
    onLT()

@app.route('/offLT11Function')
def offLT11():
    state.choice = state.LT1
    state.choiceEndp = 1
    offLT()

@app.route('/onLT12Function')
def onLT12():
    state.choice = state.LT1
    state.choiceEndp = 2
    onLT()

@app.route('/offLT12Function')
def offLT12():
    state.choice = state.LT1
    state.choiceEndp = 2
    offLT()

@app.route('/onLT21Function')
def onLT21():
    state.choice = state.LT2
    state.choiceEndp = 1
    onLT()

@app.route('/offLT21Function')
def offLT21():
    state.choice = state.LT2
    state.choiceEndp = 1
    offLT()

@app.route('/onLT22Function')
def onLT22():
    state.choice = state.LT2
    state.choiceEndp = 2
    onLT()

@app.route('/offLT22Function')
def offLT22():
    state.choice = state.LT2
    state.choiceEndp = 2
    offLT()

@app.route('/onnDR1')
def onnDR1():
    raw_data = {"command": "open"}
    message = json.dumps(raw_data)
    send(message)
    return message

@app.route('/home', methods=["POST", "GET"])
def home():
    if not g.user:
        return redirect(url_for('login'))

    return render_template('ospacev1.html', connected=state.connected, disconnected=state.disconnected, location=state.location, TVpl1=state.TVpl1, TVpl2=state.TVpl2, TVpl3=state.TVpl3, 
        TVsta1=state.TVSta1, TVsta2=state.TVSta2, TVsta3=state.TVSta3, TVact1=state.TVAct1, TVact2=state.TVAct2, TVact3 = state.TVAct3, AC1=state.AC1, AC2=state.AC2, ACsta1=state.ACSta1,
        ACsta2=state.ACSta2, ACact1=state.ACAct1, ACact2=state.ACAct2, DEpl1=state.DEpl1, DEpl2=state.DEpl2, DEsta1=state.DESta1, DEsta2=state.DESta2, DEact1=state.DEAct1, DEact2=state.DEAct2,
        isGateway=state.isGateway, isDoor=state.isDoor, locationDetail=state.locationDetail, LT1=state.LT1, LTSta11=state.LTSta11, LTAct11=state.LTAct11, LTSta12=state.LTSta12, LTAct12=state.LTAct12,
        LT2=state.LT2, LTSta21=state.LTSta21, LTAct21=state.LTAct21, LTSta22=state.LTSta22 , LTAct22=state.LTAct22)

mqttc = AWSIoTMQTTClient("OSPACE-control")
mqttc.configureEndpoint("UNIQUE-ats.iot.ap-southeast-1.amazonaws.com", 8883)
mqttc.configureCredentials("./certs/rootCA.pem", "./certs/private.pem.key", "./certs/certificate.pem.crt")
mqttc.configureAutoReconnectBackoffTime(1, 32, 20)
mqttc.configureOfflinePublishQueueing(-1)
mqttc.configureDrainingFrequency(2)
mqttc.configureConnectDisconnectTimeout(10)
mqttc.configureMQTTOperationTimeout(5)

def json_encode(string):
    return json.dumps(string)

def send(message):
    mqttc.publish(state.TOPIC_OF_PUBLISH, message, 0)

# @app.route('/resetWebsite')
def resetWebsite():
    state.TOPIC_OF_SUBSCRIBE = "Nil"
    state.TOPIC_OF_PUBLISH = "Nil"
    state.location = "Nil"
    state.locationDetail = "Nil"
    state.isGateway = 'false'
    state.isDoor = 'false'
    state.disconnected = 'true'
    state.connected = 'false'
    state.TVpl1 = "TVPlug1"
    state.TVSta1 = "Click to Reload"
    state.TVAct1 = 'false'
    state.TVpl2 = "TVPlug2"
    state.TVSta2 = "Click to Reload"
    state.TVAct2 = 'false'
    state.TVpl3 = "TVPlug3"
    state.TVSta3 = "Click to Reload"
    state.TVAct3 = 'false'
    state.AC1 = "Aircon1"
    state.ACSta1 = "Click to Reload"
    state.ACAct1 = 'false'
    state.AC2 = "Aircon2"
    state.ACSta2 = "Click to Reload"
    state.ACAct2 = 'false'
    state.DEpl1 = "DehumidPlug1"
    state.DESta1 = "Click to Reload"
    state.DEAct1 = 'false'
    state.DEpl2 = "DehumidPlug2"
    state.DESta2 = "Click to Reload"
    state.DEAct2 = 'false'
    state.LT1 = "Light1L11R12"
    state.LTSta11 = "Click to Reload"
    state.LTAct11 = 'false'
    state.LTSta12 = "Click to Reload"
    state.LTAct12 = 'false'
    state.LT2 = "Light2L21R22"
    state.LTSta21 = "Click to Reload"
    state.LTAct21 = 'false'
    state.LTSta22 = "Click to Reload"
    state.LTAct22 = 'false'
    return True    

if __name__ == "__main__":
    app.run(debug=True)
