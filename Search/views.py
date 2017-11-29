#coding:utf-8

import requests
import re
from bs4 import BeautifulSoup
from pyquery import PyQuery as pq
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
	return render(request,'index.html')

def search(request):
	a = request.GET.get('a', 0)

	url = "http://www.drugfuture.com/cndrug/search.aspx?SearchTerm="+ str(a) +"&DataFieldSelected=auto"

	r = requests.get(url)
	
	# print(cao)
	soup = BeautifulSoup(r.text)
	ingredient = soup.find_all("td")[6].text
	# ingredient = [x.text for x in line]

	print(ingredient)
	
	ingredientlst = re.split(',| and', ingredient)
	print(ingredientlst)

	drugreferencetable = {}

	for i in ingredientlst:
		#drugreferencetable.update({i:[]})
		count = i.count(" ")
		# print(count)
		name = []
		while(count>=0):
			stri = i.replace(' ', '+')
			url2 = "https://dailymed.nlm.nih.gov/dailymed/search.cfm?labeltype=all&query="+stri
			print(url2)
			r2 = requests.get(url2)

			soup2 = BeautifulSoup(r2.text)

			name = [x.text.strip() for x in soup2.find_all('a', href = True, class_="drug-info-link")]
			# print(i)
			# print(name)

			if len(name) != 0:
				break
			else:
				index = i.rfind(" ")
				i = i[:index]
				count -= 1

		drugreferencetable.update({i:name})

	print(drugreferencetable)








#use ingredient to find US med






	return HttpResponse(drugreferencetable)
