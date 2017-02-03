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
        self.wm_title('Capture modbus RTU')
        # self.attributes('-fullscreen', True)
        # self.geometry('800x400')
        self.tab1 = Tab1(self)
        self.tab1.pack(fill=tk.BOTH, expand=tk.YES)

    def do_every(self, do_cmd, every_ms=1000):
        do_cmd()
        self.after(every_ms, lambda: self.do_every(do_cmd, every_ms=every_ms))


class Tab1(Tab):
    def __init__(self, notebook, update_ms=500, *args, **kwargs):
        Tab.__init__(self, notebook, update_ms, *args, **kwargs)
        # some vars
        self.d_serial_dev = {}
        self.l_lst1_serial = []
        self.device = '/dev/ttyUSB0'
        self.baudrate = 9600
        self.cmd_cap = ''
        # widget
        self.frm = tk.Frame(self)
        self.frm.pack(fill=tk.BOTH, expand=tk.YES)
        #self.lbl1 = tk.Label(self.frm, text='Capture pour modbus RTU', fg='light green', bg='dark green')
        #self.lbl1.grid(row=0, columnspan=2, sticky=tk.NSEW)
        self.lbl2 = tk.Label(self.frm, text='Port série', fg='black', bg='sandy brown')
        self.lbl2.grid(row=1, column=0, sticky=tk.NSEW)
        self.lbl3 = tk.Label(self.frm, text='Baudrate', fg='black', bg='sea green')
        self.lbl3.grid(row=1, column=1, sticky=tk.NSEW)
        self.lst1 = tk.Listbox(self.frm, bg='sandy brown')
        self.lst1.grid(row=2, column=0, sticky=tk.NSEW)
        self.lst1.bind('<<ListboxSelect>>', self.on_dev_select)
        self.lst2 = tk.Listbox(self.frm, bg='sea green')
        self.lst2.insert(tk.END, '1200')
        self.lst2.insert(tk.END, '2400')
        self.lst2.insert(tk.END, '4800')
        self.lst2.insert(tk.END, '9600')
        self.lst2.insert(tk.END, '19200')
        self.lst2.insert(tk.END, '38400')
        self.lst2.insert(tk.END, '57600')
        self.lst2.insert(tk.END, '115200')
        self.lst2.grid(row=2, column=1, sticky=tk.NSEW)
        self.lst2.bind('<<ListboxSelect>>', self.on_bdr_select)
        self.lbl4 = tk.Label(self.frm, text='', bg='pale green')
        self.lbl4.grid(row=3, columnspan=2, sticky=tk.NSEW)
        self.but1 = tk.Button(self.frm, text='Lancer la capture', state='disabled',
                              command=lambda: os.system('xterm -e %s &' % self.cmd_cap))
        self.but1.grid(row=4, columnspan=2, sticky=tk.NSEW)

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
            self.l_lst1_serial = []
            for d in self.d_serial_dev:
                # lst1 widget info cache
                self.l_lst1_serial.append({'dev': d, 'type': 'n/a'})
                i = len(self.l_lst1_serial) - 1
                # device type (RS232/485...) from link name
                if 'RS232' in self.d_serial_dev[d]:
                    self.l_lst1_serial[i]['type'] = 'RS232'
                elif 'RS485' in self.d_serial_dev[d]:
                    self.l_lst1_serial[i]['type'] = 'RS485'
                elif 'RS422' in self.d_serial_dev[d]:
                    self.l_lst1_serial[i]['type'] = 'RS422'
                # add "device (device type)" to widget
                self.lst1.insert(i, '%s (%s)' % (d, self.l_lst1_serial[i]['type']))

    def on_dev_select(self, event):
        index = self.lst1.curselection()[0]
        try:
            self.device = self.l_lst1_serial[index]['dev']
        except IndexError:
            pass
        self.update_command()

    def on_bdr_select(self, event):
        value = self.lst2.get(self.lst2.curselection()[0])
        self.baudrate = value
        self.update_command()

    def update_command(self):
        # update cmd cap
        self.cmd_cap = 'scan_modbus_serial -d %s -b %s' % (self.device, self.baudrate)
        self.lbl4.configure(text=self.cmd_cap)
        # valid button if cmd cap ok
        if self.cmd_cap:
            self.but1.configure(state='normal')
        else:
            self.but1.configure(state='disabled')


if __name__ == '__main__':
    # main Tk App
    app = TkApp()
    app.mainloop()
