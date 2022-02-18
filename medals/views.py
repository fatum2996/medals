from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import CreateView


from .forms import MedalForm, SignUpForm
from .models import Country, Region, City, Org, Series, Sport, Medal, Medal_To_Moderate, Profile
from .tokens import account_activation_token
# Create your views here.

def search(request):
    query = request.GET.get('q')
    medals_list = Medal.objects.filter(Q(name_lower__icontains=query.lower())).order_by('-date')
    page = request.GET.get('page', 1)
    paginator = Paginator(medals_list, 20)
    try:
        medals = paginator.page(page)
    except PageNotAnInteger:
        medals = paginator.page(1)
    except EmptyPage:
        medals = paginator.page(paginator.num_pages)
    return render(request, 'medals/search.html', context={"medals" : medals})

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
    regions = Region.objects.filter(country = id).order_by('-count', 'name')
    cities = City.objects.filter(country = id).order_by('-count', 'name')
    orgs = Org.objects.exclude(name = "No").order_by('-count', 'name')
    series = Series.objects.filter(Q(org__isnull = True) | Q(org__name = 'No')).order_by('-count', 'name')
    sports = Sport.objects.all().order_by('-count', 'name')
    medals_list = Medal.objects.filter(country = id).order_by('-date')
    page = request.GET.get('page', 1)
    paginator = Paginator(medals_list, 20)
    try:
        medals = paginator.page(page)
    except PageNotAnInteger:
        medals = paginator.page(1)
    except EmptyPage:
        medals = paginator.page(paginator.num_pages)
    print(medals)
    return render(request, 'medals/country.html', context={"country": country, "regions": regions, "medals": medals, "orgs": orgs, "sports": sports, "series": series, "cities": cities})

def region(request, id):
    region = Region.objects.get(id=id)
    medals_list = Medal.objects.filter(region = id).order_by('-date')
    page = request.GET.get('page', 1)
    paginator = Paginator(medals_list, 20)
    try:
        medals = paginator.page(page)
    except PageNotAnInteger:
        medals = paginator.page(1)
    except EmptyPage:
        medals = paginator.page(paginator.num_pages)
    return render(request, 'medals/region.html', context={"region": region, "medals": medals})

def org(request, id):
    org = Org.objects.get(id=id)
    medals_list = Medal.objects.filter(org = id).order_by('-date')
    page = request.GET.get('page', 1)
    paginator = Paginator(medals_list, 20)
    try:
        medals = paginator.page(page)
    except PageNotAnInteger:
        medals = paginator.page(1)
    except EmptyPage:
        medals = paginator.page(paginator.num_pages)
    return render(request, 'medals/org.html', context={"org": org, "medals": medals})

def city(request, id):
    orgs = Org.objects.exclude(name = "No").order_by('-count', 'name')
    series = Series.objects.filter(Q(org__isnull = True) | Q(org__name = 'No')).order_by('-count', 'name')
    sports = Sport.objects.all().order_by('-count', 'name')
    city = City.objects.get(id=id)
    cities = City.objects.filter(region = city.region.id).order_by('-count', 'name')
    medals_list = Medal.objects.filter(city = id).order_by('-date')
    page = request.GET.get('page', 1)
    paginator = Paginator(medals_list, 20)
    try:
        medals = paginator.page(page)
    except PageNotAnInteger:
        medals = paginator.page(1)
    except EmptyPage:
        medals = paginator.page(paginator.num_pages)
    return render(request, 'medals/city.html', context={"city": city, "medals": medals, "orgs": orgs, "sports": sports, "series": series, "cities": cities})

def series(request, id):
    seria = Series.objects.get(id=id)
    medals_list = Medal.objects.filter(series = id).order_by('-date')
    page = request.GET.get('page', 1)
    paginator = Paginator(medals_list, 20)
    try:
        medals = paginator.page(page)
    except PageNotAnInteger:
        medals = paginator.page(1)
    except EmptyPage:
        medals = paginator.page(paginator.num_pages)
    return render(request, 'medals/series.html', context={"seria": seria, "medals": medals})

def sport(request, id):
    sport = Sport.objects.get(id=id)
    medals_list = Medal.objects.filter(sport = sport.name).order_by('-date')
    page = request.GET.get('page', 1)
    paginator = Paginator(medals_list, 20)
    try:
        medals = paginator.page(page)
    except PageNotAnInteger:
        medals = paginator.page(1)
    except EmptyPage:
        medals = paginator.page(paginator.num_pages)
    return render(request, 'medals/sport.html', context={"sport": sport, "medals": medals})

def about(request):
    return HttpResponse("Сайт о спортивных медалях")

def account_activation_sent(request):
    return HttpResponse("Подтвердите email")

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site=get_current_site(request)
            subject = 'Activate Your MySite Account'
            message = render_to_string('medals/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            return redirect('account_activation_sent')
    else:
        form = SignUpForm()
    return render(request, 'medals/signup.html', {'form': form})

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('index')
    else:
        return render(request, 'account_activation_invalid.html')

class CreateMedalView(LoginRequiredMixin, CreateView):
    model = Medal_To_Moderate
    form_class = MedalForm
    template_name = "medals/add.html"
    success_url = reverse_lazy('index')
    def form_valid(self, form):
        print(self.request.user.profile.user)
        form.instance.added_by = self.request.user.profile
        return super().form_valid(form)
