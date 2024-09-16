from django.test import TestCase
from .models import Product, Category

class ProductModelTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name="Electronics")
        self.product = Product.objects.create(
            name="Test Product",
            price=1000,
            description="This is a test product",
            stock=10,
            category=self.category,
        )

    def test_product_creation(self):
        product = self.product
        self.assertEqual(product.name, "Test Product")
        self.assertEqual(product.price, 1000)
        self.assertEqual(product.description, "This is a test product")
        self.assertEqual(product.stock, 10)
        self.assertEqual(product.category.name, "Electronics")

    def test_product_string_representation(self):
        product = self.product
        self.assertEqual(str(product), "Test Product")

    def test_stock_default_value(self):
        new_product = Product.objects.create(
            name="New Product",
            price=500,
            description="This is another test product",
            category=self.category
        )
        self.assertEqual(new_product.stock, 0)

    def test_blank_and_null_category(self):
        with self.assertRaises(ValueError):
            Product.objects.create(
                name="Blank Category Product",
                price=1500,
                description="Product with blank category",
                stock=5,
                category=""
            )
