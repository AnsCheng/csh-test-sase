import subprocess

def get_browser_process():
    try:
        # 获取应用的可执行文件名
        cmd = 'defaults read /Applications/360Chrome.app//Contents/Info CFBundleExecutable'
        executable = subprocess.check_output(cmd, shell=True).decode().strip()
        
        # 使用可执行文件名查询进程
        cmd = f'ps aux | grep "{executable}" | grep -v "grep"'
        output = subprocess.check_output(cmd, shell=True).decode()
        
        if output:
            # 提取 PID 和进程名
            parts = output.strip().split()
            pid = parts[1]
            process_name = parts[10] if len(parts) > 10 else "Unknown"
            return (pid, process_name, output)
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None


result = get_browser_process()
if result:
    pid, name, full_output = result
    print(f"找到进程 (PID: {pid}): {name}")
    print(f"完整信息:\n{full_output}")
else:
    print("未找到进程，请确保浏览器正在运行。")