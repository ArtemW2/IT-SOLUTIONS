from django.urls import path, include

from rest_framework import routers

from .viewset import CategoryViewSet, SubCategoryViewSet, StatusViewSet, TypeViewSet, TransactionViewSet
from .views import (
    reference,
    StatusCreateView, StatusUpdateView, StatusDeleteView,
    TypeCreateView, TypeUpdateView, TypeDeleteView,
    CategoryCreateView, CategoryUpdateView, CategoryDeleteView,
    get_subcategories, SubCategoryCreateView, SubCategoryUpdateView, SubCategoryDeleteView,
    TransactionListView, TransactionCreateView, TransactionUpdateView, TransactionDeleteView,
)

app_name = 'transaction'

router = routers.DefaultRouter()
router.register(r'categories', CategoryViewSet, basename = 'categories')
router.register(r'subcategories', SubCategoryViewSet, basename = 'subcategories')
router.register(r'statuses', StatusViewSet, basename = 'statuses')
router.register(r'types', TypeViewSet, basename = 'types')
router.register(r'transactions', TransactionViewSet, basename = 'transactions')

urlpatterns = [
    # path('', include(router.urls)),


    path('reference/', reference, name='reference'),

    path('categories/create/', CategoryCreateView.as_view(), name = 'category_create'),
    path('categories/<int:pk>/update/', CategoryUpdateView.as_view(), name = 'category_update'),
    path('categories/<int:pk>/delete/', CategoryDeleteView.as_view(), name = 'category_delete'),

    path('get_subcategories/', get_subcategories, name='get_subcategories'),
    path('subcategories/create/', SubCategoryCreateView.as_view(), name = 'subcategory_create'),
    path('subcategories/<int:pk>/update/', SubCategoryUpdateView.as_view(), name = 'subcategory_update'),
    path('subcategories/<int:pk>/delete/', SubCategoryDeleteView.as_view(), name = 'subcategory_delete'),

    path('statuses/create/', StatusCreateView.as_view(), name = 'status_create'),
    path('statuses/<int:pk>/update/', StatusUpdateView.as_view(), name = 'status_update'),
    path('statuses/<int:pk>/delete/', StatusDeleteView.as_view(), name = 'status_delete'),

    path('types/create/', TypeCreateView.as_view(), name = 'type_create'),
    path('types/<int:pk>/update/', TypeUpdateView.as_view(), name = 'type_update'),
    path('types/<int:pk>/delete/', TypeDeleteView.as_view(), name = 'type_delete'),
    
    path('', TransactionListView.as_view(), name = 'transaction_list'),
    path('transactions/create/', TransactionCreateView.as_view(), name = 'transaction_create'),
    path('transactions/<int:pk>/update/', TransactionUpdateView.as_view(), name = 'transaction_update'),
    path('transactions/<int:pk>/delete/', TransactionDeleteView.as_view(), name = 'transaction_delete'),
]


