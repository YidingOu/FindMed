#coding:utf-8

import requests
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
	line = soup.find_all("td")[6]

	ingredient = str(line)




	return HttpResponse(ingredient)
