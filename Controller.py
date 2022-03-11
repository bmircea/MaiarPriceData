"""
    Main process
    #TODO: 1. Outside control mechanism
           2. Persistent Storage
"""
import time
from Helper import Helper, ASSET_IDS
from multiprocessing import Process, Pipe
import logging

logging.basicConfig(level=logging.INFO)

assets = str(ASSET_IDS).split(',')

def fillPipe(pipe_end, assets): 
    while True:
        for i in range(len(assets)):
            asset, quote = assets[i].split('|')
            #logging.info("Fill: " + asset + ' ' + quote)        
            pipe_end.send((asset, quote))
            time.sleep(1)

def receiveFromPipe(pipe_end):
    while True:
        logging.info("Price: " + str(pipe_end.recv()))

if __name__ == "__main__":
    assets_A, assets_B = Pipe()
    data_A, data_B = Pipe()
    prices_A, prices_B = Pipe() 

    p1 = Process(target=fillPipe, args=(assets_A, assets))
    p2 = Process(target=Helper.queryPair, args=(assets_B, data_A))
    p3 = Process(target=Helper.getPrice, args=(data_B, prices_A))
    p4 = Process(target=receiveFromPipe, args=(prices_B,))
    
    p1.start()
    p2.start()
    p3.start()
    p4.start()
