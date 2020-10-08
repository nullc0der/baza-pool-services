from django.urls import path

from votingpayment import views

urlpatterns = [
    path('', views.VotingPaymentView.as_view()),
    path('<int:session_id>/<int:token_id>/',
         views.VotingPaymentAdminView.as_view()),
    path('address/', views.VotingPaymentAddress.as_view())
]
