# Dingtalk_Robot
HomeAssistant 钉钉群机器人消息推送

修改自： \
https://bbs.hassbian.com/thread-3920-1-1.html \
文档：
https://open.dingtalk.com/document/group/custom-robot-access 


## 修改
1、支持加签功能 \
2、支持消息类型 type

## 安装

* 将 custom_component 文件夹中的内容拷贝至自己的相应目录

或者
* 将此 repo ([https://github.com/dscao/dingtalk_robot](https://github.com/dscao/dingtalk_robot)) 添加到 [HACS](https://hacs.xyz/)，然后添加“Dingtalk Robot”

## 配置
```yaml
notify:
  - platform: dingtalk_robot
    name: dingtalk          # 实体ID  比如这个出来就是notify.dingtalk
    resource: https://oapi.dingtalk.com/robot/send?access_token=xxxxxxxxxxxxxxxxxxxxxxxx  #机器人向钉钉群推送消息的Webhook地址
    secret: SECxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx  #加签密钥 ，未加签不填写此行。
```

## 使用
```yaml
service: notify.dingtalk  #调用服务
data:
  message: 消息内容
  target:
    - at的手机号1
    - at的手机号2
    - at的手机号3


service: notify.dingtalk
data:
  message: 发送纯文本消息，当前时间：{{now().strftime('%Y-%m-%d %H:%M:%S')}}


service: notify.dingtalk
data:
  message: 发送带标题和分隔线的纯文本消息,我就是我, @XXX 是不一样的烟火
  title: 这是标题


service: notify.dingtalk
data:
  message: 发送带标题和内容的链接卡片
  title: 这是标题
  data:
    type: link
    url: 'https://www.dingtalk.com/'
    picurl: 'https://gw.alicdn.com/imgextra/i2/O1CN01r4HyWa20OJS6nSgeK_!!6000000006839-2-tps-386-80.png'


service: notify.dingtalk
data:
  message: "#### 杭州天气 @150XXXXXXXX \n > 9度，西北风1级，空气良89，相对温度73%\n > ![screenshot](https://img.alicdn.com/tfs/TB1NwmBEL9TBuNjy1zbXXXpepXa-2400-1218.png)\n > ###### 10点20分发布 [天气](https://www.dingtalk.com) \n"
  title: 这是标题
  data:
    type: markdown


service: notify.dingtalk
data:
  message: "![screenshot](https://gw.alicdn.com/tfs/TB1ut3xxbsrBKNjSZFpXXcXhFXa-846-786.png) ### 乔布斯 20 年前想打造的苹果咖啡厅 Apple Store 的设计正从原来满满的科技感走向生活化，而其生活化的走向其实可以追溯到 20 年前苹果一个建立咖啡馆的计划"
  title: 这是标题,整体跳转ActionCard类型
  data:
    type: actionCard
    url: 'https://www.dingtalk.com/'

```

## 示例
```yaml   
service: notify.dingding
data:
  title: 小汽车当前位置：{{states('sensor.mycar_loc')}}[dshass]
  message: >-
    小汽车当前位置：{{states('sensor.mycar_loc')}} {{"\n\n"}}
    状态刷新时间：{{"\n\n"}}{{state_attr('device_tracker.gddr_gooddriver',
    'querytime')}} {{"\n\n"}}
    车辆状态：{{state_attr('device_tracker.gddr_gooddriver', 'status')}} {{"\n\n"}}
    到达位置时间：{{"\n\n"}}{{state_attr('device_tracker.gddr_gooddriver',
    'updatetime')}}
    {{"\n\n"}}停车时长：{{state_attr('device_tracker.gddr_gooddriver',
    'parking_time')}}{{"\n\n"}}当前速度：{{state_attr('device_tracker.gddr_gooddriver',
    'speed') |round(1)
    }}km/h{{"\n\n"}}[查看地图](https://uri.amap.com/marker?position={{state_attr('device_tracker.gddr_gooddriver',
    'longitude')+0.00555}},{{state_attr('device_tracker.gddr_gooddriver',
    'latitude')-0.00240}})![https://restapi.amap.com/v3/staticmap?zoom=14&size=1024*512&markers=large,,A:{{state_attr('device_tracker.gddr_gooddriver',
    'longitude')+0.00555}},{{state_attr('device_tracker.gddr_gooddriver',
    'latitude')-0.00240}}&key=819c47ccf5602b3a5e97161836e1176f](https://restapi.amap.com/v3/staticmap?zoom=14&size=1024*512&markers=large,,A:{{state_attr('device_tracker.gddr_gooddriver',
    'longitude')+0.00555}},{{state_attr('device_tracker.gddr_gooddriver',
    'latitude')-0.00240}}&key=81xxxxxxxxxxxxxxxxxxx)
  date: 
    type: markdown


```



