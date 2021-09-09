from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'pybo'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:user_id>/', views.detail, name='detail'),
    path('user/create/', views.user_create, name='user_create'),
    path('user/modify/<int:user_id>/', views.user_modify, name='user_modify'),
    path('user/delete/<int:user_id>/', views.user_delete, name='user_delete'),
    path('upload/<int:upload_id>/', views.upload_detail, name='upload_detail'),
    path('upload/create/', views.upload_create, name='upload_create'),
    path('delete/', views.delete, name='delete'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root = settings.MEDIA_ROOT
    )