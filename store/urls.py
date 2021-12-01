from django.urls import path
from rest_framework import routers
from . import views
from pprint import pprint

# give parameter to a path using <> example: 'product/<id>/'
# Default Router additional features: Api root and json file

router = routers.DefaultRouter()
router.register('products', views.ProductViewSet)
router.register('collections', views.CollectionViewSet)

urlpatterns = router.urls
