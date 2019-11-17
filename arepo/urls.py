from django.urls import path, include
from arepo.views import PanelView

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('panel/', PanelView.as_view(), name='panel'),
]