"""
    Helper functions for data gathering
"""
import os
from tokenize import single_quoted
import requests
import logging
from dotenv import load_dotenv
import json
import time


load_dotenv('vars.env')
logging.basicConfig(level=logging.WARNING)

ALL_PAIRS_ENDPOINT = os.getenv('ALL_PAIRS_ENDPOINT')
SINGLE_PAIR_ENDPOINT = os.getenv('SINGLE_PAIR_ENDPOINT')
ASSET_IDS = os.getenv('ASSET_IDS')
THROTTLE_TIME = os.getenv('TIME_BETWEEN_REQUESTS')

assert ALL_PAIRS_ENDPOINT is not None, "Endpoint not found"
assert SINGLE_PAIR_ENDPOINT is not None, "Endpoint not found"


class Helper(object):
    """
    Params: Assets IDs 
    Return: Request response in JSON format, or None
    """
    @staticmethod
    def queryPair(pipe_A, pipe_B):
        while True:
            IDs = pipe_A.recv()
            url = SINGLE_PAIR_ENDPOINT.format(IDs[0], IDs[1])
            resp = requests.get(url)
            if resp is not None:
                pipe_B.send(json.loads(resp.text))
        
    """
    Params: Query Response - JSON
    Return: Asset price in USD
    """
    @staticmethod
    def getPrice(pipe_A, pipe_B):
        while True:
            data = pipe_A.recv()
            logging.info(data)
            pipe_B.send((data['basePrice'], data['baseSymbol']))
        

if __name__ == "__main__":
    print("Helper file! Do not run directly.")
    exit(-1)