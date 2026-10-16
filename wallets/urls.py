from django.urls import path
from .views import WalletDetailView

app_name=''

urlpatterns = [
    path('me/', WalletDetailView.as_view()),
]