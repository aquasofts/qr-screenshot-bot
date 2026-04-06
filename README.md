# QR Screenshot Bot

屏幕上的二维码一出现，马上通知你。

## 这是什么？

这是一个轻量级的后台监控工具，能自动检测你屏幕上出现的任何二维码，并通过飞书机器人实时推送给你。不用手动截图、不用扫码，看到即收到。

适合那些经常需要处理临时二维码的场景：
- 会议签到码
- 挂机刷课时弹出的二维码

## 怎么用？

### 1. 安装依赖

**macOS:**
```bash
pip install opencv-python requests numpy
```

**Windows:**
```bash
pip install opencv-python requests numpy pillow pyzbar
```

### 2. 配置飞书机器人

1. 在飞书群聊中添加「自定义机器人」
2. 复制 webhook URL
3. 打开对应的主文件（`mac_main.py` 或 `windows_main.py`）
4. 替换 `WEBHOOK_URL` 配置为你自己的 webhook 地址


启动后会看到这样的提示：
```
==================================================
📷 屏幕二维码监控已启动
⏱️  检测间隔: 1 秒
==================================================
```

程序会在后台默默工作，一旦检测到新的二维码，就会立即推送通知。

## 相关细节

- **macOS版本**：使用系统自带的`screencapture`命令截图，配合OpenCV内置的QR检测器
- **Windows版本**：使用PIL的ImageGrab截屏，配合pyzbar进行二维码识别
- **去重机制**：自动过滤重复的二维码，只推送新出现的内容
- **刷新速度**：每秒截图一次

## 停止监控

按 `Ctrl + C` 即可优雅退出。

## 注意事项

- 首次在macOS上运行可能需要授予屏幕录制权限
- Windows用户可能需要安装Visual C++ Redistributable
- 飞书webhook地址包含敏感信息，请勿公开分享代码

---
