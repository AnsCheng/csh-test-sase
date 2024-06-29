#!/bin/sh

#  uninstall.sh
#  stunnel-mac
#
#  Copyright © 2023 alibaba cloud. All rights reserved.
echo $SUDO_USER
chflags -R noschg /Applications/SASE.app

rm -rf /Applications/SASE.app
killall -9 SASE
killall -9 SaseDLPManager
sleep 1
killall -9 com.aliyun.security.sase.helper
killall -9 laserver

#remove daemon
sudo -u $SUDO_USER launchctl unload /Library/LaunchDaemons/com.aliyun.security.sase.Daemon.plist
launchctl unload /Library/LaunchDaemons/com.aliyun.security.sase.Daemon.plist
rm /Library/LaunchAgents/com.aliyun.security.sase.Daemon.plist

#remove helper
launchctl unload /Library/LaunchDaemons/com.aliyun.security.sase.Helper.plist
rm /Library/LaunchDaemons/com.aliyun.security.sase.Helper.plist
rm /Library/PrivilegedHelperTools/com.aliyun.security.sase.Helper

#remove saseAppManager
sudo -u $SUDO_USER launchctl remove com.aliyun.security.sase.SaseAppManager
rm /Library/LaunchAgents/com.aliyun.security.sase.SaseAppManager.plist
killall -9 SaseAppManager

#remove saseUpdate
launchctl remove com.aliyun.security.sase.SaseUpdate
rm /Library/LaunchDaemons/com.aliyun.security.sase.SaseUpdate.plist

#remove main
sudo launchctl remove com.aliyun.security.sase.main

ps -ef|grep "com.aliyun.security.sase.main.watermark" |grep -v "grep"|awk '{print $2}'|xargs kill -9
ps -ef|grep "com.aliyun.security.sase.Helper" |grep -v "grep"|awk '{print $2}'|xargs kill -9
ps -ef|grep "com.aliyun.security.sase.Crashpad_handler" |grep -v "grep"|awk '{print $2}'|xargs kill -9
ps -ef|grep "com.aliyun.security.sase.Filescan" |grep -v "grep"|awk '{print $2}'|xargs kill -9

sleep 1
killall -9 SaseSoftwareMgr
rm -r /Library/Application\ Support/AliyunCsas/data
rm /Library/Application\ Support/AliyunCsas/*.plist
rm -r /Users/"$SUDO_USER"/Library/Application\ Support/alisase
rm -r /Library/Application\ Support/AliyunSase
