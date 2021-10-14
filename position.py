import numpy as np
import time
import socket
import queue

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
#辞書を用意 ビーコンid : [] 
beacons = dict()

#入場者用のキュー
q = queue.Queue(5)
q.put(1)
q.put(2)
q.put(3)
q.put(4)
q.put(5)

#ビーコン番号
beacon_num = dict()

while True: #データ受け取りまで
    #メッセージ受信
    message = sock.recv(M_SIZE)
    message = message.decode("utf-8")
    print(message)
    #スマホ, ビーコン, 距離, rssi

    #分割
    msg = message.split(':')
    #自分の送信データの場合無視

    if (msg[1] == "1026"):
        continue

    #エラー処理
    if (msg[0] != "1" and msg[0] != "2" and msg[0] != "3"):
        print("pass")
        continue

    #print("test")
    #キーがない場合辞書を作成
    if msg[1] not in beacons:
        beacons[msg[1]] = {"1" : 0, "2" : 0, "3": 0}

    #インデックス対応
    if msg[1] not in beacon_num:
        tmp = q.get()
        beacon_num[msg[1]] = tmp
        q.put(tmp)

    

    #ディクショナリが空だったら入れる
    if ((beacons[msg[1]]["1"] == 0) and (int(msg[0]) == 1)):
        beacons[msg[1]]["1"] = float(msg[2])
    elif ((beacons[msg[1]]["2"] == 0) and (int(msg[0]) == 2)):
        beacons[msg[1]]["2"] = float(msg[2])
    elif ((beacons[msg[1]]["3"] == 0) and (int(msg[0]) == 3)):
        beacons[msg[1]]["3"] = float(msg[2])
    print(beacons)
    #print(len(dist_list))

    #DB用のデータグラム all
    send_string = str(msg[0]) + ":" +  str(msg[1]) + ":" +  str(msg[3]) + ":" +  str(msg[2]) 
    print("DB Datagrum : " + send_string)
    client.sendto(send_string.encode('utf-8'),(SEND_HOST2,SEND_PORT1))
    #Unity用のデータグラム android, RSSI, Beacon
    send_string = str(msg[0]) + ":" +  str(msg[3]) + ":" + str(beacon_num[msg[1]]) + ":" + str(msg[1])
    #send_string = str(msg[0]) + ":" +  str(msg[3]) + ":" + str(msg[1])
    print("Unity Datagrum : " + send_string)
    client.sendto(send_string.encode('utf-8'),(SEND_HOST1,SEND_PORT1))

    #位置がそろったときになる処理
    if (beacons[msg[1]]["1"] != 0 and beacons[msg[1]]["2"] != 0 and beacons[msg[1]]["3"] != 0):
        print(beacons)
        dist_list = list(beacons[msg[1]].values())
        print(dist_list)    
        #初期位置を設定する
        initial_loc = midpoint(locations)   
        #最小二乗誤差を計算
        result = minimize(mse, initial_loc, (locations, dist_list))
        #print("the answer is:")
        print(result.x)
        send_string = "p" + ":" + msg[1] + ":" + str(result.x[0]) + ":" +  str(result.x[1])
        print(send_string)
        #DB position datagrum
        client.sendto(send_string.encode('utf-8'),(SEND_HOST2,SEND_PORT1))
        #位置情報クリア
        beacons[msg[1]] = {"1" : 0, "2" : 0, "3": 0}

    print("debug beacon : " + str(beacon_num))

    
