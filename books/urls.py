from django.urls import include, path
from rest_framework import routers
from books import views
from . import views


router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'books', views.BookViewSet)

urlpatterns = [
    path('sample', views.index, name='index'),
    path('sample/<int:book_id>/', views.detail, name='detail'),
    path('sample/<int:book_id>/forms',views.formfunc,name='forms'),

    path('root/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    path('',views.Login,name='Login'),
    path("logout",views.Logout,name="Logout"),
    path("home",views.home,name="home"),

]

