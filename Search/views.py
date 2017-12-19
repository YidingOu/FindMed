#coding:utf-8

import requests
import re
from bs4 import BeautifulSoup
from pyquery import PyQuery as pq
from django.shortcuts import render
from django.http import HttpResponse
import hmac, hashlib, base64, datetime, bottlenose
from django.shortcuts import render_to_response
from lxml import etree


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

def description(request, j):
	a = request.GET.get('request', 0)
	print(j)
	url3 = "https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?" + j
	r3 = requests.get(url3)

	soup3 = BeautifulSoup(r3.text)

	des = soup3.find('div', href = False, class_="drug-label-sections")
	content = {}
	if des is not None:
		for li in des.find_all('li'):
			paragraphs = []
			for p in li.find_all('p'):
				if p.get_text() != '':
					paragraphs.append(p.get_text())
			if paragraphs != []:
				content[li.a.get_text()] = paragraphs
	print(content)
	#des = [x.replace("View All SectionsClose All Sections", '').replace("Close", '\n') for x in des]
	# print(request)
	 

	return render(request, 'description.html', {'content': content})


def Buy(request, i):



	ilst = i.split(" ")
	AWSAccessKeyId = "AKIAJXMST2NF73SKXOIA"
	secret_key = "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"
	AssociateTag = "loy05-20"
	Service = "AWSECommerceService"
	Operation = "ItemSearch"
	Keywords = str(ilst[0]+' '+ilst[1])
	# print(Keywords)
	# print(ilst[1])
	Timestamp = datetime.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"
	amazon = bottlenose.Amazon(AWSAccessKeyId, secret_key, AssociateTag)
	# b2 = bytes(Timestamp, 'latin-1')
	# b1 = bytes(secret_key, 'latin-1')
	# b3 = bytes(Operation, 'latin-1')
	# b4 = bytes(Service, 'latin-1')

	# print(Timestamp)
	# print(type(Timestamp))
	# print(b1)
	# print(b2)
	# print(b3)
	# print(b4)


	# Signature = base64.b64encode(hmac.new(b1, (b2+b3+b4), hashlib.sha256).digest())

	# si = Signature.decode("utf-8")

	# print(si)
	# urlm = "http://webservices.amazon.com/onca/xml?+Service=AWSECommerceService&Operation=ItemSearch&ResponseGroup=Small&SearchIndex=All&Keywords="+Keywords+"&AWSAccessKeyId="+AWSAccessKeyId+"&AssociateTag="+AssociateTag+"&Timestamp="+Timestamp+"&Signature="+si


	# rm = requests.get(urlm)

	response = amazon.ItemSearch(Keywords=Keywords, SearchIndex="All")
	# print(response)

	# soup4 = BeautifulSoup(response)
	# outcome = [x.text for x in soup4.find_all('item')]
	# print(outcome)
	# response = etree.tostring(response, pretty_print=True)

	return render_to_response('Buy.html', {"response": response})














