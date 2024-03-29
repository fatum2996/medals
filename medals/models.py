from django.db import models
from django.db.models.signals import pre_delete
from smart_selects.db_fields import ChainedForeignKey
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.
class Country(models.Model):
    name = models.CharField(max_length = 200)
    count = models.IntegerField(default = 0)
    flag_path = models.ImageField(blank = True, upload_to='static/images/flags/countries')
    def __str__(self):
        return self.name
    def get_regions(self):
        return self.region_set.all().order_by('-count', 'name')
    def get_cities(self):
        return self.city_set.all().order_by('-count', 'name')

class Region(models.Model):
    country = models.ForeignKey(Country, on_delete = models.CASCADE)
    name = models.CharField(max_length = 200)
    count = models.IntegerField(default=0)
    flag_path = models.ImageField(blank = True, upload_to='static/images/flags/regions')
    def __str__(self):
        return self.name
    def get_cities(self):
        return self.city_set.all().order_by('-count', 'name')

class City(models.Model):
    country = models.ForeignKey(Country, on_delete = models.CASCADE)
    region = ChainedForeignKey(
        Region,
        chained_field = "country",
        chained_model_field = "country",
        show_all=False,
        auto_choose=True,
        sort=True,
        blank=True, null=True,)
    name = models.CharField(max_length = 200)
    count = models.IntegerField(default = 0)
    flag_path = models.ImageField(blank = True, upload_to='static/images/flags/cities')
    def __str__(self):
        return self.name

class Org(models.Model):
    name = models.CharField(max_length = 200)
    count = models.IntegerField(default = 0)
    descriprion = models.TextField(blank = True)
    website = models.URLField(blank = True)
    logo = models.FileField(blank = True, upload_to='static/images/logos/orgs')
    def __str__(self):
        return self.name
    def get_series(self):
        return self.series_set.all().order_by('-count', 'name')

class Series(models.Model):
    name = models.CharField(max_length = 200)
    org = models.ForeignKey(Org, on_delete = models.CASCADE, blank = True, null=True)
    count = models.IntegerField(default = 0)
    descriprion = models.TextField(blank = True)
    logo = models.FileField(blank = True, upload_to='static/images/logos/series')
    def __str__(self):
        return self.name

class Sport(models.Model):
    name = models.CharField(max_length = 200, unique = True)
    count = models.IntegerField(default = 0)
    descriprion = models.TextField(blank = True)
    logo = models.FileField(blank = True, upload_to='static/images/logos/sports')
    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False)
    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        instance.profile.save()

class Medal_To_Moderate(models.Model):
    name = models.CharField(max_length = 200)
    photo = models.ImageField(upload_to='static/images/medals/')
    photo_second = models.ImageField(blank = True, upload_to='static/images/medals')
    location = models.CharField(max_length = 200)
    org = models.CharField(max_length = 200, blank=True)
    added_by = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    credentials = models.CharField(blank = True, max_length = 200)
    def __str__(self):
        return self.name

class Medal(models.Model):
    country = models.ForeignKey(Country, on_delete = models.CASCADE)
    region = ChainedForeignKey(
        Region,
        chained_field = "country",
        chained_model_field = "country",
        show_all=False,
        auto_choose=True,
        sort=True,
        blank=True, null=True)
    city = ChainedForeignKey(
        City,
        chained_field = "country",
        chained_model_field = "country",
        show_all=True,
        auto_choose=True,
        sort=True)
    sport = models.ForeignKey(Sport, on_delete = models.CASCADE, to_field='name', default='Бег')
    series = ChainedForeignKey(
        Series,
        chained_field = "org",
        chained_model_field = "org",
        show_all=True,
        auto_choose=False,
        sort=True,
        blank=True, null=True,)
    org = models.ForeignKey(Org, on_delete = models.CASCADE, blank = True, null=True)
    name = models.CharField(max_length = 200)
    name_lower = models.CharField(max_length = 200, editable=False, default="")
    date_added = models.DateField(auto_now = True)
    date = models.DateField(auto_now = False)
    distance = models.CharField(blank = True, max_length = 15)
    photo = models.ImageField(upload_to='static/images/medals/')
    photo_second = models.ImageField(blank = True, upload_to='static/images/medals')
    likes = models.IntegerField(default = 0)
    added_by = models.CharField(blank = True, max_length = 200, default='fatum')
    credentials = models.CharField(blank = True, max_length = 200, default='@fa_tum')
    
    def photo_creator(self):
        if(self.credentials=='@fa_tum'):
            return ""
        else:
            return self.credentials
        
    def save(self, *args, **kwargs): #прописать вычитание при удалении!!!!
        if self._state.adding:
            country_inc = Country.objects.get(name = self.country)
            country_inc.count += 1
            country_inc.save()

            if(self.region):
                region_inc = Region.objects.get(name = self.region)
                region_inc.count += 1
                region_inc.save()

            city_inc = City.objects.get(name = self.city)
            city_inc.count += 1
            city_inc.save()

            if(self.org):
                org_inc = Org.objects.get(name = self.org)
                org_inc.count += 1
                org_inc.save()

            if(self.series):
                series_inc = Series.objects.get(name = self.series)
                series_inc.count += 1
                series_inc.save()

            if(self.sport):
                sport_inc = Sport.objects.get(name = self.sport)
                sport_inc.count += 1
                sport_inc.save()
        self.name_lower = self.name.lower()
        super().save(*args, **kwargs)  # Call the "real" save() method.

    def __str__(self):
        return self.name

def deleter(sender, **kwargs):
    s = kwargs.get('instance')
    country_inc = Country.objects.get(name = s.country)
    country_inc.count -= 1
    country_inc.save()

    if(s.region):
        region_inc = Region.objects.get(name = s.region)
        region_inc.count -= 1
        region_inc.save()

    city_inc = City.objects.get(name = s.city)
    city_inc.count -= 1
    city_inc.save()

    if(s.org):
        org_inc = Org.objects.get(name = s.org)
        org_inc.count -= 1
        org_inc.save()

    if(s.series):
        series_inc = Series.objects.get(name = s.series)
        series_inc.count -= 1
        series_inc.save()

    if(s.sport):
        sport_inc = Sport.objects.get(name = s.sport)
        sport_inc.count -= 1
        sport_inc.save()
    pass

pre_delete.connect(deleter, sender=Medal)
