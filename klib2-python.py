#-*- coding: utf-8 -*-
import os
from subprocess import CREATE_NEW_CONSOLE
import sys
import time
import threading
import random
import numpy as np
import csv
import datetime
import time
import binascii
import base64
import os
import socketio
import requests

from socket import *
from select import select

import codecs


# standard Python
sio = socketio.Client()

sio.connect('http://localhost:3004')

@sio.event
def connect():
    print("I'm connected!")

@sio.event
def message(data):
    print('I received a message!')

@sio.on('send_footStatus')
def on_message(data):
    print('I received a message!2')

class KLib():
    def __init__(self,_server_ip = "127.0.0.1", _port = 3800):
        self.nrow = 0
        self.ncol = 0
        self.datasize = 0
        self.adc = None
        self.port = _port
        self.server_ip = _server_ip
        self.device = ""
        self.sensor = ""
        self.adc = []

        self.buf = None
        self.BufSize = 5000
        self.addr = None
        self.client_socket = None
        self.result = None

        self.client_socket_connection = False

    #TcpIP 연결 시도
    def init(self):
        try:
            self.addr = (self.server_ip, self.port) #server address 정보
            self.client_socket = socket(AF_INET, SOCK_STREAM) #소켓 정보

            self.client_socket.connect(self.addr) # tcpip연결
        except Exception as e:
            print('Failed to connect TCP/IP!')
            self.client_socket_connection = False
            return False
        self.client_socket_connection = True

        resp = self.client_socket.recv(self.BufSize) #버퍼 받기

        self.buf = resp
        self.datasize = 5000
        self.BufSize = self.datasize +200
        sp = 0


        #header가 2개 이상이 아닌경우 패킷이 다안들어왔을 가능성이 있음
        while(1):
            if(len(self.buf) > self.BufSize):
                break
            resp = self.client_socket.recv(self.BufSize)
            self.buf = self.buf + resp

             #header 위치 찾기

            while(1):
                sp = self.buf.index(0x7e,sp)
                if(self.buf[sp+1] == 0x7e and self.buf[sp+2]== 0x7e and self.buf[sp+3] == 0x7e):
                    self.nrow = int.from_bytes(self.buf[88:91],byteorder='little')
                    self.ncol = int.from_bytes(self.buf[92:95],byteorder='little')
                    self.datasize = self.nrow * self.ncol
                    self.BufSize = self.datasize + 200
                    break




        self.device = self.buf[4:28]
        self.sensor = self.buf[28:52]
        self.nrow = int.from_bytes(self.buf[88:91],byteorder='little')
        self.ncol = int.from_bytes(self.buf[92:95],byteorder='little')
        self.datasize = self.nrow * self.ncol
        self.BufSize

         #header, tail을 뺀 버퍼를 result에 집어넣음
        self.result = self.buf[sp + 4 : sp + self.datasize]

        # rawdata array 생성
        for i in range(96,self.datasize+96):
            self.adc.append(int(self.buf[i]))



    def check_tcp_connection(self):
        if(self.client_socket_connection == True):
            return True
        else:
            return False
    #서버와 tcp 연결 시도
    def start(self):
        self.init()
    #서봐의 tcp 연결 끊기
    def stop(self):
        self.client_socket.close()
        self.client_socket_connection = False

    #패킷읽기
    def read(self):
        self.buf  = self.buf + self.client_socket.recv(self.BufSize)

        #header가 2개 이상이 아닌경우 패킷이 다안들어왔을 가능성이 있음
        while(1):
            if(len(self.buf) > self.BufSize):
                break
            resp = self.client_socket.recv(self.BufSize)
            self.buf = self.buf + resp

        #header 위치 찾기
        sp = 0
        while(1):
            sp = self.buf.index(0x7e,sp)
            if(self.buf[sp+1] == 0x7e and self.buf[sp+2]== 0x7e and self.buf[sp+3] == 0x7e):
                break

        for i in range(96+sp,self.datasize+96+sp):
             self.adc[i-96-sp] = int(self.buf[i])

        # 읽어들인 adc 데이터 부분 삭제
        self.buf = self.buf[self.datasize+96+sp:]


    def printadc(self):
        os.system('cls')
        write_str = ""
        for i in range(self.nrow):
            # write_str = ""
            for j in range(self.ncol):
                write_str = write_str + " " + str(self.adc[i*self.ncol + j])
            # print(write_str)
            foot = 'foot'
            footNum= 'footNum'

        print(write_str)
        sio.emit('send_footStatus', {foot: write_str})
        print()


if __name__ == "__main__":
    def worker():
        klib = KLib("127.0.0.1", 3800)
        tick = 0
        FPS = 0
        prevTime = time.time()

        klib.start()
        while(1):

            klib.read()
            klib.printadc()
            tick = tick + 1
            #FPS 계산
            curTime = time.time()
            if curTime - prevTime > 1 :
                FPS = tick
                prevTime = curTime
                tick = 0
            print("FPS : ", FPS)
            foot = 'foot'
            footNum= 'footNum'
            sio.emit('send_footStatus', {footNum: 0,foot: "end"})
            time.sleep(20)


    def schedule(interval, f, wait=True):
        base_time = time.time()
        next_time = 0
        while True:
            t = threading.Thread(target=f)
            t.start()
            if wait:
                t.join()
            next_time = ((base_time - time.time()) % interval) or interval
            time.sleep(next_time)

    schedule(20,worker)




    # while(1):
    #     klib.read()
    #     klib.printadc()
    #     tick = tick + 1
    #     #FPS 계산
    #     curTime = time.time()
    #     if curTime - prevTime > 1 :
    #         FPS = tick
    #         prevTime = curTime
    #         tick = 0
    #     print("FPS : ", FPS)
    #     foot = 'foot'
    #     footNum= 'footNum'
    #     sio.emit('send_footStatus', {footNum: 0,foot: "end"})
