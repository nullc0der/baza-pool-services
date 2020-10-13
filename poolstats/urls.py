from django.urls import path
from poolstats import views


urlpatterns = [
    path('pools/', views.OwnedPoolsInfoView.as_view())
]
