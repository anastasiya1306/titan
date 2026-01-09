from django.urls import path
from .views import CategoryListView, ProductsBySubCategoryView, ProductDetailView, SubCategoryListView
from .apps import MainConfig

app_name = MainConfig.name

urlpatterns = [
    path('', CategoryListView.as_view(), name='home'),
    path('catalog/<int:subcategory_id>/', ProductsBySubCategoryView.as_view(), name='products_by_subcategory'),
    path('product/<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('category/<int:category_id>/subcategories/', SubCategoryListView.as_view(), name='subcategories_by_category'),
]
