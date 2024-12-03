-- 激活钉钉应用
tell application "钉钉-csh"
	activate
end tell

delay 1 -- 等待1秒

-- 使用 System Events 定位聊天窗口
tell application "System Events"
	tell process "DingTalk"
		set frontmost to true
		set chatWindows to every window
		repeat with chatWindow in chatWindows
			log "Found window: " & (name of chatWindow as string)
			if (name of chatWindow as string) contains "程善红" then
				log "Matched window: " & (name of chatWindow as string)
				set position of chatWindow to {100, 100} -- 设置窗口位置
				set chatWindowPosition to position of chatWindow
				exit repeat
			end if
		end repeat
	end tell
end tell

delay 1 -- 等待1秒

-- 指定目录路径
set directoryPath to POSIX file "/Users/chengshanhong/Documents/ttest/"

-- 获取目录下的所有文件
tell application "Finder"
	set filesList to every file of folder directoryPath
	repeat with aFile in filesList
		set filePath to (aFile as alias)
		set fileName to name of (info for file filePath)
		
		-- 打开文件夹并选择文件
		activate
		reveal filePath
		select filePath
		delay 1 -- 等待1秒
		
		-- 复制文件
		tell application "System Events"
			keystroke "c" using {command down} -- 复制文件
			delay 1 -- 等待1秒
			
			-- 切换回钉钉
			tell application "钉钉-csh" to activate
			delay 1 -- 等待1秒
			
			-- 粘贴文件
			keystroke "v" using {command down} -- 粘贴文件
			delay 1 -- 等待1秒
		end tell
	end repeat
end tell

return "Send_all_files_in_the_current_directory"
