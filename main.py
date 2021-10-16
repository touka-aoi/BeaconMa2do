import numpy as np
import time
import socket
import queue
import socket
import csv
import sqlite3
import time
import datetime
import threading

def retrive(msg):
    #DB名
    dbname = "tonokaiyutest.db"

    #時間を作成
    unix = time.time()
    dt = datetime.datetime.fromtimestamp(unix)
    message = msg.split(":") #送られてきたstrを:で分割

    #時間を追加
    message.append(dt)

    #DB接続
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()
    #先頭確認
    x = message[0]
    try:
        if not x == "p":
            cur.execute("CREATE TABLE IF NOT EXISTS kaiyu (sentral text,beacon text, rssi text, distance text, ymdt text)")
            cur.execute("INSERT INTO kaiyu VALUES (?,?,?,?,?)",(message))
        else: 
            cur.execute("CREATE TABLE IF NOT EXISTS coord (preparat text,beacon text, xcoord text, ycoord text, ymdt text)")
            cur.execute("INSERT INTO coord VALUES (?,?,?,?,?)",(message))
    except:
        return

    #DB反映
    conn.commit()
    conn.close()


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


def get_key_from_value(dict, needs):
    key = [k for k, v in dict.items() if v == needs]
    return str(key[0])


from scipy.optimize import minimize
counting = 0

M_SIZE = 8124 #データグラムサイズ
HOST = '192.168.128.100' #受信IP
PORT = 9000 #受信ポート番号

urssi = 0 #単位RSSI

SEND_HOST1 = '192.168.128.102' #送信IP 玉緒
SEND_PORT1 = 9000 #送信ポート
SEND_HOST2 = '192.168.128.100' #送信IP foxDot
SEND_PORT2 = 10000 #送信ポート

send_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock =socket.socket(socket.AF_INET,type=socket.SOCK_DGRAM)
sock.bind((HOST,PORT))


rec1 = [0, 0] #セントラルの座標1
rec2 = [0, 2] #セントラルの座標2
rec3 = [3, 0] #セントラルの座標2
d1 = 0
d2 = 0
d3 = 0
locations = [rec3, rec2, rec1]
#辞書を用意 ビーコンid : [] 
beacons = dict()

#入場者用のキュー
# q = queue.Queue(5)
# q.put(1)
# q.put(2)
# q.put(3)
# q.put(4)
# q.put(5)

#ビーコン番号
beacon_num = dict()

#5回無視用カウント
cnt = 0

#確認用tuple
lis = list()


while True: #データ受け取りまで
    #メッセージ受信
    message = sock.recv(M_SIZE)
    message = message.decode("utf-8")
    #print(message)
    #スマホ, ビーコン, 距離, rssi

    #分割
    msg = message.split(':')
    #自分の送信データの場合無視
    if (msg[0] == "s"):
        continue

    counting += 1

    #フジセンのやつをスルーする

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
        for i in list(range(1,6)):
            if i in beacon_num.values():
                continue
            else:
                beacon_num[msg[1]] = i

    if (counting > 25):
        lis.append(msg[1])
        lis = set(lis)
        lis = list(lis)
        print(f"lis is : {lis}")
        if (counting > 50):
            st = set(beacon_num.keys()) - set(lis)
            st = list(st)
            print(f"is empyt : {st}")
            if len(st) != 0:
                for i in st:
                    del beacon_num[i]
            counting = 0
            lis = list()




    #ディクショナリが空だったら入れる
    if ((beacons[msg[1]]["1"] == 0) and (int(msg[0]) == 1)):
        beacons[msg[1]]["1"] = float(msg[2])
    elif ((beacons[msg[1]]["2"] == 0) and (int(msg[0]) == 2)):
        beacons[msg[1]]["2"] = float(msg[2])
    elif ((beacons[msg[1]]["3"] == 0) and (int(msg[0]) == 3)):
        beacons[msg[1]]["3"] = float(msg[2])
    #print(beacons)
    #print(len(dist_list))

    #DB用のデータグラム all
    send_string = str(msg[0]) + ":" +  str(msg[1]) + ":" +  str(msg[3]) + ":" +  str(msg[2]) 
    #保存 DB用のやつ    print("DB Datagrum : " + send_string)
    retrive(send_string)

    #foxDot用のデータグラム all
    send_string = "s" + ":" + str(msg[0]) + ":" +  str(msg[1]) 

    client.sendto(send_string.encode('utf-8'),(SEND_HOST2,9000))
    #Unity用のデータグラム android, RSSI, Beacon
    send_string = str(msg[0]) + ":" +  str(msg[3]) + ":" + str(beacon_num[msg[1]]) + ":" + str(msg[1])
    #send_string = str(msg[0]) + ":" +  str(msg[3]) + ":" + str(msg[1])

#保存 Unity用のやつ      print("Unity Datagrum : " + send_string) 

    client.sendto(send_string.encode('utf-8'),(SEND_HOST1,SEND_PORT1))

    #位置がそろったときになる処理
    if (beacons[msg[1]]["1"] != 0 and beacons[msg[1]]["2"] != 0 and beacons[msg[1]]["3"] != 0):
        #print(beacons)
        dist_list = list(beacons[msg[1]].values())
#保存        print(dist_list)    
        #初期位置を設定する
        initial_loc = midpoint(locations)   
        #最小二乗誤差を計算
        result = minimize(mse, initial_loc, (locations, dist_list))
        #print("the answer is:")
#保存 位置デバッグ       print(result.x)
        send_string = "p" + ":" + msg[1] + ":" + str(result.x[0]) + ":" +  str(result.x[1])

        
        print(send_string)
        
        #DB position datagrum
        #client.sendto(send_string.encode('utf-8'),(SEND_HOST2,SEND_PORT1))
        retrive(send_string)
        #位置情報クリア
        beacons[msg[1]] = {"1" : 0, "2" : 0, "3": 0}

        print("debug beacon : " + str(beacon_num)) #保存 ビーコンナンバー



