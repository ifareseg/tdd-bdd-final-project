# Copyright 2016, 2023 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Test cases for Product Model
"""

import os
import logging
import unittest

from service import app
from service.models import Product, Category, DataValidationError, db
from tests.factories import ProductFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql://postgres:postgres@localhost:5432/postgres"
)


######################################################################
#  P R O D U C T   M O D E L   T E S T   C A S E S
######################################################################


class TestProductModel(unittest.TestCase):
    """Test Cases for Product Model"""

    @classmethod
    def setUpClass(cls):
        """Set up the test environment once for this test suite."""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        Product.init_db(app)

    @classmethod
    def tearDownClass(cls):
        """Tear down the test environment once after the test suite."""
        db.session.close()

    def setUp(self):
        """Clean the database before each test."""
        db.session.query(Product).delete()
        db.session.commit()

    def tearDown(self):
        """Remove the session after each test."""
        db.session.remove()

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_create_a_product(self):
        """It should create a Product instance."""
        product = Product(
            name="Fedora",
            description="A red hat",
            price=12.50,
            available=True,
            category=Category.CLOTHS,
        )
        self.assertEqual(str(product), "<Product Fedora id=[None]>")
        self.assertEqual(product.id, None)
        self.assertEqual(product.name, "Fedora")
        self.assertEqual(product.description, "A red hat")
        self.assertEqual(product.available, True)
        self.assertEqual(product.price, 12.50)
        self.assertEqual(product.category, Category.CLOTHS)

    def test_add_a_product(self):
        """It should add a Product to the database."""
        self.assertEqual(Product.all(), [])

        product = ProductFactory()
        product.id = None
        product.create()

        self.assertIsNotNone(product.id)
        self.assertEqual(len(Product.all()), 1)

    def test_read_a_product(self):
        """It should read a Product from the database."""
        product = ProductFactory()
        product.id = None
        product.create()

        found = Product.find(product.id)
        self.assertIsNotNone(found)
        self.assertEqual(found.id, product.id)

    def test_update_a_product(self):
        """It should update a Product in the database."""
        product = ProductFactory()
        product.id = None
        product.create()

        product.description = "UPDATED"
        product.update()

        found = Product.find(product.id)
        self.assertEqual(found.description, "UPDATED")

    def test_update_no_id(self):
        """It should not update a Product without an id."""
        product = ProductFactory()
        product.id = None
        with self.assertRaises(DataValidationError):
            product.update()

    def test_delete_a_product(self):
        """It should delete a Product from the database."""
        product = ProductFactory()
        product.id = None
        product.create()

        self.assertEqual(len(Product.all()), 1)
        product.delete()
        self.assertEqual(len(Product.all()), 0)

    def test_list_all_products(self):
        """It should list all Products."""
        self.assertEqual(Product.all(), [])

        for _ in range(5):
            product = ProductFactory()
            product.id = None
            product.create()

        self.assertEqual(len(Product.all()), 5)

    def test_find_by_name(self):
        """It should find Products by name."""
        products = ProductFactory.create_batch(5)
        for prod in products:
            prod.id = None
            prod.create()

        name = products[0].name
        found = Product.find_by_name(name)
        self.assertGreaterEqual(found.count(), 1)

    def test_find_by_category(self):
        """It should find Products by category."""
        products = ProductFactory.create_batch(5)
        for prod in products:
            prod.id = None
            prod.create()

        category = products[0].category
        found = Product.find_by_category(category)
        self.assertGreaterEqual(found.count(), 1)

    def test_find_by_availability(self):
        """It should find Products by availability."""
        products = ProductFactory.create_batch(5)
        for prod in products:
            prod.id = None
            prod.create()

        available = products[0].available
        found = Product.find_by_availability(available)
        self.assertGreaterEqual(found.count(), 1)

    def test_find_by_price_string(self):
        """It should find Products by price passed as a string."""
        products = ProductFactory.create_batch(5)
        for prod in products:
            prod.id = None
            prod.create()

        price_str = str(products[0].price)
        found = Product.find_by_price(price_str)
        self.assertGreaterEqual(found.count(), 1)

    def test_deserialize_missing_data(self):
        """It should not deserialize with missing required fields."""
        product = Product()
        with self.assertRaises(DataValidationError):
            product.deserialize({"name": "Hat"})

    def test_deserialize_bad_available_type(self):
        """It should not deserialize when available is not a boolean."""
        product = Product()
        data = {
            "name": "Hat",
            "description": "A red fedora",
            "price": "59.95",
            "available": "yes",
            "category": "CLOTHS",
        }
        with self.assertRaises(DataValidationError):
            product.deserialize(data)

    def test_deserialize_bad_category(self):
        """It should not deserialize with an invalid category."""
        product = Product()
        data = {
            "name": "Hat",
            "description": "A red fedora",
            "price": "59.95",
            "available": True,
            "category": "NOT_A_CATEGORY",
        }
        with self.assertRaises(DataValidationError):
            product.deserialize(data)
