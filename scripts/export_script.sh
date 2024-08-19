#!/usr/bin/expect -f

# Set variables
set user "cloudera"
set host "192.168.245.129"
set password "cloudera"

# Connect to remote host using SFTP
spawn sftp $user@$host

# Expect password prompt and send password
expect "password:"
send "$password\r"
expect "sftp>"
send "cd Desktop/reddit_Data\r"
expect "sftp>"
send "put /home/ubuntu/Documents/reddit_data/*\r"
expect "sftp>"
send "exit\r"
