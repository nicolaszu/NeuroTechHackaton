import argparse
import math
import numpy as np
from pythonosc import dispatcher
from pythonosc import osc_server
import matplotlib.pyplot as plt

num= list(range(0, 100))
MuseArrayDifference=[]
MuserArrayDifferenceCompare=[]
MuseArrayDifferenceMovingAverageArray=[]
global counter
counter=0
def eeg_handler(unused_addr, args, ch1, ch2, ch3, ch4):
    
   
    right = ch3 # channel 3 is right
    left = ch2 #channel 2 is left
    differenceLeftRight= left-right
    biggerSide = ch3>ch2 # if channel 3 is bigger than right side is bigger then true then its green
    MuseArrayDifference.append(differenceLeftRight)

    if (biggerSide):
        print("Right is larger")
    else:
        print ("Left side is bigger")
    
   


    if(len(MuseArrayDifference)==10):
                                
        MuseArrayDifferenceMovingAverage= np.convolve(MuseArrayDifference, np.ones((10,))/10, mode='valid') 
        MuseArrayDifferenceMovingAverageArray.append(MuseArrayDifferenceMovingAverage)
        MuserArrayDifferenceCompare.append(differenceLeftRight)
        MuseArrayDifference.pop()
        print(len(MuseArrayDifferenceMovingAverageArray))


    if(len(MuseArrayDifferenceMovingAverageArray)==100):
        PlotArrayMA= MuseArrayDifferenceMovingAverageArray.copy()
        PlotArrayNormal= MuserArrayDifferenceCompare.copy()
        print("start")
        print(len(num))
        print(len(PlotArrayMA))
        print(len(PlotArrayNormal))
        print("end")
        plt.plot(num,PlotArrayMA, label='Moving Average')
        plt.scatter(num,PlotArrayNormal, label='Normal numbers')

        plt.xlabel('Alpha difference')
        plt.ylabel('')
        plt.title('Moving Average of 100')
        plt.legend()
        plt.show()



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip",
                        default="127.0.0.1",
                        help="The ip to listen on")
    parser.add_argument("--port",
                        type=int,
                        default=7000,
                        help="The port to listen on")
    args = parser.parse_args()

    dispatcher = dispatcher.Dispatcher()
    dispatcher.map("/debug", print)
    dispatcher.map("/muse/elements/alpha_relative", eeg_handler, "EEG")

    server = osc_server.ThreadingOSCUDPServer(
        (args.ip, args.port), dispatcher)
    print("Serving on {}".format(server.server_address))
    server.serve_forever()

