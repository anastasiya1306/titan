import pytest
from django.urls import reverse
from main.models import Category, SubCategory, Product


@pytest.fixture
def setup_data(db):
    category = Category.objects.create(name="Электроника")
    subcategory = SubCategory.objects.create(name="Смартфоны", category=category)
    product = Product.objects.create(name="iPhone 15", subcategory=subcategory, price=1000)
    return {
        "category": category,
        "subcategory": subcategory,
        "product": product,
    }


def test_category_list_view(client, setup_data):
    url = reverse("main:home")
    response = client.get(url)
    assert response.status_code == 200
    assert "categories" in response.context
    assert response.context["title"] == "Главная"
    assert "main/home.html" in [t.name for t in response.templates]


def test_subcategory_list_view(client, setup_data):
    url = reverse("main:subcategories_by_category", args=[setup_data["category"].id])
    response = client.get(url)
    assert response.status_code == 200
    assert "subcategories_by_category.html" in [t.name for t in response.templates]
    assert "category" in response.context
    assert "Смартфоны" in response.content.decode()


def test_products_by_subcategory_view(client, setup_data):
    url = reverse("main:products_by_subcategory", args=[setup_data["subcategory"].id])
    response = client.get(url)
    assert response.status_code == 200
    assert "products_by_subcategory.html" in [t.name for t in response.templates]
    assert "subcategory" in response.context
    assert "category" in response.context
    assert "iPhone 15" in response.content.decode()


def test_product_detail_view(client, setup_data):
    url = reverse("main:product_detail", args=[setup_data["product"].id])
    response = client.get(url)
    assert response.status_code == 200
    assert "product_detail.html" in [t.name for t in response.templates]
    assert "product" in response.context
    assert "iPhone 15" in response.content.decode()


@pytest.mark.django_db
def test_404_for_nonexistent_category(client):
    url = reverse("main:subcategories_by_category", args=[999])
    response = client.get(url)
    assert response.status_code == 404


@pytest.mark.django_db
def test_404_for_nonexistent_subcategory(client):
    url = reverse("main:products_by_subcategory", args=[999])
    response = client.get(url)
    assert response.status_code == 404
