from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("core.urls")),
    path('category/', include("category.urls")),
    path('accounts/', include("accounts.urls")),
    path('store/', include("store.urls")),
    path('cart/', include("cart.urls")),
    path('orders/', include("order.urls")),
]

urlpatterns += static(settings.STATIC_URL, document_root = settings.STATICFILES_DIRS[0])
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
