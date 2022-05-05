from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from core.views import CustomerViewSet, ProfessionViewSet, \
    DocumentViewSet, DataSheetViewSet

router = routers.DefaultRouter()
router.register(r'customers', CustomerViewSet, basename='customer')
router.register(r'professions', ProfessionViewSet)
router.register(r'documents', DocumentViewSet)
router.register(r'datasheets', DataSheetViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
]
