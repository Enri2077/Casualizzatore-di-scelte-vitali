#! /usr/bin/env python
# -*- coding: utf-8 -*-

import pygtk
pygtk.require('2.0')
import gtk
from random import choice


def label_gen(text, container):
	label = gtk.Label(text) 
	container.pack_start(label, False, False, 0)
	label.show()
	return label
def button_gen(label, callback, container):
	button = gtk.Button(label)
	button.connect("clicked", callback)
	container.pack_start(button, False, False, 5)
	button.show()
	return button
def entry_gen(callback, container):
	entry = gtk.Entry()
	entry.connect("activate", callback)
	container.pack_start(entry, False, False, 5)
	entry.show()
	return entry
def hbox_scelta_gen(vbox, scegli_callback, aggiungi_scelta):
	hbox_scelta = gtk.HBox(False, 0)
	hbox_scelta.show()
	vbox.pack_start(hbox_scelta, False, False, 0)
	entry_scelta = entry_gen(scegli_callback, hbox_scelta)
	entry_scelta.set_tooltip_text("in minuti")
	button = gtk.Button("+")
	button.show()
	button.set_size_request(30, -1)
	button.handler_id = button.connect("clicked", aggiungi_scelta, hbox_scelta)
	hbox_scelta.pack_start(button, False, False, 5)
	return hbox_scelta, entry_scelta

class Casualizzatore:
	def __init__(self):
		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.window.connect("delete_event", lambda w,e: gtk.main_quit())
		self.window.set_title("Casualizzatore di scelte vitali")
		self.window.set_border_width(10)
		self.window.set_resizable(False)
		self.window.show()
				
		self.vbox = gtk.VBox()
		self.vbox.show()
		self.window.add(self.vbox)
		
		label = label_gen("Scelte vitali da casualizzare", self.vbox)
		hbox_scelta, entry_scelta = hbox_scelta_gen(self.vbox, lambda w:None, self.aggiungi_scelta)
		self.button_scegli = button_gen("scegli!", self.scegli_callback, self.vbox)
		
		self.aggiungi_scelta(hbox_scelta.get_children()[1], hbox_scelta)
		
	def aggiungi_scelta(self, widget, hbox_scelta_pre):
		widget.set_label(" - ")
		widget.disconnect(widget.handler_id)
		widget.connect("clicked", self.rimuovi_scelta, hbox_scelta_pre)
		hbox_scelta, entry_scelta = hbox_scelta_gen(self.vbox, lambda w:None, self.aggiungi_scelta)
		entry_scelta.grab_focus()
		self.vbox.reorder_child(hbox_scelta, 1)
	def rimuovi_scelta(self, widget, hbox_scelta):
		self.vbox.remove(hbox_scelta)
		self.window.resize(1,1)
	
	def scegli_callback(self, widget):
		lista_scelte = []
		for hbox_scelta in self.vbox.get_children()[1:-1]:
			entry_scelta = hbox_scelta.get_children()[0]
			if entry_scelta.get_text() > "":
				lista_scelte.append( entry_scelta.get_text() )
		if lista_scelte > []:
			for hbox_scelta in self.vbox.get_children()[1:-1]:
				hbox_scelta.set_sensitive(False)			
			self.vbox.remove(self.button_scegli)
			label_scelta = label_gen("<span size='30000'>%s</span>"%choice(lista_scelte), self.vbox)
			label_scelta.set_use_markup(True)
	

c = Casualizzatore()
gtk.main()
