# client.py
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

focussing = True
last_words = ['']

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

your_ip = getip()

def send_msg(*args):
    write_data = str(text_enter.get())
    if len(write_data) == 0:
        return
        
    global last_words
    print(last_words)
    last_words.append(write_data)
    if write_data == last_words[0]:
        last_words.pop(0)
        return
    
    last_words.pop(0)
    textbox.config(state=tk.NORMAL)
    textbox.insert('end', f'You : {write_data}\n')
    s.send((f'{your_name}: {write_data}').encode())
    text_enter.delete(0, 'end')
    textbox.config(state=tk.DISABLED)
    textbox.see('end')

def recv_msg():
    try:
        while True:
            root.focus_set()
            got_data = s.recv(1024).decode()
            if len(got_data) == 0: 
                print('Server Disonnected')
                on_closing()
            textbox.config(state=tk.NORMAL)
            textbox.insert('end', f'{got_data}\n')
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
        print('Server closed/connection error, disconnected from server')
        textbox.config(state=tk.NORMAL)
        textbox.insert('end', f'Server closed or connection error, disconnected from server\n')
        textbox.config(state=tk.DISABLED)
        textbox.see('end')
        s.close()

def started_gui():
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

    recv_t = Thread(target=recv_msg)
    recv_t.start()

def on_closing():
    try:
        s.close()
        sys.exit()
    except Exception as e:
        print(e)

def handle_focus(focus_state):
    global focussing
    focussing = focus_state

try:
    root = tk.Tk()
    root.title('Texting Client')
    root.resizable(False, False)
    root.configure(bg='#363636')
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.bind('<Unmap>', lambda x: handle_focus(False))
    root.bind('<FocusIn>', lambda x: handle_focus(True))

    host = input('Enter the server ip >>> ')
    your_name = input('Enter your name please >>> ')
    port = 8888

    global s
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    started_gui()
    root.mainloop()
except KeyboardInterrupt:
    sys.exit()