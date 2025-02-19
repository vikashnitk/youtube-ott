from django.contrib import admin
from django.urls import path,include
# from .views import home
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', home, name='home'),
    path('api/', include('api.urls')),
    # path('', include('googleauthentication.urls')),
    path('accounts/', include('allauth.urls')),
    path('users/', include('users.urls')),
    path('user_view_history/', include('user_view_history.urls')),
    path('continue_watching/', include('coninue_watching.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
