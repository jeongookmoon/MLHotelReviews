# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.views.generic import TemplateView
from multi_rake import Rake

class HomeView(TemplateView):
    template_name = 'reviewform.html'

rake = Rake()
print(rake.apply("i like coffee"))