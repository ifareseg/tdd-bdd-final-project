# Copyright 2016, 2022 John J. Rofrano. All Rights Reserved.
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
Test factories for Products
"""

# pylint: disable=too-few-public-methods

import factory
from factory.fuzzy import FuzzyChoice, FuzzyDecimal

from service.models import Category, Product


class ProductFactory(factory.Factory):
    """Factory class for creating fake Product objects for tests."""

    class Meta:
        """Factory metadata."""
        model = Product

    id = factory.Sequence(lambda n: n)
    name = factory.Faker("word")
    description = factory.Faker("sentence")
    price = FuzzyDecimal(1.00, 1000.00, 2)
    available = FuzzyChoice([True, False])
    category = FuzzyChoice(list(Category))
