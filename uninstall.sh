function sase() {
  if [[ "$1" == 'remove' ]]; then
    sudo launchctl remove com.aliyun.security.sase.daemon
    sudo launchctl remove com.aliyun.security.sase.main
    sudo ps -ef | grep sase | grep -v grep | awk '{ print $2 }' | xargs sudo kill -9
  elif [[ "$1" == 'uninstall' ]]; then
    sudo launchctl remove com.aliyun.security.sase.daemon
    sudo launchctl remove com.aliyun.security.sase.main
    sudo ps -ef | grep sase | grep -v grep | awk '{ print $2 }' | xargs sudo kill -9 
    sudo rm /Library/LaunchDaemons/com.aliyun.security.sase.*
    sudo rm -rf "/Applications/SASE.app"
    sudo rm -rf "/opt/AliyunSase"
    sudo rm -rf "/Library/Application Support/AliyunSase"
  elif [[ "$1" == 'reload' ]]; then
    sudo launchctl load -w /Library/LaunchDaemons/com.aliyun.security.sase.main.plist
  elif [[ "$1" == 'reboot' ]]; then
    sudo ps -ef | grep sase | grep -v grep | awk '{ print $2 }' | xargs sudo kill -9
  else
    echo "unspported"
  fi
}