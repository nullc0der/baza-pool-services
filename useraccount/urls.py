from django.urls import path

from knox.views import LogoutView

from useraccount.views import LoginView


urlpatterns = [
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view())
]
