from django.urls import path, include

urlpatterns = [
    path('useraccount/', include('useraccount.urls')),
    path('tokendb/', include('tokendb.urls')),
    path('votingsession/', include('votingsessions.urls')),
    path('votingpayment/', include('votingpayment.urls'))
]
