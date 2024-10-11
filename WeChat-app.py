import os
import subprocess
import time

def run_applescript(script):
    """Run an AppleScript command."""
    process = subprocess.Popen(['osascript', '-e', script], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        raise RuntimeError(f"AppleScript error: {stderr.decode().strip()}")
    return stdout.decode().strip()

def install_wechat_from_app_store():
    """Install WeChat from the Mac App Store."""
    print("正在从App Store安装微信...")
    applescript = '''
    tell application "System Events"
        tell process "App Store"
            launch
            delay 5
            tell window 1
                -- Find and click the search field
                set searchField to missing value
                repeat with elem in every UI element
                    if (role description of elem as string) contains "search field" then
                        set searchField to elem
                        exit repeat
                    end if
                end repeat
                if searchField is not missing value then
                    set value of searchField to "WeChat"
                    keystroke return
                    delay 5
                    
                    -- Wait for the search results to load
                    repeat while not (exists UI element "WeChat" of list 1 of scroll area 1)
                        delay 1
                    end repeat
                    
                    -- Click the "Get" button
                    tell list 1 of scroll area 1
                        repeat with i from 1 to (count UI elements)
                            set thisElement to UI element i
                            if name of thisElement is "Get" then
                                click thisElement
                                delay 5
                                if exists UI element "Install" then
                                    click UI element "Install"
                                    -- Wait for the installation to complete
                                    repeat
                                        delay 5
                                        if not (exists UI element "Install") then
                                            log "微信安装完成."
                                            exit repeat
                                        end if
                                    end repeat
                                    exit repeat
                                end if
                            end if
                        end repeat
                    end tell
                else
                    log "没有找到搜索字段"
                end if
            end tell
        end tell
    end tell
    '''
    run_applescript(applescript)
    print("微信安装已启动。等待安装完成...")

    # 等待微信安装完成
    app_path = "/Applications/WeChat.app"
    while not os.path.exists(app_path):
        time.sleep(5)
    print("微信安装成功")

def open_wechat():
    """打开微信应用程序."""
    app_path = "/Applications/WeChat.app"
    if os.path.exists(app_path):
        print("Opening WeChat...")
        subprocess.run(['open', app_path])
    else:
        print("微信未安装。请先安装。")

if __name__ == "__main__":
    action = input("输入 'install' 从 App Store 安装微信，或输入 'open' 以打开微信：")

    if action == "install":
        install_wechat_from_app_store()
    elif action == "open":
        open_wechat()
    else:
        print("无效操作。请输入 'install' 或 'open' ")
