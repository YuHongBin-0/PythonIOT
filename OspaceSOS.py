from flask import current_app
import pywhatkit as pwt
from datetime import date, datetime
import json
import time
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient


def json_encode(string):
    return json.dumps(string)

def send(message):
    myMQTTClient.publish(state.TOPIC_OF_PUBLISH, message, 0)


mqttc = AWSIoTMQTTShadowClient("myClientID")
mqttc.configureEndpoint("UNIQUE-ats.iot.ap-southeast-1.amazonaws.com", 8883)
mqttc.configureCredentials("./certs/rootCA.pem", "./certs/private.pem.key", "./certs/certificate.pem.crt")
mqttc.configureAutoReconnectBackoffTime(1, 32, 20)
mqttc.configureConnectDisconnectTimeout(10)
mqttc.configureMQTTOperationTimeout(5)
persistentSubShadow = mqttc.createShadowHandlerWithName("PersistentSubShadow", True)
myMQTTClient = mqttc.getMQTTConnection()

class state:

    AMK_OF_SUBSCRIBE = "InsertTopic"
    BDK_OF_SUBSCRIBE = "InsertTopic"
    TMP_OF_SUBSCRIBE = "InsertTopic"
    TLH_OF_SUBSCRIBE = "InsertTopic"
    TOPIC_OF_PUBLISH = "nil"

    looping = True

    a = 0

    def customCallback(mqttc, userdata, message):
        payload = str(message.payload)
        print(payload)

        if '"CLASS_SWITCH_BINARY", "ZwCmd": "SWITCH_BINARY_REPORT", "CurrSts": "On"' in payload:
            now = datetime.now()
            currentHour = int(now.strftime("%H"))
            print(currentHour)
            currentMinute = int(now.strftime("%M"))
            currentMin = currentMinute + 2
            if currentMinute == 60 :
                currentMin = 00
                currentHour =  currentHour + 1
            
            if currentMinute == 61 :
                currentMin = int('01')
                currentHour =  currentHour + 1
            print(currentMin)
            time.sleep(1)
            # pwt.sendwhatmsg('+65 98671339', 'SENDING MESSAGES USING PYWHATKIT', currentHour, currentMin, 15, True, 3)


mqttc.connect()
myMQTTClient.subscribe(state.BDK_OF_SUBSCRIBE, 0, state.customCallback)
print('connected to bdk')
myMQTTClient.subscribe(state.TMP_OF_SUBSCRIBE, 0, state.customCallback)
print('connected to tmp')
myMQTTClient.subscribe(state.AMK_OF_SUBSCRIBE, 0, state.customCallback)  
print('connected to amk')

print('start sleeping')

state.TOPIC_OF_PUBLISH = 'InsertTopic'




while True:
    print("Looping")
    time.sleep(60)
    print('sending message')

    myMQTTClient.subscribe(state.BDK_OF_SUBSCRIBE, 0, state.customCallback)
    print('connected to bdk')
    myMQTTClient.subscribe(state.TMP_OF_SUBSCRIBE, 0, state.customCallback)
    print('connected to tmp')
    myMQTTClient.subscribe(state.AMK_OF_SUBSCRIBE, 0, state.customCallback)  
    print('connected to amk')

    state.a = state.a + 1 
    print(state.a)
    if (state.a == 30):

        raw_data = {"EVENT": "ZW_SWITCH_BINARY_SET", "NODE_ID": 7, "ENDPOINT_ID": 0, "SWITCH": "ON"}
        message = json.dumps(raw_data)
        send(message)
        state.a = 0
