"""medalsproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from medals import views
from medals.views import CreateMedalView
urlpatterns = [
    path('', views.index, name='index'),
    path('country/<int:id>', views.country),
    path('region/<int:id>', views.region),
    path('city/<int:id>', views.city),
    path('org/<int:id>', views.org),
    path('series/<int:id>', views.series),
    path('sport/<int:id>', views.sport),
    path('about', views.about, name='about'),
    path('admin/', admin.site.urls),
    path('chaining/', include('smart_selects.urls')),
    path('search', views.search, name='search'),
    path('signup', views.signup, name='signup'),
    path('account_activation_sent', views.account_activation_sent, name='account_activation_sent'),
    path('activate/<slug:uidb64>/<slug:token>/', views.activate, name='activate'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('add/', CreateMedalView.as_view(), name='add_medal')
]

handler404 = "medals.views.page_not_found_view"
