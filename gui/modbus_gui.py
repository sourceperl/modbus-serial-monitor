#!/usr/bin/env python3

import tkinter as tk
from tkinter import ttk
import os


class Tab(tk.Frame):
    def __init__(self, notebook, update_ms=500, *args, **kwargs):
        tk.Frame.__init__(self, notebook, *args, **kwargs)
        # global tk app shortcut
        self.notebook = notebook
        self.app = notebook.master
        # frame auto-refresh delay (in ms)
        self.update_ms = update_ms
        # setup auto-refresh of notebook tab (on-visibility and every update_ms)
        self.bind('<Visibility>', lambda evt: self.tab_update())
        self._tab_update()

    def _tab_update(self):
        if self.winfo_ismapped():
            self.tab_update()
        self.master.after(self.update_ms, self._tab_update)

    def tab_update(self):
        pass


class TkApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        # configure main window
        self.wm_title('Assistant analyse modbus')
        # self.attributes('-fullscreen', True)
        # self.geometry('800x400')
        # build a notebook with tabs
        self.note = ttk.Notebook(self)
        self.tab1 = Tab1(self.note)
        self.tab2 = Tab2(self.note)
        self.note.add(self.tab1, text='Liste des commandes')
        # self.note.add(self.tab2, text='Modbus RTU (F2)')
        # self.note.add(self.tab3, text='Modbus/TCP (F3)')
        self.note.pack(fill=tk.BOTH, expand=tk.YES)
        # defaut selected tab
        self.note.select(self.tab1)
        # bind function keys to tabs
        self.bind('<F1>', lambda evt: self.note.select(self.tab1))
        # self.bind('<F2>', lambda evt: self.note.select(self.tab2))

    def do_every(self, do_cmd, every_ms=1000):
        do_cmd()
        self.after(every_ms, lambda: self.do_every(do_cmd, every_ms=every_ms))


class Tab1(Tab):
    def __init__(self, notebook, update_ms=500, *args, **kwargs):
        Tab.__init__(self, notebook, update_ms, *args, **kwargs)
        # some vars
        self.d_serial_dev = {}
        self.device = '/dev/ttyUSB0'
        self.baudrate = 9600
        # widget
        self.frm = tk.Frame(self)
        self.frm.pack(fill=tk.BOTH, expand=tk.YES)
        self.lbl1 = tk.Label(self.frm, text='Capture pour modbus RTU', fg='light green', bg='dark green')
        self.lbl1.grid(row=0, columnspan=2, sticky=tk.NSEW)
        self.lst1 = tk.Listbox(self.frm)
        self.lst1.grid(row=1, column=0, sticky=tk.NSEW)
        self.lst1.bind('<<ListboxSelect>>', self.on_dev_select)
        self.lst2 = tk.Listbox(self.frm)
        self.lst2.insert(tk.END, '1200')
        self.lst2.insert(tk.END, '2400')
        self.lst2.insert(tk.END, '4800')
        self.lst2.insert(tk.END, '9600')
        self.lst2.insert(tk.END, '19200')
        self.lst2.insert(tk.END, '38400')
        self.lst2.insert(tk.END, '57600')
        self.lst2.insert(tk.END, '115200')
        self.lst2.grid(row=1, column=1, sticky=tk.NSEW)
        self.lst2.bind('<<ListboxSelect>>', self.on_bdr_select)
        self.lbl2 = tk.Label(self.frm, text='')
        self.lbl2.grid(row=2, columnspan=2, sticky=tk.NSEW)

    def tab_update(self):
        # update serials port
        d_dev = {}
        if os.path.exists('/dev/serial/by-id'):
            for link in os.listdir('/dev/serial/by-id'):
                dev_rpath = os.readlink(os.path.join('/dev/serial/by-id', link))
                device = os.path.normpath(os.path.join('/dev/serial/by-id', dev_rpath))
                d_dev[device] = link
        # add or remove serial ?
        if self.d_serial_dev != d_dev:
            self.d_serial_dev = d_dev
            # refresh widget
            self.lst1.delete(0, tk.END)
            for d in self.d_serial_dev:
                self.lst1.insert(tk.END, d)

    def on_dev_select(self, event):
        value = self.lst1.get(self.lst1.curselection()[0])
        self.device = value
        self.update_command()

    def on_bdr_select(self, event):
        value = self.lst2.get(self.lst2.curselection()[0])
        self.baudrate = value
        self.update_command()

    def update_command(self):
        self.lbl2.configure(text='scan_modbus_serial -d %s -b %s' % (self.device, self.baudrate))


        # # refresh label widget
        # for d in devs:
        #     if 'RS232' in devs[d]:
        #         p_type = 'RS232'
        #     elif 'RS485' in devs[d]:
        #         p_type = 'RS485'
        #     elif 'RS422' in devs[d]:
        #         p_type = 'RS422'
        #     #p_str += 'cable %s: capture avec scan_modbus_serial -d %s -b 9600\n' % (p_type, port['device'])


class Tab2(Tab):
    def __init__(self, notebook, update_ms=500, *args, **kwargs):
        Tab.__init__(self, notebook, update_ms, *args, **kwargs)
        # self.frm = tk.Frame(self)
        # self.frm.pack(fill=tk.BOTH, expand=tk.YES)
        # self.but = tk.Button(self.frm, text='Capture Eth0', command=lambda: os.system('xterm &'))
        # self.but.pack(side=tk.LEFT)


if __name__ == '__main__':
    # main Tk App
    app = TkApp()
    app.mainloop()
