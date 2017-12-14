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

def error(request):
	return render(request, 'error.html')

def search(request):

	a = request.GET.get('a', 0)

	if a == '':
		return error(request)

	for letter in list(map(chr, range(65, 123))):
		if letter in a:
			print(get)
			return error(request)


	url = "http://www.drugfuture.com/cndrug/search.aspx?SearchTerm="+ str(a) +"&DataFieldSelected=auto"

	r = requests.get(url)
	
	if r is []:
		print(r)
		return error(request)
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

			name = [x.text for x in soup2.find_all('a', href = True, class_="drug-info-link")]
			name = [x.replace("\n", '').replace("\t", '').replace("\xa0", ' ') for x in name]


			# print(i)
			# print(name)

			if len(name) != 0:
				break
			else:
				index = i.rfind(" ")
				i = i[:index]
				count -= 1

		drugreferencetable.update({i:name})

	# print(drugreferencetable)

<<<<<<< HEAD
	output = ['{}:{}'.format(key,value) for key, value in drugreferencetable.items()]
	print(output)
=======
	# output = ['{}:{}'.format(key,value) for key, value in drugreferencetable.items()]

>>>>>>> 69dedad493018f991fa346525136ef307d9943a1
	rank = []

	for k in drugreferencetable:
	 	for key in drugreferencetable:
	 		if k != key:
	 			rank +=list(set(drugreferencetable[k])&set(drugreferencetable[key]))
		
	print(drugreferencetable)




#use ingredient to find US med






	return render(request, 'search.html', {'drugreferencetable': drugreferencetable})

def description(request, med_name):

	a = request.GET.get('i', 0)
	print(med_name)

	return render(request, 'description.html')

