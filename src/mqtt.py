#coding=utf-8

from time import sleep
import threading
import paho.mqtt.client as mqtt
import numpy as np
import random
import IP_Functions

# mqtt 中间件信息
mqtt_broker_ip = "mqtt.iecube.com.cn"
mqtt_broker_port = 1883
mqtt_broker_username = ""
mqtt_broker_passwd = ""

# ------------------------------------------------------------------------
# mqtt callback functions
# ------------------------------------------------------------------------
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

# ------------------------------------------------------------------------
# QUBE_MQTT_CtrlLogic
# ------------------------------------------------------------------------

def Mqtt_Working_Thread():

    while(True):
        ClientID = "MqttIPReporter/" + str(random.random()*10000)
        client = mqtt.Client(ClientID)
        client.on_connect = on_connect
        client.on_message = on_message
        client.username_pw_set(mqtt_broker_username,mqtt_broker_passwd)
        client.connect(mqtt_broker_ip, mqtt_broker_port, 60)

        # 启动 mqtt client
        client.loop_start()

        threadRunning = True

        while(threadRunning):
            try:
                hostname = IP_Functions.get_host_name()
                IP = IP_Functions.get_host_ip()
                client.publish("MqttIPReporter/" + hostname + "/IP", IP)
                print(hostname + " : " + IP)
                # Report IP every 5 seconds
                sleep(5)
                pass
            except expression as identifier:
                threadRunning = False
                print(identifier)
                pass


        # 停止 mqtt client
        client.loop_stop()

        # Reconnect Timeout = 5s
        sleep(5)


if __name__ == '__main__':
    Mqtt_Working_Thread()