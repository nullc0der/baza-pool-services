from rest_framework.routers import DefaultRouter

from tokendb import views

router = DefaultRouter()
router.register(r'', views.TokenViewSet, basename='token')

urlpatterns = router.urls
