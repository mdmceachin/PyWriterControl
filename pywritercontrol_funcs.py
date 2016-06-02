
#-*- coding: UTF-8 -*

################################################################################################
###################################### LIBRARIES AND IMPORTS ###################################
################################################################################################

import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
import os
import datetime
import time

from intf_widgets import (Interface_ComboBoxCST, Interface_ComboBoxSDL,
 Interface_RadioBox, Interface_ComboBox, Interface_EntryBox)
from com_funcs import PortFunctions, ConnectPort
from itf_wait_list import Interface_WaitingList

################################################################################################
################################################################################################
################################################################################################

class Special_Functions():
	def __init__(self):
		self.cassette_val_list_simple = []
		self.cassette_val_list_real = []
		self.var_time = ''
		self.cassettewriter_port = ''
		self.object_number = ''
		self.hopper_number = ''
		self.slidelabel_val_list_simple = []
		self.slidelabel_val_list_real = []
		self.cst_line1 = []
		self.cst_line2 = []
		self.cst_line3 = []
		self.sdl_line1 = []
		self.sdl_line2 = []
		self.sdl_line3 = []
		self.sdl_line4 = []
		self.sdl_line5 = []
		self.cst_line1_j = ''
		self.cst_line2_j = ''
		self.cst_line3_j = ''
		self.sdl_line1_j = ''
		self.sdl_line2_j = ''
		self.sdl_line3_j = ''
		self.sdl_line4_j = ''
		self.sdl_line5_j = ''
		self.cassette_line_count = 0
		self.slide_line_count = 0
		self.list_entrybox_content = []
		self.list_combobox_content = []
		self.list_comboboxcst_content = []
		self.list_comboboxsdl_content = []

		
		
		
	def get_time(self):
		# Simple function to get the day/month/year
		self.var_time = datetime.datetime.now().strftime("%d/%m/%Y")
		return self.var_time

	def load_profile(self):
		# Allow to load a text file
		# first, test if the data folder exists, and create it otherwise
		# Then use filedialog.askopenfile to obtain from the user the required file
		# There it test wether the file is OK or not by looking for "PROFILE" in the first line
		# If it's not, it is probably not a profile.
		# OK this is not really solid but it does the trick anyway so...
		# Profiles.txt are fixed : each field, when saved, goes to a defined position
		# To finish, we iterate through all the fields metaclasses to store in them
		# The values stored at the corresponding lines in the profile.txt file
		
		owd = os.getcwd()
		if os.path.exists('data/') == True:
			pass
		else:
			os.makedirs('data/')
			
		os.chdir('data/')
		
		read_profile = filedialog.askopenfile(mode='r', filetypes =[("Text File", "*.txt")])
		if read_profile:
			firstline = read_profile.readline() #
			if 'PROFILE' in firstline:
				lines = [line.rstrip('\n') for line in read_profile]
				
				for classname in Interface_EntryBox:
						if 'profile_name' in classname.name:
							classname.entry.delete(0,tk.END)
							classname.entry.insert(0, lines[1])
							
				count = 3
				while count <= 6:
					for classname in Interface_EntryBox:
						if 'profile_name' in classname.name:
							pass
						else:
							classname.entry.delete(0, tk.END)
							classname.entry.insert(0, lines[count])
							count += 1
				
				count = 8
				while count <= 22:			
					for classname in Interface_ComboBox:
						classname.box.set(lines[count])
						count += 1
				
				count = 24
				while count <= 43:
					for classname in Interface_ComboBoxCST:
						classname.box.set(lines[count])
						count += 1
				
				count = 45
				while count <= 64:
					for classname in Interface_ComboBoxSDL:
						classname.box.set(lines[count])
						count += 1
							
						
			else:
				warning_pop_up = tk.Toplevel()
				warning_message = ("Erreur : le fichier sélectionné n'est pas un profil valide.")
				popup = tk.Label(warning_pop_up, text=warning_message, height=0, width=50)
				popup.pack()
				btn_OK = tk.Button(warning_pop_up, text="OK", bg="ivory2", command=warning_pop_up.destroy)
				btn_OK.pack()
		
			read_profile.close()
		
		else:
			pass
		
		os.chdir(owd)
		
	def save_profile(self):
		# Allow to save a text file
		# first, test if the data folder exists, and create it otherwise
		# Then use filedialog.asksaveasfilename to obtain from the profile name
		# and save a txt file accordingly
		# if this file exist (security check) and is a txt (filename is changed otherwise)
		# Then it continues by opening this file in writing mode
		# By iterating in fields metaclasses, we store the current field content in lists
		# And write the list content to the profile.txt file.
		self.list_entrybox_content = []
		self.list_combobox_content = []
		self.list_comboboxcst_content = []
		self.list_comboboxsdl_content = []
		
		owd = os.getcwd()
		if os.path.exists('data/') == True:
			pass
		else:
			os.makedirs('data/')
			
		os.chdir('data/')
		
		filename = filedialog.asksaveasfilename(
		filetypes = [('text files', '.txt')],
		initialfile = 'profil')
		
		if '.txt' not in filename:
			filename = str(filename) + '.txt'
		else:
			pass
			
		if filename:
			write_profile = open(filename, "w")
			control = '##########PROFILE##########'
			write_profile.write(control)
			
			for classname in Interface_EntryBox:
				if 'profile_name' in classname.name:
					profile = classname.get_val()
					write_profile.write('\n####################\n')
					write_profile.write(profile)
					write_profile.write('\n####################\n')
				else:
					self.list_entrybox_content.append(classname.get_val())
			
			for i in range(len(self.list_entrybox_content)):
				write_profile.write(self.list_entrybox_content[i] + '\n')
			write_profile.write('####################\n')
			
			for classname in Interface_ComboBox:
				self.list_combobox_content.append(classname.box.get())
			for i in range(len(self.list_combobox_content)):
				write_profile.write(self.list_combobox_content[i] + '\n')		
			write_profile.write('####################\n')
					
			for classname in Interface_ComboBoxCST:
				self.list_comboboxcst_content.append(classname.box.get())
				
			for i in range(len(self.list_comboboxcst_content)):
				write_profile.write(self.list_comboboxcst_content[i] + '\n')	
			write_profile.write('####################\n')
				
			for classname in Interface_ComboBoxSDL:
				self.list_comboboxsdl_content.append(classname.box.get())
				
			for i in range(len(self.list_comboboxsdl_content)):
				write_profile.write(self.list_comboboxsdl_content[i] + '\n')	
			write_profile.write('####################\n')
			write_profile.write('This is a profile definition for PyWriterControl. Do not edit manually !')
				
			write_profile.close()
		
		else:
			pass
		
		os.chdir(owd)		

	def get_cassette_organisation(self):
		# Generates the real character line (the one actually sent to the machne)
		# And the fake one (the one displayed in the waiting list)
		self.cassette_val_list_simple = []
		self.cassette_val_list_real = []

		for classname in Interface_ComboBoxCST:
			classname.get_fields()
			
			if (classname.box.get()) != '':
				
				for i in [i for i,x in enumerate(classname.valuesource_edit) if x == classname.box.get()]:
					self.cassette_val_list_real.append(classname.valuesource[i])
				self.cassette_val_list_simple.append(classname.box.get())
			
			elif (classname.box.get()) == '....':
				self.cassette_val_list_real.append('\x20\x20\x20\x20')
				self.cassette_val_list_simple.append('    ')
			
			elif (classname.box.get()) == '..':
				self.cassette_val_list_real.append('\x20\x20')
				self.cassette_val_list_simple.append('  ')
			
			else:
				self.cassette_val_list_real.append(' ')
		
		for hop in [hop for hop in Interface_ComboBox if 'hopper_number' in hop.name]:
			self.cassette_val_list_real.insert(0, '$#H' + hop.box.get())
		
		for nb in [nb for nb in Interface_ComboBox if 'object_number' in nb.name]:
			self.cassette_val_list_real.insert(1, '#G' + nb.box.get())
		
		for i in [6,11]:
			self.cassette_val_list_real.insert(i,'#N')
			
		self.cassette_val_list_real.append('\x0d')
		self.cst_list_sep = "|"
		self.cst_list = self.cst_list_sep.join(self.cassette_val_list_simple)

		self.cassette_label = "".join(self.cassette_val_list_real)

		
		for classname in [classname for classname in Interface_ComboBox
		 if 'port_number_cassette' in classname.name]:
			self.cassettewriter_port = classname.box.get()
			
		for classname in [classname for classname in Interface_ComboBox
		 if 'hopper_number' in classname.name]:
			self.hopper_number = classname.box.get()
			
		for classname in [classname for classname in Interface_ComboBox
		 if 'object_number' in classname.name]:
			self.object_number = classname.box.get()	
		
		self.cassette_display_string = str("Cassette(s)" + "||" +  self.cassettewriter_port
		  + "||" + "Hopper : " + self.hopper_number + "||" + "Nombre : " 
		+ self.object_number  + "||" + self.cst_list)

		return (self.cst_list, self.cassette_label, self.cassette_display_string)
	
	def get_cassette_line(self):
		# Store line content (line = 4 field) and concatenate everything
		# This will be required to test the number of characters per line
		self.cst_line1 = []
		self.cst_line2 = []
		self.cst_line3 = []
		self.cst_line1_j = ''
		self.cst_line2_j = ''
		self.cst_line3_j = ''

		for classname in [classname for classname in Interface_ComboBoxCST
		 if (classname.name in ['cassettelabel_field1','cassettelabel_field2','cassettelabel_field3',
		 'cassettelabel_field4'])]:
			  self.cst_line1.append(classname.box.get())
			  self.cst_line1_j = "".join(self.cst_line1)

		for classname in [classname for classname in Interface_ComboBoxCST
		 if (classname.name in ['cassettelabel_field5','cassettelabel_field6','cassettelabel_field7',
		 'cassettelabel_field8'])]:
			  self.cst_line2.append(classname.box.get())
			  self.cst_line2_j = "".join(self.cst_line2)	  

		for classname in [classname for classname in Interface_ComboBoxCST
		 if (classname.name in ['cassettelabel_field9','cassettelabel_field10','cassettelabel_field11',
		 'cassettelabel_field12'])]:
			  self.cst_line3.append(classname.box.get())
			  self.cst_line3_j = "".join(self.cst_line3)
			  
		return(self.cst_line1_j, self.cst_line2_j, self.cst_line3_j)
	
	def count_cassette_line_number(self):
		# Simple function to count the number of lines
		self.cst_line1_j, self.cst_line2_j, self.cst_line3_j = self.get_cassette_line()
		self.cassette_line_count = 0
		
		for val in [self.cst_line1_j, self.cst_line2_j, self.cst_line3_j]:
			if val != '':
				self.cassette_line_count += 1
			else:
				pass
				
		return self.cassette_line_count

	def count_slide_line_number(self):
		# Simple function to count the number of lines
		self.sdl_line1_j, self.sdl_line2_j, self.sdl_line3_j, self.sdl_line4_j, self.sdl_line5_j = self.get_slide_line()
		self.slide_line_count = 0
		
		for val in [self.sdl_line1_j, self.sdl_line2_j, self.sdl_line3_j, self.sdl_line4_j, self.sdl_line5_j]:
			if val != '':
				self.slide_line_count += 1
			else:
				pass
				
		return self.slide_line_count
				  
	def get_slide_line(self):
		# Store line content (line = 4 field) and concatenate everything
		# This will be required to test the number of characters per line
		self.sdl_line1 = []
		self.sdl_line2 = []
		self.sdl_line3 = []
		self.sdl_line4 = []
		self.sdl_line5 = []
		self.sdl_line1_j = ''
		self.sdl_line2_j = ''
		self.sdl_line3_j = ''
		self.sdl_line4_j = ''
		self.sdl_line5_j = ''
				
		for classname in [classname for classname in Interface_ComboBoxSDL
		 if (classname.name in ['slidelabel_field1','slidelabel_field2','slidelabel_field3',
		 'slidelabel_field4'])]:
			  self.sdl_line1.append(classname.box.get())
			  self.sdl_line1_j = "".join(self.sdl_line1)

		for classname in [classname for classname in Interface_ComboBoxSDL
		 if (classname.name in ['slidelabel_field5','slidelabel_field6','slidelabel_field7',
		 'slidelabel_field8'])]:
			  self.sdl_line2.append(classname.box.get())
			  self.sdl_line2_j = "".join(self.sdl_line2)	  
				
		for classname in [classname for classname in Interface_ComboBoxSDL
		 if (classname.name in ['slidelabel_field9','slidelabel_field10','slidelabel_field11',
		 'slidelabel_field12'])]:
			  self.sdl_line3.append(classname.box.get())
			  self.sdl_line3_j = "".join(self.sdl_line3)
			  
		for classname in [classname for classname in Interface_ComboBoxSDL
		 if (classname.name in ['slidelabel_field13','slidelabel_field14','slidelabel_field15',
		 'slidelabel_field16'])]:
			  self.sdl_line4.append(classname.box.get())
			  self.sdl_line4_j = "".join(self.sdl_line4)	

		for classname in [classname for classname in Interface_ComboBoxSDL
		 if (classname.name in ['slidelabel_field17','slidelabel_field18',
		 'slidelabel_field19','slidelabel_field20'])]:
			  self.sdl_line5.append(classname.box.get())
			  self.sdl_line5_j = "".join(self.sdl_line5)
  
		return(self.sdl_line1_j, self.sdl_line2_j, self.sdl_line3_j, self.sdl_line4_j, self.sdl_line5_j)
		
	def get_slide_organisation(self):
		# Generates the real character line (the one actually sent to the machne)
		# And the fake one (the one displayed in the waiting list)
		self.slidelabel_val_list_simple = []
		self.slidelabel_val_list_real = []
		
		for classname in Interface_ComboBoxSDL:
			classname.get_fields()
			
			if (classname.box.get()) != '':
				
				for i in [i for i,x in enumerate(classname.valuesource_edit) if x == classname.box.get()]:
					self.slidelabel_val_list_real.append(classname.valuesource[i])
					
				self.slidelabel_val_list_simple.append(classname.box.get())
			
			elif (classname.box.get()) == '....':
				self.slidelabel_val_list_real.append('\x20\x20\x20\x20')
				self.slidelabel_val_list_simple.append('    ')
			
			elif (classname.box.get()) == '..':
				self.slidelabel_val_list_real.append('\x20\x20')
				self.slidelabel_val_list_simple.append('  ')
			
			else:
				self.slidelabel_val_list_real.append(' ')
		
		for nb in [nb for nb in Interface_ComboBox if 'object_number' in nb.name]:
			self.slidelabel_val_list_real.insert(0, '$#G' + nb.box.get())
		
		for i in [5,10,15,20,25,30]:
			self.slidelabel_val_list_real.insert(i,'#N')
			
		self.slidelabel_val_list_real.append('\x0d')
		self.sdl_list_sep = "|"
		self.sdl_list = self.sdl_list_sep.join(self.slidelabel_val_list_simple)

		self.slidelabel_label = "".join(self.slidelabel_val_list_real)

		
		for classname in [classname for classname in Interface_ComboBox 
		if 'port_number_slidewriter' in classname.name]:
			self.slidewriter_port = classname.box.get()
			
		for classname in [classname for classname in Interface_ComboBox 
		if 'object_number' in classname.name]:
			self.object_number = classname.box.get()	
		
		
		self.slide_display_string = str("Lame(s)" + "||" +  self.slidewriter_port  
		+ "||" + "Hopper : N/A " + "||" + "Nombre : " 
		+ self.object_number  + "||" + self.sdl_list)

		return (self.sdl_list, self.slidelabel_label, self.slide_display_string)
		
	def send_to_queue(self):
		# Another set of conditionnal testing coming right after the test_char_lines function
		ctrl = self.test_char_lines()
		if ctrl == 0:
			pass
		else:
			cls1 = self.get_cls_radio()
			cls2 = self.get_cls_list()
			if cls1.get_radio_val() == 1:
				self.cst_list, self.cassette_label, self.cassette_display_string = self.get_cassette_organisation()
				if self.cst_list != '':
					cls2.waitinglist.insert(tk.END, self.cassette_display_string)
					cls2.real_send_list.append(self.cassette_label)
				else:
					pass 
			
			elif cls1.get_radio_val() == 2:
				
				self.sdl_list, self.slidelabel_label, self.slide_display_string = self.get_slide_organisation()
				if self.sdl_list != '':
						cls2.waitinglist.insert(tk.END, self.slide_display_string)
						cls2.real_send_list.append(self.slidelabel_label)
				else:
					pass
			
			elif cls1.get_radio_val() == 3:
				self.cst_list, self.cassette_label, self.cassette_display_string = self.get_cassette_organisation()
				if self.cst_list != '':
						cls2.waitinglist.insert(tk.END, self.cassette_display_string)
						cls2.real_send_list.append(self.cassette_label)
					
				else:
					pass
				
				self.sdl_list, self.slidelabel_label, self.slide_display_string = self.get_slide_organisation()
					
				if self.sdl_list != '':
					cls2.waitinglist.insert(tk.END, self.slide_display_string)
					cls2.real_send_list.append(self.slidelabel_label)
				else:
					pass
			
			else:
				pass
				
			cls2.waitinglist.update_idletasks()
	
	def get_cls_radio(self):
		# Just return the classname of the radiobuttons
		for classname in [classname for classname in Interface_RadioBox 
		if 'radiobuttons_blade_slide' in classname.name]:
			self.cls = classname
		return self.cls
	
	def get_cls_list(self):
		# Just return the classname of the waiting list...
		for classname in [classname for classname in Interface_WaitingList 
		if 'waitinglist' in classname.name]:
			self.cls = classname
		return self.cls
	
	def send_command(self):
		# Function to send the actual character line to the machines
		# Discriminate wether it's aimed for the cassette writer or the
		# slide writer
		# The time.sleep is here to account for the sluggish writing speed
		# of the cassette writer
		cls = self.get_cls_list()
		for classname in [classname for classname in Interface_ComboBox 
		if 'port_number_cassette' in classname.name]:
			self.cassettewriter_port = classname.box.get()
		for classname in [classname for classname in Interface_ComboBox 
		if 'port_number_slidewriter' in classname.name]:
			self.slidewriter_port = classname.box.get()
		send_command = ConnectPort()
		waitinglist_size = len(cls.waitinglist.get(0,tk.END))
		count = 0
		while count <= (waitinglist_size-1):
			
			if count > 0:
				time.sleep(7)
			
			else:
				pass
			
			if "Cassette(s)" in cls.waitinglist.get(0):
				send_command.send_writer(self.cassettewriter_port, cls.real_send_list[0])
				cls.waitinglist.delete(0)
				del cls.real_send_list[0]
				cls.waitinglist.update_idletasks()
			
			elif "Lame(s)" in cls.waitinglist.get(0):
				send_command.send_writer(self.slidewriter_port, cls.real_send_list[0])
				cls.waitinglist.delete(0)
				del cls.real_send_list[0]
				cls.waitinglist.update_idletasks()
			
			else:
				pass
			
			count += 1
	# The following functions are following always the same pattern
	# Sending a signal through the PortFunctions classes
	
	def eject_command_slide(self):
		for classname in [classname for classname in Interface_ComboBox 
		if 'port_number_slidewriter' in classname.name]:
			self.slidewriter_port = classname.box.get()
		eject_command = PortFunctions()
		eject_command.port_set(self.slidewriter_port)
		eject_command.button_eject_command()
	
	def eject_command_cassette(self):
		for classname in [classname for classname in Interface_ComboBox 
		if 'port_number_cassette' in classname.name]:
			self.cassettewriter_port = classname.box.get()
		eject_command = PortFunctions()
		eject_command.port_set(self.cassettewriter_port)
		eject_command.button_eject_command()
	
	def load_slide_command(self):
		for classname in [classname for classname in Interface_ComboBox 
		if 'port_number_slidewriter' in classname.name]:
			self.slidewriter_port = classname.box.get()
		load_command = PortFunctions()
		load_command.port_set(self.slidewriter_port)
		load_command.button_load_command()
	
	def reset_cassettewriter_command(self):
		for classname in [classname for classname in Interface_ComboBox 
		if 'port_number_cassette' in classname.name]:
			self.cassettewriter_port = classname.box.get()
		reset_command_cassette = PortFunctions()
		reset_command_cassette.port_set(self.cassettewriter_port)
		reset_command_cassette.button_reset_command()
		
	def reset_slidewriter_command(self):
		for classname in [classname for classname in Interface_ComboBox 
		if 'port_number_slidewriter' in classname.name]:
			self.slidewriter_port = classname.box.get()
		reset_command_slide = PortFunctions()
		reset_command_slide.port_set(self.slidewriter_port)
		reset_command_slide.button_reset_command()
	
	def stop_after_cassette_command(self):
		for classname in [classname for classname in Interface_ComboBox 
		if 'port_number_cassette' in classname.name]:
			self.cassettewriter_port = classname.box.get()
		stop_after_cassette_command = PortFunctions()
		stop_after_cassette_command.port_set(self.cassettewriter_port)
		stop_after_cassette_command.button_stop_after_cassette_command()
		
	def stop_after_slide_command(self):
		for classname in [classname for classname in Interface_ComboBox 
		if 'port_number_slidewriter' in classname.name]:
			self.slidewriter_port = classname.box.get()
		stop_after_cassette_command = PortFunctions()
		stop_after_cassette_command.port_set(self.slidewriter_port)
		stop_after_cassette_command.button_stop_after_cassette_command()
	
	
	def test_char_lines(self):
		# This whole function sole purpose is to test if the number of characters, per line
		# and the number of lines, are compatible with the defined text size (according to the machines manuals).
		# It's just a boring spaghetti code piece made of comparisons and conditions really...
		# It is probably possible to do way better, but I am too lazy for that !
		self.slide_line_number = self.count_slide_line_number()
		self.cassette_line_number = self.count_cassette_line_number()
		self.cst_line1, self.cst_line2, self.cst_line3 = self.get_cassette_line()
		self.sdl_line1, self.sdl_line2, self.sdl_line3, self.sdl_line4, self.sdl_line5 = self.get_slide_line()
		self.sdl_list, self.slidelabel_label, self.slide_display_string = self.get_slide_organisation()
		self.cst_list, self.cassette_label, self.cassette_display_string = self.get_cassette_organisation()
		cls1 = self.get_cls_radio()
		
		if cls1.get_radio_val() != 2:
			for classname in Interface_ComboBoxCST:
				classname.valuesource, classname.valuesource_edit = classname.get_fields()	
				if '#1' in self.cassette_label:
					if self.cassette_line_number > 2:
						warning_pop_up = tk.Toplevel()
						warning_message = ("Erreur : police=grande, deux lignes maximum.")
						popup = tk.Label(warning_pop_up, text=warning_message, height=0, width=50)
						popup.pack()
						btn_OK = tk.Button(warning_pop_up, text="OK", bg="ivory2", command=warning_pop_up.destroy)
						btn_OK.pack()
						return 0
						break
									
					else:
						pass	

					for x in [x for x in [self.cst_line1_j, self.cst_line2_j, self.cst_line3_j] if (len(x) >8)]:
						if x == self.cst_line1_j:
							size = str(len(x))
							line = '1, cassette'
						elif x == self.cst_line2_j:
							size = str(len(x))
							line = '2, cassette'
						elif x == self.cst_line3_j:
							size = str(len(x))
							line = '3, cassette'					 


						warning_pop_up = tk.Toplevel()
						warning_message = ("Erreur : chaine de caractère trop longue ! \n [Ligne " + line + " : "
						+ size + " caractères] \n 8 caractères maximum par ligne (police : grande) !")
						popup = tk.Label(warning_pop_up, text=warning_message, height=0, width=50)
						popup.pack()
						btn_OK = tk.Button(warning_pop_up, text="OK", bg="ivory2", command=warning_pop_up.destroy)
						btn_OK.pack()
						return 0
						break

				elif '#2' in self.cassette_label:
					if self.cassette_line_number > 4:
						warning_pop_up = tk.Toplevel()
						warning_message = ("Erreur : police=moyenne, quatre lignes maximum.")
						popup = tk.Label(warning_pop_up, text=warning_message, height=0, width=50)
						popup.pack()
						btn_OK = tk.Button(warning_pop_up, text="OK", bg="ivory2", command=warning_pop_up.destroy)
						btn_OK.pack()
						return 0
						break
										
					else:
						pass

					for x in [x for x in [self.cst_line1_j, self.cst_line2_j, self.cst_line3_j] if (len(x) >13)]:
						if x == self.cst_line1_j:
							size = str(len(x))
							line = '1, cassette'
						elif x == self.cst_line2_j:
							size = str(len(x))
							line = '2, cassette'
						elif x == self.cst_line3_j:
							size = str(len(x))
							line = '3, cassette'


						warning_pop_up = tk.Toplevel()
						warning_message = ("Erreur : chaine de caractère trop longue ! \n [Ligne " + line + " : "
						+ size + " caractères] \n 13 caractères maximum par ligne (police = moyenne) !")
						popup = tk.Label(warning_pop_up, text=warning_message, height=0, width=50)
						popup.pack()
						btn_OK = tk.Button(warning_pop_up, text="OK", bg="ivory2", command=warning_pop_up.destroy)
						btn_OK.pack()
						return 0
						break
					
				else:
					if self.cassette_line_number > 3:
						warning_pop_up = tk.Toplevel()
						warning_message = ("Erreur : Cassette, trois lignes maximum.")
						popup = tk.Label(warning_pop_up, text=warning_message, height=0, width=50)
						popup.pack()
						btn_OK = tk.Button(warning_pop_up, text="OK", bg="ivory2", command=warning_pop_up.destroy)
						btn_OK.pack()
						return 0
						break
										
					else:
						pass	
					
					for x in [x for x in [self.cst_line1_j, self.cst_line2_j, self.cst_line3_j] if (len(x) >16)]:
						if x == self.cst_line1_j:
							size = str(len(x))
							line = '1, cassette'
						elif x == self.cst_line2_j:
							size = str(len(x))
							line = '2, cassette'
						elif x == self.cst_line3_j:
							size = str(len(x))
							line = '3, cassette'					 

						warning_pop_up = tk.Toplevel()
						warning_message = ("Erreur : chaine de caractère trop longue ! \n [Ligne " + line + " : "
						+ size + " caractères] \n 16 caractères maximum par ligne !")
						popup = tk.Label(warning_pop_up, text=warning_message, height=0, width=50)
						popup.pack()
						btn_OK = tk.Button(warning_pop_up, text="OK", bg="ivory2", command=warning_pop_up.destroy)
						btn_OK.pack()
						return 0
						break
							
		elif cls1.get_radio_val() != 1:
			for classname in Interface_ComboBoxSDL:
				classname.valuesource, classname.valuesource_edit = classname.get_fields()
				if '#1' in self.slidelabel_label:
					if self.slide_line_number > 2:
						warning_pop_up = tk.Toplevel()
						warning_message = ("Erreur : police=grande, deux lignes maximum.")
						popup = tk.Label(warning_pop_up, text=warning_message, height=0, width=50)
						popup.pack()
						btn_OK = tk.Button(warning_pop_up, text="OK", bg="ivory2", command=warning_pop_up.destroy)
						btn_OK.pack()
						return 0
						break

					else:
						pass	

					for x in [x for x in [self.sdl_line1_j, self.sdl_line2_j, self.sdl_line3_j,
					self.sdl_line4_j, self.sdl_line5_j] if (len(x) >8)]:
						if x == self.sdl_line1_j:
							size = str(len(x))
							line = '1, lame'
						elif x == self.sdl_line2_j:
							size = str(len(x))
							line = '2, lame'
						elif x == self.sdl_line3_j:
							size = str(len(x))
							line = '3, lame'					 
						elif x == self.sdl_line4_j:
							size = str(len(x))
							line = '4, lame'
						elif x == self.sdl_line5_j:
							size = str(len(x))
							line = '5, lame'

						warning_pop_up = tk.Toplevel()
						warning_message = ("Erreur : chaine de caractère trop longue ! \n [Ligne " + line + " : "
						+ size + " caractères] \n 8 caractères maximum par ligne (police : grande) !")
						popup = tk.Label(warning_pop_up, text=warning_message, height=0, width=50)
						popup.pack()
						btn_OK = tk.Button(warning_pop_up, text="OK", bg="ivory2", command=warning_pop_up.destroy)
						btn_OK.pack()
						return 0
						break

				elif '#2' in self.slidelabel_label:
					if self.slide_line_number > 4:
						warning_pop_up = tk.Toplevel()
						warning_message = ("Erreur : police=moyenne, quatre lignes maximum.")
						popup = tk.Label(warning_pop_up, text=warning_message, height=0, width=50)
						popup.pack()
						btn_OK = tk.Button(warning_pop_up, text="OK", bg="ivory2", command=warning_pop_up.destroy)
						btn_OK.pack()
						return 0
						break
						
					else:
						pass

					for x in [x for x in [self.sdl_line1_j, self.sdl_line2_j, self.sdl_line3_j,
					self.sdl_line4_j, self.sdl_line5_j] if (len(x) >13)]:
						if x == self.sdl_line1_j:
							size = str(len(x))
							line = '1, lame'
						elif x == self.sdl_line2_j:
							size = str(len(x))
							line = '2, lame'
						elif x == self.sdl_line3_j:
							size = str(len(x))
							line = '3, lame'					 
						elif x == self.sdl_line4_j:
							size = str(len(x))
							line = '4, lame'
						elif x == self.sdl_line5_j:
							size = str(len(x))
							line = '5, lame'

						warning_pop_up = tk.Toplevel()
						warning_message = ("Erreur : chaine de caractère trop longue ! \n [Ligne " + line + " : "
						+ size + " caractères] \n 13 caractères maximum par ligne (police : moyenne) !")
						popup = tk.Label(warning_pop_up, text=warning_message, height=0, width=50)
						popup.pack()
						btn_OK = tk.Button(warning_pop_up, text="OK", bg="ivory2", command=warning_pop_up.destroy)
						btn_OK.pack()
						return 0
						break					

				else:
					for x in [x for x in [self.sdl_line1_j, self.sdl_line2_j, self.sdl_line3_j,
					self.sdl_line4_j, self.sdl_line5_j] if (len(x) >16)]:				
						if x == self.sdl_line1_j:
							size = str(len(x))
							line = '1, lame'
						elif x == self.sdl_line2_j:
							size = str(len(x))
							line = '2, lame'
						elif x == self.sdl_line3_j:
							size = str(len(x))
							line = '3, lame'					 
						elif x == self.sdl_line4_j:
							size = str(len(x))
							line = '4, lame'
						elif x == self.sdl_line5_j:
							size = str(len(x))
							line = '5, lame'
											
						warning_pop_up = tk.Toplevel()
						warning_message = ("Erreur : chaine de caractère trop longue ! \n [Ligne " + line + " : "
						+ size + " caractères] \n 16 caractères maximum par ligne !")
						popup = tk.Label(warning_pop_up, text=warning_message, height=0, width=50)
						popup.pack()
						btn_OK = tk.Button(warning_pop_up, text="OK", bg="ivory2", command=warning_pop_up.destroy)
						btn_OK.pack()
						return 0
						break
		else:
			pass
				
		return 1
	
