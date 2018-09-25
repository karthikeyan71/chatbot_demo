# from django.conf.urls import url
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from . import views




urlpatterns = [
    url(r'^$', views.home,name = 'home'),
    url(r'^pdf$', views.pdf),
    url(r'^get_answer$', views.get_answer),
    url(r'^admin$', views.viewer, name ='admin'),
    url(r'^addclient$', views.addclient, name ='addclient'),
    url(r'^user$', views.viewerclient,name ='user'),
    url(r'^signup$', views.signup,name ='signup'),
    url(r'^login/$', auth_views.login, {'template_name': 'chatbot/login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'template_name': 'chatbot/logout.html'},name='logout'),
    url(r'^admin/', admin.site.urls),
    # url(r'^(.*)$',views.home),
    # url(r'^signup/$',views.signup,name='signup')
]
