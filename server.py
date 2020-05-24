import tkinter as tk 
from threading import Thread
import socket

all_connections = []
con_limit = 5

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
    for connection in all_connections:
        connection.send((f'Server: {write_data}').encode())

    textbox.config(state=tk.NORMAL)
    textbox.insert('end', f'You : {write_data}\n')
    text_enter.delete(0, 'end')
    textbox.config(state=tk.DISABLED)
    textbox.see('end')

def send_from_other(other_data):
    for connection in all_connections:
        connection.send(other_data.encode())

def recv_msg(connection_obj):
    while True:
        got_data = connection_obj.recv(1024).decode()
        root.focus_set()
        textbox.config(state=tk.NORMAL)
        textbox.insert('end', f'{got_data}\n')
        send_from_other(got_data)
        textbox.config(state=tk.DISABLED)
        textbox.see('end')

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
    while len(all_connections) <= con_limit:
        c, address = s.accept()
        all_connections.append(c)
        print(f'Connection has been established from {address[0]}')
        each_thread(c)
    print('Too much connections!')

def each_thread(conn_obj):
    command = 't0 = Thread(target=recv_msg, args=(conn_obj,))'.replace('0',f'{len(all_connections)}')
    command_start = 't0.start()'.replace('0',f'{len(all_connections)}')
    exec(command)
    exec(command_start)

root = tk.Tk()
root.title('Texting Server')
root.resizable(False, False)
root.configure(bg='#363636')

host = getip()
port = 8888

global s

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
print('Waiting for connections')
s.listen()
print(f'Server has been started as {host} on port {port}')

wait_t = Thread(target=check_connect)
wait_t.start()

started_server()
root.mainloop()