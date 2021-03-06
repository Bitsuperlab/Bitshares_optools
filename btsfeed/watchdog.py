#!/usr/bin/env python3
# coding=utf8 sw=1 expandtab ft=python

import os
import sys
from datetime import datetime
import time
from bts import BTS
import operator
import json
from math import fabs

## Loading Config
config_file = open("config.json")
config = json.load(config_file)
config_file.close()

## Opening RPC to wallet
client = BTS(
    config["client"]["rpc_user"],
    config["client"]["rpc_password"],
    config["client"]["rpc_host"],
    config["client"]["rpc_port"]
)

runtime = 0
timeout = 60
while True:
  try:
    response = client.request("get_info", [])
    blockchain_info = response.json()["result"]

    age = int(blockchain_info["blockchain_head_block_age"])
    height = int(blockchain_info["blockchain_head_block_num"])
    timestamp = blockchain_info["blockchain_head_block_timestamp"]
    health = blockchain_info["blockchain_average_delegate_participation"]
    confirm = blockchain_info["blockchain_confirmation_requirement"]
    wallet_open = blockchain_info["wallet_open"]
    if wallet_open == True:
      runtime += 10
    else:
      runtime = 0
    if age >= timeout and runtime > 120:
      print("blockchain sync timeout, block %d age is %d, restart client" %(height, age))
      runtime = 0
      os.system("killall -9 bitshares_client");
    else:
      print("[%s] block:%d,age:%d,health:%.2f%%,confirm:%s " %(timestamp,height, age,health, confirm))
    time.sleep(10)
  except Exception as e:
    runtime = 0
    print("unknown error, retry after 10 seconds")
    print(e)
    time.sleep(10)
