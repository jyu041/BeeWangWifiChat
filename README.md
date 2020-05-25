# BeeWangWifiChat
# Goal:
To create one of the most energy efficient local network chatting program in python a 16 year old can create. 
That consits atleast one server, and two or more clients.

# Dumb stuff:
Have you ever had a friend, who's class is at the opposide side of your school? 
Have you ever wanted to chat in class but you cannot talk?
As long as you all are on the same wifi, you can use this program to talk to each other!
There are no subscription fees! There are no one collecting logs, or spying your conversations!
This is a simple, efficient chatting program (well still in development)!

# Dependencies:
- tkinter (for the GUI)
- threading (for being able to recieve messages and send messages)
- socket (the base of the program, to create TCP connections)
 - sys (mainly for force quitting the program)
 - plyer (to give a notification)
 - time (mainly using the .sleep() method)

# Info:
- There is a variable called "con_limit" in "server.py", this is a limit of how much clients can be connected at once
- Server still use quite a lot of resource power, I am too bad to fix this, I need people who are better xD

# Apologies!
I have not studied python very deeply or networking very deeply, there could be way more potential to this program, but I just have not
got the skills to discover them. 

# ChangeLog:
**Version 4:**
 * 26th May 2020 (Morning)
 - Super improvement on the UI
 - More improvement on data control stuff

**Version 3:**
 * 25th May 2020 (Afternoon)
 - Added ability to stop spam, clients can not repeat same message twice in a row
 - Users can not spam the enter key to spam empty strings
 - Added desktop notification (only active when window does not have focus)
 - Added glowing icon notification (only active when window does not have focus)

**Version 2:** 
 * 25th May 2020 (Before the morning, around 3am)
 - Added more messages to inform users about situations
 - Python does not crash and quit anymore when ever a client or server disconnects
 - Server should now allow clients to "rejoin" if their spot were not taken

**Version 1:** 
 * 24th May 2020 (Night)
 - The base of the program, allows a server and multiple clients have a "group chat" environment with GUI.
