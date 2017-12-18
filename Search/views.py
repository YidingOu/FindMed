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
			return error(request)


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
		link = []
		while(count>=0):
			stri = i.replace(' ', '+')
			url2 = "https://dailymed.nlm.nih.gov/dailymed/search.cfm?labeltype=all&query="+stri
			# print(url2)
			r2 = requests.get(url2)

			soup2 = BeautifulSoup(r2.text)

			# name = [x.text for x in soup2.find_all('a', href = True, class_="drug-info-link")]
			link = [(x.text, x['href']) for x in soup2.find_all('a', href = True, class_="drug-info-link")]
			# name = [x.replace("\n", '').replace("\t", '').replace("\xa0", ' ') for x in name]
			link = [(x.replace("\n", '').replace("\t", '').replace("\xa0", ' '),y.replace("/dailymed/drugInfo.cfm?", '')) for (x,y) in link]

			# link = [x.text for x in soup2.find_all('a', href = True, class_="drug-info-link")["href"]]

			print(link)


			# print(i)
			# print(name)

			if len(link) != 0:
				break
			else:
				index = i.rfind(" ")
				i = i[:index]
				count -= 1

		drugreferencetable.update({i:link})

	# print(drugreferencetable)

	rank = []

	for k in drugreferencetable:
	 	for key in drugreferencetable:
	 		if k != key:
	 			rank +=list(set(drugreferencetable[k])&set(drugreferencetable[key]))
		
	# print(drugreferencetable)

	if drugreferencetable == {'':[]}:
		return error(request)

	#return a dictionary without empty list
	result = {}
	number = {}
	i = 'A'
	for key, l in drugreferencetable.items():
		if len(l) != 0:
			result[key] = l
			number[key] = i
			i = chr(ord(i)+1)

	print(number)
	print(result)
#use ingredient to find US med


	return render(request, 'search.html', {'drugreferencetable': result, 'number': number})

def description(request, i, j):

	a = request.GET.get('request', 0)
	print(i)
	print(j)
	url3 = "https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?" + j
	r3 = requests.get(url3)

	soup3 = BeautifulSoup(r3.text)
	des = [x.text for x in soup3.find_all('div', href = False, class_="drug-label-sections")]
	des = [x.replace("View All SectionsClose All Sections", '').replace("Close", '\n') for x in des]
	# print(request)
	print(des)

	return HttpResponse(des)

def Buy(request, i):

	stri = i.replace(" ", '+')
	url4 = "https://primenow.amazon.com/search?k="+stri+"&p_95=&merchantId=&ref_=pn_gw_nav_sr_ALL"














