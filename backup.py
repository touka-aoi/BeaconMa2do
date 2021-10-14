import numpy as np
import time
import socket

#複数値のときデフォルト値は最後に書く
def rssi2dist(rssi, urssi, N=20):
    """
    引数
    ----------
    rssi : float
        取得RSSI
    urssi : float 
        単位RSSI
    N : integer
        特性値
    """
    #RSSIからDistにする式
    dist = 10 ** (- ( (rssi - urssi)) / N)
    #距離を返す
    return dist


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

M_SIZE = 8124 #データグラムサイズ
HOST = '192.168.128.101' #受信IP
PORT = 9000 #受信ポート番号

urssi = 0 #単位RSSI

SEND_HOST1 = '192.168.128.106' #送信IP 玉緒
SEND_PORT1 = 9000 #送信ポート
SEND_HOST2 = '192.168.128.107' #送信IP 西村
SEND_PORT2 = 10000 #送信ポート

send_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock =socket.socket(socket.AF_INET,type=socket.SOCK_DGRAM)
sock.bind((HOST,PORT))

rec1 = [0, 3] #セントラルの座標1
rec2 = [2, 0] #セントラルの座標2
rec3 = [0, 0] #セントラルの座標2
d1 = 0
d2 = 0
d3 = 0
locations = [rec3, rec2, rec1]
#辞書をようい

while True: #データ受け取りまで
    #print("test")
    dist_dict = {"1" : 0, "2" : 0, "3": 0}
    dist_list = []
    while True:
        message = sock.recv(M_SIZE)
        message = message.decode("utf-8")
        print(message)
        #スマホ, ビーコン, 距離, rssi
        msg = message.split(':')
        #自分の送信データの場合無視
        if (msg[0] == "p"):
            continue
        #ディクショナリが空かつ1番だったら入れるよ
        if ((dist_dict["1"] == 0) and (int(msg[0]) == 1)):
            dist_list.append(float(msg[2]))
            dist_dict["1"] = 1
        elif ((dist_dict["2"] == 0) and (int(msg[0]) == 2)):
            dist_list.append(float(msg[2]))
            dist_dict["2"] = 1
        elif ((dist_dict["3"] == 0) and (int(msg[0]) == 3)):
            dist_list.append(float(msg[2]))
            dist_dict["3"] = 1
        #print("length is")
        #print(len(dist_list))
        if (len(dist_list) == 3):
            break
        #print(f"dist list is {dist_list}")
        #西村 9000
        send_string = send_string = str(msg[0]) + ":" +  str(msg[1]) + ":" +  str(msg[3]) + ":" +  str(msg[2]) 
        print("this is nishi" + send_string)
        client.sendto(send_string.encode('utf-8'),(SEND_HOST2,SEND_PORT1))
        #TamaWWWo 9000
        send_string = str(msg[0]) + ":" +  str(msg[3] + ":" + str(msg[1]))
        print("this is tamao" + send_string)
        #デバグ用 単体送信
        client.sendto(send_string.encode('utf-8'),(SEND_HOST1,SEND_PORT1))


    #初期位置を設定する
    initial_loc = midpoint(locations)   
    #最小二乗誤差を計算
    result = minimize(mse, initial_loc, (locations, dist_list))
    #print("the answer is:")
    print(result.x)
    send_string = "p" + ":" + str(result.x[0]) + ":" +  str(result.x[1])
    print(send_string)

    #Tamawo 10000
    #西村 10000
    client.sendto(send_string.encode('utf-8'),(SEND_HOST1,SEND_PORT2))
    

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