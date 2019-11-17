from django.urls import path, include
from arepo.views import PanelView, HomePageView

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('', HomePageView.as_view(), name='home'),
    path('panel/', PanelView.as_view(), name='panel'),
]
