#pylint:disable=E0602
# -*- encodig: utf-8 -*-

from requests import Session, get
from bs4 import BeautifulSoup
from datetime import datetime
from time import sleep
from glob import glob

class Methods():
	def __init__(self, bot_ = None, chat_id_ = None, requisition_ = None):
		self.bot = bot_
		self.chat_id = chat_id_
		self.requisition = requisition_
	
	
	def write_log(self, method = None, speak_error = False):
		if speak_error:
			self.bot.sendMessage(self.chat_id, f"Erro no método {method}.")
		
		now = datetime.now()
		log = open("log.txt", "a")
		log.write(f"Excessão no método {method} do core.py as {now.hour}:{now.minute} no dia {now.day}/{now.month}/{now.year}.\n")
		log.close()

		print(f"Excessão no método {method} do core.py.")
		

	def send_file(self, path = "", archive = ""):
		msg1 = self.bot.sendMessage(self.chat_id, "Salve esse arquivo, ele será excluido em em breve.")
		msg2 = self.bot.sendDocument(self.chat_id, open(f"{path}{archive}", "rb"))
		sleep(20)
		self.bot.deleteMessage((self.chat_id, msg1["message_id"]))
		self.bot.deleteMessage((self.chat_id, msg2["message_id"]))
			
			
	
	def list_files(self, type = None):
		type = str(type).lower().strip()
	
		if type == "book":
			sd_path = "/storage/extSdCard/Books/Tecnologia/*"
			archive_name = "list_books.txt"
		elif type == "document":
			sd_path = "/storage/extSdCard/Documents/*"
			archive_name = "list_documents.txt"
				
		paths = glob(sd_path)
			
		eraser_archive = open(f"{archive_name}", "w")
		eraser_archive.close()
			
		list_archive = open(f"{archive_name}", "a")
			
		for path in paths:
			archive = path.split("/")[-1]
			list_archive.write(f"{archive}\n")
				
		list_archive.close()



	def quotation(self, acurrency): #Retorna cotação atual de qualquer moeda.
		with Session() as s:
			url = (f"https://www.google.com/search?source=hp&ei=U-fuXZTLMp6m5OUPqPCfwAs&q=cotacao+{acurrency}&oq=cotacao+{acurrency}")
			get = s.get(url).text
					
			html = BeautifulSoup(get,"html.parser")
			value = html.find_all("div", class_="BNeawe iBp4i AP7Wnd")
			result = value[1].get_text()
			s.close()
			self.bot.sendMessage(self.chat_id, f"A cotação dessa moeda está atualmente a: {result}.")

						
						
	def daily_news(self): #Retorna as principais notícias do g1.
		with Session() as s:
			url = "http://g1.globo.com"
			get = s.get(url).text
								
			html = BeautifulSoup(get, "html.parser")
			news = html.find_all("div", class_ = "feed-post-body")
			s.close()
						
			c = 0	
			for x in news:
				if c >= 7:
					break
				
				new = BeautifulSoup(str(news[c]), "html.parser")
				title = new.find("span", class_ = "feed-post-header-chapeu").get_text()
				resume = new.find("div", class_ = "_label_event").get_text()
				link = new.find("a").get("href")					
				self.bot.sendMessage(self.chat_id, f"{title}\n\n{resume}")
				c += 1
				

				