## 虎牙弹幕小助手python版

### 功能

1. 首次自动扫码登陆,后续自动使用token登陆(Mac window测试通过,linux未完成)
2. 自动监听主播上下线
3. 监听礼物,贵族弹幕,自动回复

### Todo

1. token登陆易过期,寻找一次登陆到期自动刷新的机制
2. 主播上下线通过轮询,待优化
3. 监听礼物消息未破解完,现在只能破解全系统礼物

### 运行

1. git clone https://github.com/br3ant/huya_barrage
2. cd huya_barrage
3. pip3 install -r requirements.txt
4. python3 main.py

### 注意事项

chromedriver驱动程序版本和电脑的chrome版本一定要一致
chromedriver下载地址 http://npm.taobao.org/mirrors/chromedriver
chrome版本:右上角三个点->帮助->关于


## 免责声明：仅学习使用，如有侵权，请联系本人删除（1106617567@qq.com）
