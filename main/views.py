from django.views.generic import ListView, DetailView

from django.shortcuts import get_object_or_404
from main.models import Category, SubCategory, Product


class CategoryListView(ListView):
    extra_context = {
        'title': 'Параллакс'
    }
    model = Category
    template_name = 'main/home.html'
    context_object_name = 'categories'


class ProductsBySubCategoryView(ListView):
    model = Product
    template_name = 'products_by_subcategory.html'
    context_object_name = 'products'

    def get_queryset(self):
        self.subcategory = get_object_or_404(SubCategory, id=self.kwargs['subcategory_id'])
        self.category = self.subcategory.category  # <-- добавили категорию
        return Product.objects.filter(subcategory=self.subcategory).order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subcategory'] = self.subcategory
        context['category'] = self.category  # <-- передаём категорию
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'  # новый шаблон
    context_object_name = 'product'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'


class SubCategoryListView(ListView):
    model = SubCategory
    template_name = 'subcategories_by_category.html'
    context_object_name = 'subcategories'

    def get_queryset(self):
        # получаем категорию, которую будем выводить через карточки
        self.category = get_object_or_404(Category, id=self.kwargs['category_id'])
        # Добавляем сортировку по нужному полю
        return SubCategory.objects.filter(category=self.category).order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context