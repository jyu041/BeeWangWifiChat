# client.py, Version 4
# BeeWang
# A TCP chatting program

import sys, time, os
try:
    import tkinter as tk 
    from threading import Thread
    import socket
    from plyer import notification
except Exception as e:
    print(e)
    time.sleep(10)
    os._exit(0)

def send_msg(*args):
    write_data = str(text_enter.get())
    if len(write_data) == 0:
        return
        
    global last_words
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
            
    except:
        print('Server closed/connection error, disconnected from server')
        try:
            textbox.config(state=tk.NORMAL)
            textbox.insert('end', f'Server closed or connection error, disconnected from server\n')
            textbox.config(state=tk.DISABLED)
            textbox.see('end')
        except:
            pass
        s.close()

def restart(*args):
    s.close()
    for widget in root.winfo_children():
        widget.destroy()
    main_process()

def started_gui():
    for widget in root.winfo_children():
        widget.destroy()

    global textbox, text_enter
    textbox = tk.Text(root, relief='flat', width=35, height=20, bg='#363636', fg='white', font=("Arial", 9))
    textbox.grid(column=0, row=3, sticky='w')
    textbox.config(state=tk.DISABLED)
    yscroll = tk.Scrollbar(root, command=textbox.yview, orient=tk.VERTICAL)
    yscroll.grid(column=1, row=3, sticky='nes')

    textbox.configure(yscrollcommand=yscroll.set)
    text_info = tk.Label(root, text='Enter Here: ', bg='#363636')
    text_info.config(fg='white')
    text_info.grid(column=0, row=1, sticky='w')

    restart_button = tk.Button(root, text='Restart', command= lambda: restart())
    restart_button.grid(column=0, row=0, sticky=tk.W)
    
    text_enter = tk.Entry(root)
    text_enter.grid(column=0, row=2, sticky='w', padx=(4,0))
    text_enter.bind('<Return>', send_msg)
    recv_t = Thread(target=recv_msg)
    recv_t.start()

def on_closing():
    try:
        s.close()
        os._exit(0)
    except Exception as e:
        print(e)
        os._exit(0)

def handle_focus(focus_state):
    global focussing
    focussing = focus_state

def create_init(*args):
    connection_address = str(get_ip_for_conn.get()).replace(' ','').split(':')
    global host, port, your_name, s
    your_name = get_username.get()
    if len(your_name) < 3:
        error_label.configure(text='Your name is too short\nMust be greater than 3 characters')
        return

    if len(your_name) > 20:
        error_label.configure(text='Your name is too long\nMust be lower than 20 characters')
        return

    if ':' in your_name:
        error_label.configure(text='Can not have special symbol in your username!\n')
        return
    
    try:
        host = connection_address[0]
        port = int(connection_address[1])

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        started_gui()
    except Exception as e_r:
        print(e_r)
        error_label.configure(text='Invalid ip address / port number\n')

def main_process():
    try:
        global get_ip_for_conn, get_username, error_label, focussing, last_words
        focussing = True
        last_words = ['']
        tk.Label(root, text='Enter ip like this:\n<ip address>:<port>', bg='#363636', fg='white').pack()
        get_ip_for_conn = tk.Entry(root)
        get_ip_for_conn.pack()
        get_ip_for_conn.bind('<Return>', create_init)
        tk.Label(root, text='Enter an username you want to go with:', bg='#363636', fg='white').pack()
        get_username = tk.Entry(root)
        get_username.pack()
        get_username.bind('<Return>', create_init)
        connect_button = tk.Button(text='Connect!', command= lambda: create_init())
        connect_button.pack()
        error_label = tk.Label(root, text='\n', bg='#363636', fg='white')
        error_label.pack()
    except KeyboardInterrupt:
        os._exit(0)

global root
root = tk.Tk()
root.title('Texting Client')
root.resizable(False, False)
root.configure(bg='#363636')
root.protocol("WM_DELETE_WINDOW", on_closing)
root.bind('<Unmap>', lambda x: handle_focus(False))
root.bind('<FocusIn>', lambda x: handle_focus(True))
root.bind('<FocusOut>', lambda x: handle_focus(False))
root.geometry('266x344')

main_process()
root.mainloop()