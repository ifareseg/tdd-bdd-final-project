######################################################################
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
######################################################################

"""
Steps file for loading background data into the service
"""

import os
import requests
from behave import given
from service.common.status import HTTP_201_CREATED

BASE_URL = os.getenv("BASE_URL", "http://localhost:8080")
REST_ENDPOINT = f"{BASE_URL}/products"


@given("the following products")
def step_impl(context):
    """Delete all products and load products from the feature background table."""

    # Delete all existing products
    response = requests.get(REST_ENDPOINT)
    response.raise_for_status()

    for product in response.json():
        requests.delete(f"{REST_ENDPOINT}/{product['id']}").raise_for_status()

    # Load products from background table
    for row in context.table:
        payload = {
            "name": row["name"],
            "description": row["description"],
            "price": row["price"],
            "available": row["available"].strip().lower() == "true",
            "category": row["category"],
        }

        response = requests.post(REST_ENDPOINT, json=payload)
        assert response.status_code == HTTP_201_CREATED
