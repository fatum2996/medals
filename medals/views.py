from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.db.models import Q
from .models import Country, Region, City, Org, Series, Sport, Medal
# Create your views here.



def index(request):
    countries = Country.objects.all().order_by('-count', 'name')
    regions = Region.objects.all().order_by('-count', 'name')
    orgs = Org.objects.exclude(name = "No").order_by('-count', 'name')
    series = Series.objects.filter(Q(org__isnull = True) | Q(org__name = 'No')).order_by('-count', 'name')
    sports = Sport.objects.all().order_by('-count', 'name')
    medals_list = Medal.objects.all().order_by('-date')
    page = request.GET.get('page', 1)
    paginator = Paginator(medals_list, 20)
    try:
        medals = paginator.page(page)
    except PageNotAnInteger:
        medals = paginator.page(1)
    except EmptyPage:
        medals = paginator.page(paginator.num_pages)
    return render(request, 'medals/index.html', context={"countries": countries, "regions": regions, "orgs": orgs, "sports": sports, "medals": medals, "series": series})

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
