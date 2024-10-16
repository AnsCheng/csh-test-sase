import time
import os
import subprocess

def run_applescript(script):
    """Run an AppleScript script and return the result."""
    try:
        result = subprocess.check_output(['osascript', '-e', script], universal_newlines=True)
        return result.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running AppleScript: {e}")
        return "Unknown"


def install_wechat_from_app_store():
    """Install WeChat from the Mac App Store."""
    print("Starting WeChat installation from the App Store...")
    applescript = '''
    tell application "System Events"
        tell process "App Store"
            launch
            delay 10  -- 增加延迟时间
            tell window "App Store"
                -- 找到搜索框
                set searchField to UI element "UIA.AppStore.SearchField" of group 1 of group 1
                log "Search field found"
                set value of searchField to "WeChat"
                keystroke return
                delay 5
                
                -- 等待搜索结果加载
                log "Waiting for search results..."
                repeat while not (exists UI element "WeChat" of collection view 1 of scroll area 1)
                    delay 1
                end repeat
                log "Search results loaded"
                
                -- 找到搜索结果列表
                set resultList to collection view 1 of scroll area 1
                log "Result list found"
                
                -- 检查每个UI元素以找到下载按钮
                repeat with i from 1 to (count UI elements of resultList)
                    set thisElement to UI element i of resultList
                    log "Checking element: " & name of thisElement & ", Role: " & role description of thisElement
                    if (role description of thisElement as string) contains "button" and (name of thisElement as string) contains "Download" then
                        log "Found download button"
                        click thisElement
                        delay 5
                        if exists UI element "Install" of thisElement then
                            log "Found 'Install' button"
                            click UI element "Install" of thisElement
                            
                            -- 等待安装完成
                            set startTime to current date
                            log "Installation started."
                            repeat
                                delay 5
                                set buttonStatus to my get_install_button_status()
                                if buttonStatus is "" then
                                    log "WeChat installation completed."
                                    exit repeat
                                else
                                    set currentTime to current date
                                    set elapsedTime to (currentTime - startTime) / 60
                                    log "WeChat installation in progress... Button status: " & buttonStatus & " Elapsed time: " & elapsedTime & " minutes"
                                    if elapsedTime > 60 then
                                        log "Installation timed out after 60 minutes."
                                        exit repeat
                                    end if
                                end if
                            end repeat
                            exit repeat
                        end if
                    end if
                end repeat
            end tell
        end tell
    end tell
    '''

    try:
        run_applescript(applescript)
        print("WeChat installation initiated. Waiting for the installation to complete...")
    except RuntimeError as e:
        print(f"Error initiating WeChat installation: {e}")
        return

    # 等待安装完成
    app_path = "/Applications/WeChat.app"
    start_time = time.time()
    timeout = 60 * 60  # 1小时超时
    while not os.path.exists(app_path):
        elapsed_time = time.time() - start_time
        if elapsed_time > timeout:
            print("Installation timed out after 1 hour.")
            break
        time.sleep(5)
        button_status = get_install_button_status()
        print(f"WeChat installation in progress... Button status: {button_status} Elapsed time: {elapsed_time:.2f} seconds")

    if os.path.exists(app_path):
        print("WeChat installation completed successfully.")
        print(f"WeChat is installed at: {app_path}")
    else:
        print("WeChat installation failed.")

if __name__ == "__main__":
    install_wechat_from_app_store()