from django.urls import path, include
from arepo.views import PanelView, HomePageView, StatView, OrderDetailView, \
    OrderEditView, OrderNewView, OrderListView, OrderCloseView

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('', HomePageView.as_view(), name='home'),
    path('panel/', PanelView.as_view(), name='panel'),
    path('stats/', StatView.as_view(), name='stats'),
    path('waiter/', OrderListView.as_view(), name='waiter'),
    path('waiter/order/new', OrderNewView.as_view(), name='order_new'),
    path('waiter/order/<int:pk>', OrderDetailView.as_view(), name='order_detail'),
    path('waiter/order/<int:pk>/edit', OrderEditView.as_view(), name='order_edit'),
    path('waiter/order/<int:pk>/close', OrderCloseView.as_view(), name='order_close'),
]
