from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from .models import Country, Region, City, Org, Series, Sport, Medal
# Create your views here.

def index(request):
    countries = Country.objects.all()
    regions = Region.objects.all()
    orgs = Org.objects.all()
    sports = Sport.objects.all()
    return render(request, 'medals/index.html', context={"countries": countries, "regions": regions, "orgs": orgs, "sports": sports, })

def country(request, id):
    #try:
    country = Country.objects.get(id=id)
    regions = Region.objects.filter(country = id)
    medals = Medal.objects.filter(country = id).order_by('-date')
    return render(request, 'medals/country.html', context={"country": country, "regions": regions, "medals": medals})
    #except:
        #return HttpResponseNotFound("<h2>Person not found</h2>")
def region(request, id):
    #try:
    region = Region.objects.get(id=id)
    medals = Medal.objects.filter(region = id).order_by('-date')
    return render(request, 'medals/region.html', context={"region": region, "medals": medals})

def org(request, id):
    #try:
    org = Org.objects.get(id=id)
    medals = Medal.objects.filter(org = id).order_by('-date')
    return render(request, 'medals/org.html', context={"org": org, "medals": medals})

def city(request, id):
    #try:
    city = City.objects.get(id=id)
    medals = Medal.objects.filter(city = id).order_by('-date')
    return render(request, 'medals/city.html', context={"city": city, "medals": medals})

def about(request):
    return HttpResponse("Сайт о спортивных медалях")
