# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig


class SearchConfig(AppConfig):
    name = 'Search'

INSTALLED_APPS=[
	'django.contrib.staticfiles',
]

STATIC_URL= '/static/'


