from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),  # login, logout, password views
    path('accounts/', include('accounts.urls')),             # register, profile
    path('', include('store.urls')),
    path('api/products/', include('api_products.urls')),
    path('api/order/', include('api_order.urls')),
    path('api/cart/', include('cart.urls')),
    path('api/auth/', include('rest_framework.urls')),  # DRF login/logout views
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
