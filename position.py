import numpy as np
import time
import socket

def distance(posx, posy):
    #配列としてまとめて処理
    return np.sqrt(sum( (np.array(posx) - np.array(posy)) ** 2))
#配列でうけとってすべての距離を計算して可算する。

def mse(x, locations , distances):
    #temp
    sum_sqerr = 0.0
    for loc, dist in zip(locations, distances):
        #xは推定場所
        dist_calculated = distance(x, loc)
        #二乗誤差を求める
        sum_sqerr += (dist_calculated - dist) ** 2
        #locationの数割って〆る
    return sum_sqerr / len(locations)

#初期位置を平均から求める
def midpoint(*args):
    return np.mean(np.array(*args), axis=0)

from scipy.optimize import minimize
#start = time.time()

M_SIZE =1024
HOST = '10.200.162.83'
PORT = 10000

sock =socket.socket(socket.AF_INET,type=socket.SOCK_DGRAM)
sock.bind((HOST,PORT))

rec1 = [0,0] #セントラルの座標1
rec2 = [0.1, 1.9] #セントラルの座標2
#rec3 = [3.65, 2.1] #セントラルの座標2
d1 = 0
d2 = 0
#d3 = 0
locations = [rec1, rec2, rec3]

while True: #データ受け取りまで
    message, cli_addr = sock.recvfrom(M_SIZE)
    message = message.decode("utf-8")
    msg = message.split('?')
    if (int(msg[0]) == 0):
        d1 = int(msg[2])
    elif (int(msg[0]) == 1):
        d2 = int(msg[2])
    elif (int(msg[0]) == 2):
        d3 = int(msg[2])
    distances = [d1, d2, d3]
    #初期位置を設定する
    initial_loc = midpoint(locations)   
    #最小二乗誤差を計算
    result = minimize(mse, initial_loc, (locations, distances))
    print(result.x)
    print(message)

d1 = 1.084
d2 = 1.135
d3 = 3.055

locations = [rec1, rec2, rec3]
distances = [d1, d2, d3]
#初期位置を設定する
initial_loc = midpoint(locations)

result = minimize(mse, initial_loc, (locations, distances))
print(result.x)

#end = time.time() - start
#print(end)
