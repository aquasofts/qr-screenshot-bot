import cv2
import numpy as np
from PIL import ImageGrab, Image
from pyzbar.pyzbar import decode
import requests
import json
import time
import winreg

# ============== 配置区 ==============
WEBHOOK_URL = "https://open.feishu.cn/open-apis/bot/v2/hook/xxxxx"
CHECK_INTERVAL = 1  # 截图间隔（秒）
# ===================================

def send_feishu_message(content: str):
    """发送飞书文本消息"""
    payload = {
        "msg_type": "text",
        "content": {
            "text": f"🔔 检测到二维码!\n\n内容: {content}\n\n时间: {time.strftime('%Y-%m-%d %H:%M:%S')}"
        }
    }
    
    headers = {"Content-Type": "application/json"}
    
    try:
        response = requests.post(WEBHOOK_URL, headers=headers, json=payload, timeout=10)
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def capture_screen():
    """截取屏幕"""
    screen = ImageGrab.grab()
    screen_rgb = screen.convert('RGB')
    img = cv2.cvtColor(np.array(screen_rgb), cv2.COLOR_RGB2BGR)
    return img

def detect_qrcode(img):
    """检测二维码"""
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    barcodes = decode(gray)
    
    results = []
    for barcode in barcodes:
        data = barcode.data.decode('utf-8')
        rect = barcode.rect
        results.append({
            'data': data,
            'position': (rect.left, rect.top, rect.width, rect.height)
        })
    return results

def main():
    print("=" * 50)
    print("📷 屏幕二维码监控已启动")
    print(f"⏱️  检测间隔: {CHECK_INTERVAL} 秒")
    print("=" * 50)
    
    last_qrcodes = set()
    
    while True:
        try:
            img = capture_screen()
            qrcodes = detect_qrcode(img)
            
            current_qrcodes = {qr['data'] for qr in qrcodes}
            new_qrcodes = current_qrcodes - last_qrcodes
            
            if new_qrcodes:
                print(f"\n🚨 检测到 {len(new_qrcodes)} 个新二维码!")
                
                for content in new_qrcodes:
                    print(f"   内容: {content}")
                    
                    # 发送飞书通知
                    result = send_feishu_message(content)
                    
                    # 检查发送结果
                    if result.get('code') == 0:
                        print("   ✅ 飞书通知发送成功")
                    elif result.get('StatusCode') == 0:
                        print("   ✅ 飞书通知发送成功")
                    else:
                        print(f"   ❌ 发送失败: {result}")
                    
                    time.sleep(0.5)
                
                last_qrcodes.update(new_qrcodes)
            
            time.sleep(CHECK_INTERVAL)
            
        except KeyboardInterrupt:
            print("\n\n🛑 用户停止监控")
            break
        except Exception as e:
            print(f"❌ 错误: {e}")
            time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()