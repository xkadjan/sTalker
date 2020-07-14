# -*- coding: utf-8 -*-
"""
Created on Thu Jul  9 14:11:03 2020

@author: xkadj
"""
import subprocess
import os
with open(os.devnull, "wb") as limbo:
    for n in range(0, 255):
        ip="192.168.2.{0}".format(n)
        result=subprocess.Popen(["ping", "-c", "1", "-n", "-W", "2", ip],
            stdout=limbo, stderr=limbo).wait()
        if result:
#            print (ip,"inactive")
            continue
        else:
            print(ip, "active")