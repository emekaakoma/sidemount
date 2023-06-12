from django.contrib import admin
from django.conf.urls import include
from django.urls import path
from rest_framework import routers
from sidemountapi.views import register_user, login_user, BeltView, CommentView, EventView, SideMountUserView

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'belts', BeltView, 'belt')
router.register(r'comments', CommentView, 'comment')
router.register(r'events', EventView, 'event')
router.register(r'smusers', SideMountUserView, 'smuser')

urlpatterns = [
    path('register', register_user),
    path('login', login_user),
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
]
