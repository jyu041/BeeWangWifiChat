# server.py
# BeeWang
# A TCP chatting program

import sys, time
try:
    import tkinter as tk 
    from threading import Thread
    import socket
    from plyer import notification
except Exception as e:
    print(e)
    time.sleep(10)
    sys.exit()

all_connections = []
con_limit = 5
user_dict = {}

focussing = True

def getip():
    supnig = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        supnig.connect(('10.255.255.255', 1))
        IP = supnig.getsockname()[0]
    except Exception as e:
        print(e)
        IP = '127.0.0.1'
    finally:
        supnig.close()
    return IP

def send_msg(*args):
    write_data = str(text_enter.get())
    if len(write_data) == 0:
        return

    for connection in all_connections:
        connection.send((f'Server: {write_data}').encode())

    textbox.config(state=tk.NORMAL)
    textbox.insert('end', f'You : {write_data}\n')
    text_enter.delete(0, 'end')
    textbox.config(state=tk.DISABLED)
    textbox.see('end')

def send_from_other(other_data, conn_obj1, write):
    for connection in all_connections:
        if connection == conn_obj1:
            continue
        connection.send(other_data.encode())

    if write:
        textbox.config(state=tk.NORMAL)
        textbox.insert('end', f'{other_data}\n')
        textbox.config(state=tk.DISABLED)
        textbox.see('end')

def recv_msg(connection_obj):
    try:
        while True:
            got_data = connection_obj.recv(1024).decode()
            root.focus_set()
            '''
            if len(user_dict[str(connection_obj)]) == 2:
                user_dict.update({str(connection_obj.getpeername()):got_data.split(':')[0]})
                print(user_dict)
                print(user_dictp[connection_obj])
            '''
            textbox.config(state=tk.NORMAL)
            textbox.insert('end', f'{got_data}\n')
            send_from_other(got_data, connection_obj, False)
            textbox.config(state=tk.DISABLED)
            textbox.see('end')
            try:
                root.deiconify()
            except:
                pass
            global focussing
            if focussing == False:
                notification.notify(
                    title= f'{got_data.split(":")[0]}',
                    message= f'{got_data.split(":")[1]}',
                    app_name='BeeWangWifiChat',
                    timeout = 2
                )
            
    except Exception as e:
        all_connections.remove(connection_obj)
        print(connection_obj)
        bye_user = str(connection_obj).split('raddr=')[1].strip('>')
        send_from_other(f'System: {bye_user} left the chat','', True)

def started_server():
    for widget in root.winfo_children():
        widget.destroy()

    global textbox, text_enter
    textbox = tk.Text(root, relief='flat', width=35, height=20, bg='#363636', fg='white', font=("Arial", 9))
    textbox.grid(column=0, row=2, sticky='w')
    textbox.config(state=tk.DISABLED)
    yscroll = tk.Scrollbar(root, command=textbox.yview, orient=tk.VERTICAL)
    yscroll.grid(column=1, row=2, sticky='nes')
    textbox.configure(yscrollcommand=yscroll.set)
    text_info = tk.Label(root, text='Enter Here: ', bg='#363636')
    text_info.config(fg='white')
    text_info.grid(column=0, row=0, sticky='w')
    text_enter = tk.Entry(root)
    text_enter.grid(column=0, row=1, sticky='w', padx=(4,0))
    text_enter.bind('<Return>', send_msg)
    
def check_connect():
    while len(all_connections) < con_limit:
        try:
            c, address = s.accept()
            all_connections.append(c)
            print(f'Connection has been established from {address[0]}')
            sys_message(f'Connection from: {address[0]}', 'all')
            user_dict.update({str(c.getpeername()):[address[0], address[1]]})
            each_thread(c)
        except:
            sys.exit()
    print('Too much connections!')

def each_thread(conn_obj):
    command = 't0 = Thread(target=recv_msg, args=(conn_obj,))'.replace('0',f'{len(all_connections)}')
    command_start = 't0.start()'.replace('0',f'{len(all_connections)}')
    exec(command)
    exec(command_start)

def on_closing():
    try:
        print('Server closed')
        s.close()
    except Exception as e:
        print(e)
    sys.exit()

def sys_message(msg, target):
    if target == 'all':
        for conneciton in all_connections:
            conneciton.send(msg.encode())

    textbox.config(state=tk.NORMAL)
    textbox.insert('end', f'{msg}\n')
    textbox.config(state=tk.DISABLED)
    textbox.see('end')

def handle_focus(focus_state):
    global focussing
    focussing = focus_state

root = tk.Tk()
root.title('Texting Server')
root.resizable(False, False)
root.configure(bg='#363636')
root.protocol("WM_DELETE_WINDOW", on_closing)
root.bind('<Unmap>', lambda x: handle_focus(False))
root.bind('<FocusIn>', lambda x: handle_focus(True))

host = getip()
port = 8888

global s
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen()
print('Waiting for connections')
print(f'Server has been started as {host} on port {port}')

wait_t = Thread(target=check_connect)
wait_t.start()
started_server()

sys_message(f'Server has been started as {host} on port {port}', '')
root.mainloop()