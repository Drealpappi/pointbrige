from django.urls import path
from .views import ClaimPointsView

urlpatterns =[
    path('', ClaimPointsView.as_view())
]