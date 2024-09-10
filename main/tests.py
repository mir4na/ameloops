from django.test import TestCase
from .models import Product

class ProductModelTest(TestCase):

    def setUp(self):
        # This method will run before each test
        self.product = Product.objects.create(
            name="Test Product",
            price=1000,
            description="This is a test product",
            stock=10,
            category="Electronics",
        )

    def test_product_creation(self):
        # Test if the product is created correctly
        product = self.product
        self.assertEqual(product.name, "Test Product")
        self.assertEqual(product.price, 1000)
        self.assertEqual(product.description, "This is a test product")
        self.assertEqual(product.stock, 10)
        self.assertEqual(product.category, "Electronics")

    def test_product_string_representation(self):
        # Test the string representation of the product
        product = self.product
        self.assertEqual(str(product), "Test Product")

    def test_stock_default_value(self):
        # Test that the default stock value is set to 0
        new_product = Product.objects.create(
            name="New Product",
            price=500,
            description="This is another test product",
        )
        self.assertEqual(new_product.stock, 0)

    def test_blank_and_null_category(self):
        # Test that a product can have a blank or null category
        product_with_blank_category = Product.objects.create(
            name="Blank Category Product",
            price=1500,
            description="Product with blank category",
            stock=5,
            category=""
        )
        product_with_null_category = Product.objects.create(
            name="Null Category Product",
            price=2000,
            description="Product with null category",
            stock=5,
            category=None
        )
        self.assertEqual(product_with_blank_category.category, "")
        self.assertIsNone(product_with_null_category.category)
