from django.urls import path

from rest_framework.routers import DefaultRouter

from votingsessions import views

urlpatterns = [
    path('current/', views.CurrentVotingSessionView.as_view())
]


router = DefaultRouter()
router.register(r'', views.VotingSessionViewSet, basename='voting_session')

urlpatterns += router.urls
