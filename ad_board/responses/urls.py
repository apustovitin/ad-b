from django.urls import path
from .views import ResponseAdd, ResponseDetail, ResponseSearch, response_accept, ResponseDelete

urlpatterns = [
    path('', ResponseSearch.as_view(),name='responses'),
    path('<int:pk>/', ResponseDetail.as_view(), name='response_detail'),
    path('<int:pk>/accept/', response_accept, name='response_accept'),
    path('<int:pk>/delete/', ResponseDelete.as_view(), name='response_delete'),
]