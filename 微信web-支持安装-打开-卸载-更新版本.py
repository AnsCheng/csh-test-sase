import os
import requests
import subprocess
import shutil
from packaging import version
from bs4 import BeautifulSoup

# 微信官网下载链接
WECHAT_DOWNLOAD_URL = "https://dldir1.qq.com/weixin/mac/WeChatMac.dmg"

# 下载文件的保存路径
DOWNLOAD_PATH = "/tmp/WeChatMac.dmg"

# 应用安装路径
APP_PATH = "/Applications/WeChat.app"

# 实际挂载点路径
MOUNT_POINT = "/Volumes/微信 WeChat"

def download_wechat():
    print("正在下载微信安装包...")
    response = requests.get(WECHAT_DOWNLOAD_URL, stream=True)
    if response.status_code == 200:
        with open(DOWNLOAD_PATH, 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)
        print("下载完成")
    else:
        print(f"下载失败，状态码: {response.status_code}")
        return False
    return True

def check_download():
    if os.path.exists(DOWNLOAD_PATH):
        print("DMG文件已下载")
        return True
    else:
        print("DMG文件未下载，请检查下载过程")
        return False

def mount_dmg():
    print("正在挂载DMG文件...")
    result = subprocess.run(['hdiutil', 'attach', DOWNLOAD_PATH], capture_output=True, text=True)
    if result.returncode == 0:
        print("挂载成功")
        print(result.stdout)
        return True
    else:
        print(f"挂载失败: {result.stderr}")
        return False

def unmount_dmg():
    print("正在卸载DMG文件...")
    result = subprocess.run(['hdiutil', 'detach', MOUNT_POINT], capture_output=True, text=True)
    if result.returncode == 0:
        print("卸载成功")
        return True
    else:
        print(f"卸载失败: {result.stderr}")
        return False

def get_installed_version():
    if os.path.exists(APP_PATH):
        info_plist_path = os.path.join(APP_PATH, "Contents", "Info.plist")
        if os.path.exists(info_plist_path):
            result = subprocess.run(['defaults', 'read', info_plist_path, 'CFBundleShortVersionString'], capture_output=True, text=True)
            if result.returncode == 0:
                return result.stdout.strip()
    return None

def get_latest_version():
    try:
        response = requests.get("https://mac.weixin.qq.com/?t=mac&lang=zh_CN", timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # 查找包含版本号的 <p> 标签
            version_tag = soup.find('div', class_='download-area').find_all('p')[1]
            if version_tag:
                return version_tag.text.strip()
            else:
                print("未能找到版本号标签")
        else:
            print(f"请求失败，状态码: {response.status_code}")
    except Exception as e:
        print(f"获取最新版本失败: {e}")
    return None

def is_latest_version(installed_version, latest_version):
    if installed_version and latest_version:
        return version.parse(installed_version) >= version.parse(latest_version)
    return False

def install_wechat():
    print("正在安装微信...")
    if os.path.exists(APP_PATH):
        print("微信已安装，跳过安装")
        return True
    
    wechat_app_path = f"{MOUNT_POINT}/WeChat.app"
    if not os.path.exists(wechat_app_path):
        print(f"WeChat.app 未找到: {wechat_app_path}")
        return False
    
    result = subprocess.run(['cp', '-R', wechat_app_path, '/Applications/'], capture_output=True, text=True)
    if result.returncode == 0:
        print("安装成功")
        return True
    else:
        print(f"安装失败: {result.stderr}")
        return False

def uninstall_wechat():
    print("正在卸载微信...")
    if not os.path.exists(APP_PATH):
        print("微信未安装，跳过卸载")
        return True
    
    try:
        shutil.rmtree(APP_PATH)
        print("卸载成功")
        return True
    except Exception as e:
        print(f"卸载失败: {e}")
        return False

def open_wechat():
    print("正在打开微信...")
    if not os.path.exists(APP_PATH):
        print("微信未安装，无法打开")
        return False
    
    result = subprocess.run(['open', APP_PATH], capture_output=True, text=True)
    if result.returncode == 0:
        print("打开成功")
        return True
    else:
        print(f"打开失败: {result.stderr}")
        return False

def upgrade_wechat():
    print("正在检查微信版本...")
    installed_version = get_installed_version()
    latest_version = get_latest_version()

    if installed_version and latest_version:
        print(f"当前安装版本: {installed_version}")
        print(f"最新版本: {latest_version}")

        if is_latest_version(installed_version, latest_version):
            print("微信已是最新版本，无需更新")
            return True
        else:
            print("微信不是最新版本，开始更新...")
            if os.path.exists(APP_PATH):
                if not uninstall_wechat():
                    print("卸载旧版本失败")
                    return False
            if download_wechat() and mount_dmg() and install_wechat() and unmount_dmg():
                print("微信更新完成")
                return True
            else:
                print("微信更新失败")
                return False
    else:
        print("无法获取版本信息")
        return False

if __name__ == "__main__":
    action = input("请输入 'install' 安装微信, 'uninstall' 卸载微信, 'open' 打开微信, 或 'upgrade' 更新微信: ")

    if action == "install":
        if check_download():
            if not os.path.exists(APP_PATH):
                if mount_dmg() and install_wechat() and unmount_dmg():
                    print("微信安装完成")
                else:
                    print("微信安装失败")
            else:
                print("微信已安装，跳过安装")
        else:
            if download_wechat() and mount_dmg() and install_wechat() and unmount_dmg():
                print("微信安装完成")
            else:
                print("微信安装失败")
    elif action == "uninstall":
        if uninstall_wechat():
            print("微信卸载完成")
        else:
            print("微信卸载失败")
    elif action == "open":
        if open_wechat():
            print("微信打开完成")
        else:
            print("微信打开失败")
    elif action == "upgrade":
        if upgrade_wechat():
            print("微信更新完成")
        else:
            print("微信更新失败")
    else:
        print("无效的操作")
