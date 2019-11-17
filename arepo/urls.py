from django.urls import path, include
from arepo.views import PanelView, HomePageView, StatView, WaiterView

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('', HomePageView.as_view(), name='home'),
    path('panel/', PanelView.as_view(), name='panel'),
    path('stats/', StatView.as_view(), name='stats'),
    path('waiter/', WaiterView.as_view(), name='waiter'),

]
