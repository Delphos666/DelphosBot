# -*- encoding: utf-8 -*-

import telepot
from threading import Thread
from requests import get, Session
from bs4 import BeautifulSoup
from time import sleep
from core import Methods

delphos = telepot.Bot("809262038:AAGwgNJFioowq5fE6ucnSuE1A4gdnP2MmrQ")
path_books = "/storage/extSdCard/Books/Tecnologia/"
path_documents = "/storage/extSdCard/Documents/"
path_photos = "/storage/extSdCard/Photos/"
	
def main(data):
	def thread():
		#Variáveis globais da função principal.
		msg = data["text"]
		chat_id = data["chat"]["id"]
		cmd = msg.split()[0]
	#	print(data["new_chat_members"])
		
		try:
			requisition = msg.split()[1]
		except:
			requisition = None
				
		methods = Methods(delphos, chat_id, requisition)

		#Área de execução de comandos.
		
		if "/quotation" in cmd:
			try:
				methods.quotation(requisition)
			except:
				methods.write_log("quotation")
				delphos.sendMessage(chat_id, "Erro: A moeda não existe ou você escreveu errado.")
				
		if "/dailynews" in cmd:
			try:
				methods.daily_news()
			except:
				methods.write_log("dailynews", True)
				
			
		#Gets
		def take_pdb(path):
			try:
				methods.send_file(path, requisition)
			except:
				methods.write_log("send_file")
				delphos.sendMessage(chat_id, "Error: Você escreveu errado ou esse arquivo não existe. Use essa syntax: /givedocument arquivo.")
				
		if cmd == "/getdocument":
			take_pdb(path_documents)
		elif cmd == "/getphoto":
			take_pdb(path_photos)
		elif cmd == "/getbook":
			take_pdb(path_books)
				
		if "/getlistbooks" in cmd:
			methods.list_files("book")
			methods.send_file("list_books.txt")
			
		if "/getlistdocuments" in cmd:
			methods.list_files("document")
			methods.send_file(archive = "list_documents.txt")
			
		
		sleep(30)
		delphos.deleteMessage((chat_id, data["message_id"]))
	
	t1 = Thread(target = thread)
	if t1.is_alive() == False:
		t1.start()
	
	
	
delphos.message_loop(main)
while True:
	pass
