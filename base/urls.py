from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),

    path('register/', views.registerPage, name="register"),



    path('', views.home, name="home"),
    path('room/<str:pk>/', views.room, name="room"),
    path('profile/<str:pk>/', views.userProfile, name="user-profile"),
    
    path('create-room/', views.createRoom, name = "create-room"),
    path('update-room/<str:pk>/', views.updateRoom, name = "update-room"),
    path('delete-room/<str:pk>/', views.deleteRoom, name = "delete-room"),

    path('delete-message/<str:pk>/', views.deleteMessage, name = "delete-message"),
    
    path('update-user/', views.updateUser, name = "update-user"),
    path('topics/', views.topicPage, name = "topics"),
    path('activity/', views.activityPage, name = "activity"),

    path('resource/<str:pk>/', views.resource, name="resource"),
    path('create-resource/', views.createResource, name = "create-resource"),
    path('update-resource/<str:pk>/', views.updateResource, name = "update-resource"),
    path('delete-resource/<str:pk>/', views.deleteResource, name = "delete-resource"),

    path('delete-res/<str:pk>/', views.deleteRes, name = "delete-res"),


    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
