
    //地图接口
    var mapSettings = {
        /**
            设置地图前端信号灯绿灯时长
            @param{lightTime} 长度为4，元素类型为数字型的数组。
            lightTime=[8,9,8,10]分别为南北右转，东西左转，东西右转，南北左转时长
         **/
        setMapLightTime:function (lightTime){
            window.setLightTime(lightTime);
        },

        /**
            在地图中增加一辆车。
        **/
        addCar:function(){
            window.addacar();
        }
    }

    //serial接口
    var serialSettings = {
        /**
            向上位机websocket发送信号灯信息
            lightTime
        **/
        sendSerialLightTime:function (stateIndex){
            var lightInfo = {
              "type": 'singalLight',
              "state": stateIndex
            }
            console.log(">>>>> send singalLight: ", stateIndex)
            console.log("send msg by ws singalLight")
            window.ws.send(JSON.stringify(lightInfo))
        },
         /**
            向上位机websocket发送信号灯信息
            lightTime
        **/
        sendLaneInfo:function (cars){
           var lightInfo = {
            "type": 'lane',
            "cars": cars
            }
            console.log("send msg by ws lane")
            window.ws.send(JSON.stringify(lightInfo))
        }
    }

    var  trafficSettings = {

        webSocket:{

            url:"ws://127.0.0.1:8000/chat",
            //接收上位机webSocket client.write_message发送的数据，并对前端做相应处理，如设置信号灯绿灯时长。

            onmessage:function(data){
                console.log(data);
                var type = data['type'];
                var res = data['data'];
                if (type === 'addCar' && res === true) {
                    mapSettings.addCar();
                }

                if (type === 'lightTime') {
                    mapSettings.setMapLightTime(res);
                }
            }
        },
    };





