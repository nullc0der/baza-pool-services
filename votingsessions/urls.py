from rest_framework.routers import DefaultRouter

from votingsessions import views

router = DefaultRouter()
router.register(r'', views.VotingSessionViewSet, basename='voting_session')

urlpatterns = router.urls
