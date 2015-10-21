__author__ = 'hut-dell'

import zmq
import random
import sys
import time
import threading

class StartForwarders(threading.Thread):
    def __init__(self, direction):
        threading.Thread.__init__(self)
        self.direction = direction

    def run(self):
        didrun = False
        print "self.direction = " + str(self.direction)
        print ""
        print ""
        if(self.direction == "UnityToOpencog"):


            try:
                context = zmq.Context(1)
                # Unity Pub Facing
                frontend = context.socket(zmq.SUB)
                frontend.bind("tcp://*:5559")

                frontend.setsockopt(zmq.SUBSCRIBE, "")

                # Python Sub Facing
                backend = context.socket(zmq.PUB)
                backend.bind("tcp://*:5560")
                print "launching UnityToOpenCog forwarder Port:5559 for PUB  Port:5560 for SUB "
                didrun = True
                zmq.device(zmq.FORWARDER, frontend, backend)
            except Exception, e:
                print e
                print "bringing down zmq device"
            finally:
                pass
                frontend.close()
                backend.close()
                context.term()

        if(self.direction == "OpencogToUnity"):


            try:
                context = zmq.Context(1)
                # Python Sub Facing
                frontend = context.socket(zmq.SUB)
                frontend.bind("tcp://*:5561")

                frontend.setsockopt(zmq.SUBSCRIBE, "")

                # Unity Sub facing
                backend = context.socket(zmq.PUB)
                backend.bind("tcp://*:5562")
                print "launching OpenCogToUnity forwarder Port:5561 for PUB  Port:5562 for SUB"
                didrun = True
                zmq.device(zmq.FORWARDER, frontend, backend)
            except Exception, e:
                print e
                print "bringing down zmq device"
            finally:
                pass
                frontend.close()
                backend.close()
                context.term()
        if(didrun == False):
            print "did not run " + str(self.direction)


thread1 = StartForwarders("UnityToOpencog")
thread2 = StartForwarders("OpencogToUnity")
thread3 = StartForwarders("Random Bullshit")

thread1.start()
thread2.start()
thread3.start()

kount = 0
#print ("starting while(true) loop")

while(True):
    kount = kount + 1
    print kount
    time.sleep(5)

