# -*- coding: utf-8 -*-
"""
Created on Sat Jul  4 22:38:33 2020
This script solve byte parsing of SBUS record by Saleae logic analyzer
Logic Async Serial analyzer was set on: inverted logic, baud rate of 100000, 8 data bits, even parity bit, and 2 stop bits
@author: xkadj
"""

import pandas as pd
import matplotlib.pylab as plt

file = r"sbus_t14s5_five_axis.log"

def split_messages_by_prefix(raw):
    messages_list,message = [],[]
    for byte in raw.value:
        if byte == 240:
            messages_list.append(message)
            message = []
        message.append(byte)
    lenghts = []
    for message in messages_list:
        lenghts.append(len(message))
    return messages_list[1:],lenghts

def split_messages_by_time_diff(raw):
    messages_list,message = [],[]
    for i,row in raw.iterrows():
        if row.time_diff > 0.001:
            messages_list.append(message)
            message = []
        message.append(row.value)
    lenghts = []
    for message in messages_list:
        lenghts.append(len(message))
    return messages_list,lenghts

def get_axes(time_diff_messages_df_dropna):
    axes = []
    for i,message in time_diff_messages_df_dropna.iterrows():
        axes.append(list(unpack(bytes(message.astype(int).tolist()[1:23]), 11)))
    return pd.DataFrame(axes)

def unpack(data, bitlen):
    mask = (1 << bitlen) - 1
    for chunk in zip(*[iter(data)] * bitlen):
        n = int.from_bytes(chunk, 'little')
        a = []
        for i in range(8):
            a.append(n & mask)
            n >>= bitlen
        yield from reversed(a)

# =============================================================================

raw = pd.read_csv(file, engine='python', quoting=csv.QUOTE_NONE)
raw['value'] = raw['Value'].str[-5:-1].apply(int, base=16)
raw['time_diff'] = raw['Time [s]'].diff()

prefix_messages_list,prefix_lenghts = split_messages_by_prefix(raw)
time_diff_messages_list,time_diff_lenghts = split_messages_by_time_diff(raw)

prefix_messages_df = pd.DataFrame(prefix_messages_list)
time_diff_messages_df = pd.DataFrame(time_diff_messages_list)

time_diff_messages_df_dropna = time_diff_messages_df.dropna()

axes = get_axes(time_diff_messages_df_dropna)




# =============================================================================

plt.plot(axes[3],'.',label='3')
plt.plot(axes[4],'.',label='4')
plt.plot(axes[5],'.',label='5')
plt.plot(axes[6],'.',label='6')
plt.plot(axes[7],'.',label='7')

plt.legend(["axe 3", "axe 4","axe 5", "axe 6", "axe 7"], loc ="lower right")



#plt.plot(raw['Time [s]'],raw['value'],'.')
#plt.plot(raw['Time [s]'],raw['time_diff'],'.')