"""
    Main process
    #TODO: 1. Outside control mechanism
           2. Persistent Storage
"""
import time
from Helper import Helper, ASSET_IDS, THROTTLE_TIME
from multiprocessing import Process, Pipe
import logging

logging.basicConfig(level=logging.WARNING)

assets = str(ASSET_IDS).split(',')

def fillPipe(pipe_end, assets): 
    while True:
        for i in range(len(assets)):
            asset, quote = assets[i].split('|')
            logging.info("Fill: " + asset + ' ' + quote)        
            pipe_end.send((asset, quote))
            time.sleep(float(THROTTLE_TIME))

def receiveFromPipe(pipe_end):
    while True:
        resp = pipe_end.recv()
        logging.info("Price: {0} {1}".format(str(resp[1]), str(resp[0])))
        # TODO 2.

def startProcesses(processList):
    for process in processList:
        process.start()

def stopProcesses(processList):
    for process in processList:
        process.stop()


if __name__ == "__main__":
    assets_A, assets_B = Pipe()
    data_A, data_B = Pipe()
    prices_A, prices_B = Pipe() 
    processes = []

    fillProcess = Process(target=fillPipe, args=(assets_A, assets))
    queryProcess = Process(target=Helper.queryPair, args=(assets_B, data_A))
    priceProcess = Process(target=Helper.getPrice, args=(data_B, prices_A))
    receiverProcess = Process(target=receiveFromPipe, args=(prices_B,))

    processes.append(fillProcess)
    processes.append(queryProcess)
    processes.append(priceProcess)
    processes.append(receiverProcess)

    startProcesses(processes)