from django.urls import path
from .views import AdsList, AdAdd, AdDetail, AdUpdate, AdDelete
from responses.views import ResponseAdd

urlpatterns = [
    path('', AdsList.as_view(),name='ads'),
    path('add/', AdAdd.as_view(), name='ad_add'),
    path('<int:pk>/', AdDetail.as_view(), name='ad_detail'),
    path('<int:pk>/edit/', AdUpdate.as_view(), name='ad_update'),
    path('<int:pk>/delete/', AdDelete.as_view(), name='ad_delete'),
    path('<int:pk>/response_add', ResponseAdd.as_view(), name='response_add'),
]