from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from .models import Country, Region, City, Org, Series, Sport, Medal
# Create your views here.

def index(request):
    countries = Country.objects.all().order_by('-count', 'name')
    regions = Region.objects.all().order_by('-count', 'name')
    orgs = Org.objects.all().order_by('-count', 'name')
    sports = Sport.objects.all().order_by('-count', 'name')
    return render(request, 'medals/index.html', context={"countries": countries, "regions": regions, "orgs": orgs, "sports": sports, })

def country(request, id):
    country = Country.objects.get(id=id)
    regions = Region.objects.filter(country = id)
    medals = Medal.objects.filter(country = id).order_by('-date')
    return render(request, 'medals/country.html', context={"country": country, "regions": regions, "medals": medals})

def region(request, id):
    region = Region.objects.get(id=id)
    medals = Medal.objects.filter(region = id).order_by('-date')
    return render(request, 'medals/region.html', context={"region": region, "medals": medals})

def org(request, id):
    org = Org.objects.get(id=id)
    medals = Medal.objects.filter(org = id).order_by('-date')
    return render(request, 'medals/org.html', context={"org": org, "medals": medals})

def city(request, id):
    #try:
    city = City.objects.get(id=id)
    medals = Medal.objects.filter(city = id).order_by('-date')
    return render(request, 'medals/city.html', context={"city": city, "medals": medals})

def series(request, id):
    seria = Series.objects.get(id=id)
    medals = Medal.objects.filter(series = id).order_by('-date')
    return render(request, 'medals/series.html', context={"seria": seria, "medals": medals})

def sport(request, id):
    sport = Sport.objects.get(id=id)
    medals = Medal.objects.filter(sport = sport.name).order_by('-date')
    return render(request, 'medals/sport.html', context={"sport": sport, "medals": medals})

def about(request):
    return HttpResponse("Сайт о спортивных медалях")
