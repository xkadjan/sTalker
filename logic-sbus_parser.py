# -*- coding: utf-8 -*-
"""
Created on Sat Jul  4 22:38:33 2020
This script solve byte parsing of SBUS record by Saleae logic analyzer
Logic Async Serial analyzer was set on: inverted logic, baud rate of 100000, 8 data bits, even parity bit, and 2 stop bits
inspirated by: https://github.com/1arthur1/PiSBUS
@author: xkadj
"""

import csv
import pandas as pd
import matplotlib.pylab as plt

file = r"sbus_t14s5_five_axis.log"
#file = r"C:\Users\xkadj\OneDrive\PROJEKTY\Projekt_ROBOTIKA\drone\logic\jetson.txt"
def split_messages_by_prefix(raw):
    messages_list,message = [],[]
    for byte in raw.value:
        if byte == 15:
            messages_list.append(message)
            message = []
        message.append(byte)
    lenghts = []
    for message in messages_list:
        lenghts.append(len(message))
    return messages_list[1:],lenghts

def split_messages_by_time_diff(raw):
    messages_list,times,message = [],[],[]
    for i,row in raw.iterrows():
        if row.time_diff > 0.001:
            times.append(row['Time [s]'])
            messages_list.append(message)
            message = []
        message.append(row.value)
    lenghts = []
    for message in messages_list:
        lenghts.append(len(message))
    return messages_list,lenghts,times

def get_axes(time_diff_messages_df_dropna):
    axes = []
    for i,message in time_diff_messages_df_dropna.iterrows():
        axes.append(list(unpack(bytes(message.astype(int).tolist()[1:23]), 11)))
    axes = pd.DataFrame(axes)
    axes['time'] = time_diff_messages_df_dropna.reset_index().time
    return axes

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
time_diff_messages_list,time_diff_lenghts,times = split_messages_by_time_diff(raw)

prefix_messages_df = pd.DataFrame(prefix_messages_list)
time_diff_messages_df = pd.DataFrame(time_diff_messages_list)
time_diff_messages_df['time'] = pd.Series(times)

time_diff_messages_df_dropna = time_diff_messages_df.dropna()

axes = get_axes(time_diff_messages_df_dropna)




# =============================================================================
plt.figure(figsize=[20, 4], dpi=100, facecolor='w', edgecolor='r').set_facecolor('whitesmoke')
plt.plot(axes.time,axes[4],'.',label='4')
plt.plot(axes.time,axes[5],'.',label='5')
plt.plot(axes.time,axes[6],'.',label='6')
plt.plot(axes.time,axes[7],'.',label='7')
plt.plot(axes.time,axes[3],'.',label='3')
plt.legend(["axe 4","axe 5", "axe 6", "axe 7", "mode axe"], loc ="lower right")
plt.title('SBUS: axe values', size=12, loc='left')
plt.xlabel('time[s]',size=10)
plt.ylabel('axe value [-]',size=10)

plt.minorticks_on()
plt.tick_params(axis='both',which='major',length=10,width=1,labelsize=6)
plt.style.use('seaborn-paper')
plt.grid(True)
plt.tight_layout()


#plt.plot(raw['Time [s]'],raw['value'],'.')
#plt.plot(raw['Time [s]'],raw['time_diff'],'.')