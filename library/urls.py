from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(prefix='libraries', viewset=views.LibraryViewSet, basename='library')
router.register(prefix='authors', viewset=views.AuthorViewSet, basename='author')
router.register(prefix='books', viewset=views.BookViewSet, basename='book')
router.register(prefix='transactions', viewset=views.TransactionsViewSet, basename='transactions')

urlpatterns = [
    path('', include(router.urls)),
]
