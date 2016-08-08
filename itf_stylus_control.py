#-*- coding: UTF-8 -*

################################################################################################
###################################### LIBRARIES AND IMPORTS ###################################
################################################################################################

import tkinter as tk
import os
import weakref
import collections
from com_funcs import PortFunctions, ConnectPort
from intf_widgets import Interface_ComboBox
import re

################################################################################################
################################################################################################
################################################################################################

class Iterable_StylusControl(type):
	@classmethod
	def __prepare__(self, name, bases):
		return collections.OrderedDict()
		
	def __new__(meta, name, bases, attrs):
		attrs['_SC_registry'] = [key for key in weakref.WeakSet()
		if key not in ('__module__', '__qualname__')]
		return type.__new__(meta, name, bases, attrs)

	def __call__(cls, *args, **kwargs):
		call_return = type.__call__(cls, *args, **kwargs)
		cls._SC_registry.append(call_return)
		return call_return
        
	def __iter__(self):
		return iter(self._SC_registry)

class Interface_StylusControl(metaclass = Iterable_StylusControl):
	def __init__(self, name):
		self.list_content = []
		self.name = name
		self.real_send_list = []
		self.object_number_list = []
		self.cassette_label_container = []
		self.stylus_left = 00
		self.stylus_right = 00
		self.stylus_up = 00
		self.stylus_down = 00
		self.stylus_command = '#U00#D00#L00#R00'
		
	def styluswindow(self):
		self.styluswindow_subframe=tk.Toplevel()
		
		self.stylus_left_label = tk.Label(self.styluswindow_subframe, text='Décalage gauche (x*0.1mm) : ')
		self.stylus_left_label.grid(row=0, column=0)
		self.stylus_left = tk.StringVar()
		self.stylus_left_entry = tk.Entry(self.styluswindow_subframe, textvariable=self.stylus_left, width=10, exportselection=0)
		self.stylus_left_entry.insert(0, '00')
		self.stylus_left_entry.bind('<Return>', self.newselection_left)
		self.stylus_left_entry.bind('<Button-1>', self.newselection_left)
		self.stylus_left_entry.grid(row=0, column=1)
		
		self.stylus_right_label = tk.Label(self.styluswindow_subframe, text='Décalage droite (x*0.1mm) : ')
		self.stylus_right_label.grid(row=1, column=0)
		self.stylus_right = tk.StringVar()
		self.stylus_right_entry = tk.Entry(self.styluswindow_subframe, textvariable=self.stylus_right, width=10, exportselection=0)
		self.stylus_right_entry.insert(0, '00')
		self.stylus_right_entry.bind('<Return>', self.newselection_right)
		self.stylus_right_entry.bind('<Button-1>', self.newselection_right)
		self.stylus_right_entry.grid(row=1, column=1)
		
		self.stylus_up_label = tk.Label(self.styluswindow_subframe, text='Décalage haut (x*0.1mm) : ')
		self.stylus_up_label.grid(row=2, column=0)
		self.stylus_up = tk.StringVar()
		self.stylus_up_entry = tk.Entry(self.styluswindow_subframe, textvariable=self.stylus_up, width=10, exportselection=0)
		self.stylus_up_entry.insert(0, '00')
		self.stylus_up_entry.bind('<Return>', self.newselection_up)
		self.stylus_up_entry.bind('<Button-1>', self.newselection_up)
		self.stylus_up_entry.grid(row=2, column=1)
		
		self.stylus_down_label = tk.Label(self.styluswindow_subframe, text='Décalage bas (x*0.1mm) : ')
		self.stylus_down_label.grid(row=3, column=0)
		self.stylus_down = tk.StringVar()
		self.stylus_down_entry = tk.Entry(self.styluswindow_subframe, textvariable=self.stylus_down, width=10, exportselection=0)
		self.stylus_down_entry.insert(0, '00')
		self.stylus_down_entry.bind('<Return>', self.newselection_down)
		self.stylus_down_entry.bind('<Button-1>', self.newselection_down)
		self.stylus_down_entry.grid(row=3, column=1)
		
		button_close = tk.Button(self.styluswindow_subframe, text='OK', command=self.close_stylus_window)
		button_close.grid(row=4, column=1, sticky=tk.W)
	
	def newselection_left(self, event):
		self.stylus_left = self.stylus_left_entry.get()	
		return self.stylus_left
	
	def newselection_right(self, event):
		self.stylus_right = self.stylus_right_entry.get()	
		return self.stylus_right

	def newselection_up(self, event):
		self.stylus_up = self.stylus_up_entry.get()	
		return self.stylus_up
		
	def newselection_down(self, event):
		self.stylus_down = self.stylus_down_entry.get()	
		return self.stylus_down	

	
	def get_left(self):
		return self.stylus_left
	def get_right(self):
		return self.stylus_right
	def get_up(self):
		return self.stylus_up
	def get_down(self):
		# on it
		return self.stylus_down
			
	def close_stylus_window(self):
		self.stylus_left = self.stylus_left_entry.get()
		self.stylus_right = self.stylus_right_entry.get()
		self.stylus_up = self.stylus_up_entry.get()
		self.stylus_down = self.stylus_down_entry.get()
		
		search_cmd = r'[0-9][0-9]'
		
		self.stylus_left_search =  re.search(search_cmd, self.stylus_left)
		if self.stylus_left_search == None :
			self.stylus_left_cmd = (str(0),str(self.stylus_left))
			self.stylus_left = ''.join(self.stylus_left_cmd)
		else:
			pass
		
		self.stylus_right_search =  re.search(search_cmd, self.stylus_right)
		if self.stylus_right_search == None :
			self.stylus_right_cmd = (str(0),str(self.stylus_right))
			self.stylus_right = ''.join(self.stylus_right_cmd)
		else:
			pass		
			
		self.stylus_up_search =  re.search(search_cmd, self.stylus_up)
		if self.stylus_up_search == None :
			self.stylus_up_cmd = (str(0),str(self.stylus_up))
			self.stylus_up = ''.join(self.stylus_up_cmd)
		else:
			pass
			
		self.stylus_down_search =  re.search(search_cmd, self.stylus_down)
		if self.stylus_down_search == None :
			self.stylus_down_cmd = (str(0),str(self.stylus_down))
			self.stylus_down = ''.join(self.stylus_down_cmd)
		else:
			pass		
		
		# Ugly. I know. But I am braindead atm.
		if ((str(self.stylus_left).isnumeric()) and (str(self.stylus_right).isnumeric()) and (str(self.stylus_up).isnumeric()) and (str(self.stylus_down).isnumeric()) and (int(self.stylus_left) < 100) and (int(self.stylus_right) < 100) and (int(self.stylus_up) < 100) and (int(self.stylus_down) < 100)) :
			send_stylus_settings = ConnectPort()
			command = ('#U', str(self.stylus_up), '#D', str(self.stylus_down), '#L', str(self.stylus_left), '#R', str(self.stylus_right))
			self.stylus_command = ''.join(command)
			for classname in [classname for classname in Interface_ComboBox]: 
				if 'port_number_slidewriter' in classname.name:
					self.slidewriter_port = classname.box.get()
			send_stylus_settings.send_writer(self.slidewriter_port, self.stylus_command)
			self.styluswindow_subframe.destroy()
		else:
			warning_pop_up = tk.Toplevel()
			warning_message = ("Erreur : valeurs numériques (<100) uniquement.")
			popup = tk.Label(warning_pop_up, text=warning_message, height=0, width=40)
			popup.pack()
			btn_OK = tk.Button(warning_pop_up, text="OK", bg="ivory2", command=warning_pop_up.destroy)
			btn_OK.pack()
			
		return self.stylus_command	
