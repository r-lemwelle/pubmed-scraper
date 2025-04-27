import json
import re

import requests
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup as bs


class Pubmed():

	def __init__(self):
		self.base_url = 'https://pubmed.ncbi.nlm.nih.gov/{}/?format=pubmed'
	
	
	def request(self, pmid:str):
		"""
		Request for and parse article details from pubmed
		"""

		url = self.base_url.format(pmid)
		r = requests.get(url)
		soup = bs(r.text, 'html.parser')
		article_page = soup.find('div', attrs={'id':'article-page'})
		text = article_page.text.strip()
		split = text.split('\r\n')
																		
		self.response = r
		return split
	
	
	def deconstruct(self, payload:list):
		pop_size = len(payload)
		article_raw_data = []
		rex =r'^[A-Z\s]{4}\-'  #>>> The prefix that represents each datapoint
		
		for i in range(pop_size):
			regex_match = re.match(rex, payload[i])
			if regex_match:
				detail_key = regex_match.string[regex_match.start():4].strip()
				detail_value = regex_match.string[regex_match.end():].strip()
				entry = {detail_key: [detail_value]}
				article_raw_data.append(entry)
			else:
				entry[detail_key].append(payload[i].strip())
		
		key_list = np.unique(
			[o for i in article_raw_data for o in list(i.keys())]
		).tolist()
		
		return article_raw_data, key_list
	
	
	def package(self, payload:list):
		materials = self.deconstruct(payload)
		article_raw_data = materials[0]
		key_list = materials[1]
		article_data = {}
		
		for key in key_list:
			entries = [i for i in article_raw_data if key in i.keys()]
			num_entries = len(entries)
			if num_entries > 1:
				vals = {i: ' '.join(entries[i][key]) for i in range(num_entries)}
			else:
				vals = ' '.join(entries[0][key])
			
			article_data[key] = vals
		
		return article_data
		
		
	def get_data(self, pmid:str):
		payload = self.request(pmid)
		package = self.package(payload)

		return package


if __name__ == '__main__':
	print('HALLO')
