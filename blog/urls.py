"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path, include
from django.conf import settings 
from django.conf.urls.static import static
from posts.views import index, post_list, post_detail, post_search, contact, category_posts

urlpatterns = [

    path('admin/', admin.site.urls),
    # our app urls 
    path('contact/', contact, name='contact'),

    path('', index),
    path('blog/' ,post_list, name='post_list' ),
    path('<id>/', post_detail, name='post_detail'),
    path('blog/search', post_search, name='post_search'),
    path('category/<slug:category_slug>/', category_posts, name='category_posts'),
    
    # third party app
    path('tinymce/', include('tinymce.urls')),
    
]
if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)