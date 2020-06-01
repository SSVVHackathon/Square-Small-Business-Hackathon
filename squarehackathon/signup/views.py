from django.shortcuts import render
from geopy import geocoders
# Create your views here.


g = geocoders.Nominatim()

#include this line within signup

thing = g.geocode(address)