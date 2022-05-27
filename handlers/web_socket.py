import tornado.websocket
import json
import threading
import serial
import asyncio

import dbUtil
import time
import handlers.fuzzy as fuzzy

serialPort = "com3"
baudRate = 9600

# 串口
# 波特率
ser = serial.Serial(serialPort, baudRate, timeout=0.5)
print("参数设置：串口=%s ，波特率=%d" % (serialPort, baudRate))

global db


class SocketHandler(tornado.websocket.WebSocketHandler):
    global db
    clients = set()

    def on_message(self, message):
        global db
        db = self.settings['db']
        #print(message)

        data = json.loads(message)
        typ = data['type']

        #print("get type is", typ)

        # 接收到车流量信息
        if typ == 'lane':
            #print("type is lane")
            # 发送给推理机处理
            reasonHandler(data)

        # 接收到信号灯状态信息，转发给下位机
        else:
            state = data['state']
            ser.write(str(state).encode())
            #print("信号灯状态：", str(state).encode())

    def open(self):

        SocketHandler.clients.add(self)

    def on_close(self):

        SocketHandler.clients.remove(self)

    def check_origin(self, origin):

        return True  # 允许WebSocket的跨域请求


default_handlers = [
    (r"/chat", SocketHandler),
]

'''
    根据前台地图车流量数据进行推理，得出四个状态信号灯的时长，最后返回给前台地图
'''


def confident_infer(rain, snow, wind, lightTime):
    print("chushi:", lightTime)
    rain = max(0, min(100, rain))
    snow = max(0, min(100, snow))
    wind = max(0, min(100, wind))
    cf_p = dict()
    cf_p['下雨'] = rain / 100
    cf_p['下雪'] = snow / 100
    cf_p['大风'] = wind / 100
    newdict = {}
    entitys = dbUtil.findKLList(db)
    for index, element in enumerate(entitys):
        premise = element.E
        conclusion = element.H
        val = cf_p[premise]
        if val >= element.CFE:
            newdict[conclusion] = val * element.CFHE
    print("所有相关结论：", newdict)
    maxkey = ""
    for key, value in newdict.items():
        if (value == max(newdict.values())):
            maxkey = key
    if (maxkey == "绿灯时间+3s"):
        print("最终结论为：", maxkey)
        for i in range(len(lightTime)):
            lightTime[i] += 3
    elif (maxkey == "绿灯时间+5s"):
        print("最终结论为：", maxkey)
        for i in range(len(lightTime)):
            lightTime[i] += 5
    elif (maxkey == "绿灯时间+6s"):
        print("最终结论为：", maxkey)
        for i in range(len(lightTime)):
            lightTime[i] += 6
    # print("zuihou", lightTime)
    return lightTime


def get_fuzzy_name_by_car_number(car_number):
    if car_number < 6:
        return "small"
    elif car_number < 12:
        return "mid"
    else:
        return "large"


def reasonHandler(data):
    global db
    cars = data['cars']
    topRight = cars["topRight"]
    eastLeft = cars["eastLeft"]
    eastRight = cars["eastRight"]
    topLeft = cars["topLeft"]

    res_car_numbers = [topRight, eastLeft, eastRight, topLeft]

    #print("topLeft:" + str(topLeft) + ";topRight:" + str(topRight) + ";eastLeft=" + str(eastLeft) + ";eastRight=" + str(
        #eastRight))

    # 存入数据库
    dbUtil.addCar(db, "topRight", topRight, time.strftime("%Y-%m-%d %H:%M:%S"))
    dbUtil.addCar(db, "eastLeft", eastLeft, time.strftime("%Y-%m-%d %H:%M:%S"))
    dbUtil.addCar(db, "eastRight", eastRight, time.strftime("%Y-%m-%d %H:%M:%S"))
    dbUtil.addCar(db, "topLeft", topLeft, time.strftime("%Y-%m-%d %H:%M:%S"))

    # 计90s为一次通行周期，根据权重分配通行时间.
    # 基础通行时间为5s，在5s基础上累加.
    total_time = 16
    basePassTime = 5

    res_base_pass_time = basePassTime
    res_public_time = total_time

    print("每个方向基础时间为", basePassTime, "，除此以外，根据权重分配", total_time)

    fuzzy_handler = fuzzy.get_default_fuzzy()
    topRightWeight = fuzzy_handler.get_result_by_input(get_fuzzy_name_by_car_number(topRight))
    eastLeftWeight = fuzzy_handler.get_result_by_input(get_fuzzy_name_by_car_number(eastLeft))
    eastRightWeight = fuzzy_handler.get_result_by_input(get_fuzzy_name_by_car_number(eastRight))
    topLeftWeight = fuzzy_handler.get_result_by_input(get_fuzzy_name_by_car_number(topLeft))

    print("获取到权重比例为：", topRightWeight, eastLeftWeight, eastRightWeight, topLeftWeight)

    total_weight = topLeftWeight + topRightWeight + eastLeftWeight + eastRightWeight

    pass_times = [
        basePassTime + (total_time * topRightWeight / total_weight),
        basePassTime + (total_time * eastLeftWeight / total_weight),
        basePassTime + (total_time * eastRightWeight / total_weight),
        basePassTime + (total_time * topLeftWeight / total_weight),
    ]

    res_public_allocated_times = [tim - basePassTime for tim in pass_times]

    print("各方向基础时间为：", pass_times)

    ####################推理机处理逻辑开始#################
    weather = dbUtil.getWeather(db)
    rain = weather.rain
    snow = weather.snow
    wind = weather.wind

    res_weather_rain = rain
    res_weather_snow = snow
    res_weather_wind = wind

    print("在基础时间上根据天气情况进行进一步加成")
    intersectionLightTimes = confident_infer(rain, snow, wind, pass_times)

    res_weather_add_times = [intersectionLightTimes[i] - res_public_allocated_times[i] - basePassTime for i in range(4)]
    res_final_results = [tim for tim in intersectionLightTimes]

    import datetime

    res_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    dbUtil.insertResult(
        db=db,
        name="",
        weather_rain=res_weather_rain,
        weather_snow=res_weather_snow,
        weather_wind=res_weather_wind,
        base_pass_time=res_base_pass_time,
        public_time=res_public_time,
        car_numbers=res_car_numbers,
        public_allocated_times=res_public_allocated_times,
        weather_add_times=res_weather_add_times,
        final_results=res_final_results,
        time=res_time,
    )

    ####################推理机处理逻辑结束#################

    # 推理机推理结果

    # intersectionLightTimes = [topRight, eastLeft, eastRight, topLeft]

    print(intersectionLightTimes)
    for client in SocketHandler.clients:
        client.write_message(json.dumps({
            'type': "lightTime",
            "data": intersectionLightTimes
        }))


def checkTask():
    last = ""
    while (1):
        data = ser.readline()
        s3 = data.decode().rstrip()
        if s3 == 'yes':
            for client in SocketHandler.clients:
                client.write_message(json.dumps({
                    'type': "addCar",
                    "data": True
                }))
        last = s3


def loopCheckTask():
    # loop = asyncio.get_event_loop()  用这种会出现下面报错  使用apscheduler + asyncio 建议使用以下方式
    # 处理报错  RuntimeError: There is no current event loop in thread 'ThreadPoolExecutor-0_0'.
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    bj = loop.create_task(checkTask())
    loop.run_until_complete(asyncio.wait([bj]))


try:
    thread = threading.Thread(target=loopCheckTask)
    thread.start()

except:
    print("Error: unable to start thread")
