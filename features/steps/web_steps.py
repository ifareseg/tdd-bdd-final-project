######################################################################
# Copyright 2016, 2021 John J. Rofrano. All Rights Reserved.
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

# pylint: disable=function-redefined, missing-function-docstring
# flake8: noqa
"""
Web Steps

Steps file for web interactions with Selenium

For information on Waiting until elements are present in the HTML see:
    https://selenium-python.readthedocs.io/waits.html
"""
"""
Web steps for Product Admin UI
"""

import os
from behave import when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = os.getenv("BASE_URL", "http://localhost:8080")

COPIED = {}


def _id_for_field(field_name: str) -> str:
    mapping = {
        "Id": "product_id",
        "Name": "product_name",
        "Description": "product_description",
        "Price": "product_price",
        "Available": "product_available",
        "Category": "product_category",
    }
    return mapping[field_name]


def _id_for_button(button_name: str) -> str:
    mapping = {
        "Create": "create-btn",
        "Retrieve": "retrieve-btn",
        "Update": "update-btn",
        "Delete": "delete-btn",
        "Clear": "clear-btn",
        "Search": "search-btn",
    }
    return mapping[button_name]


@when('I visit the "Home Page"')
def step_visit_home(context):
    """Open the home page."""
    context.driver.get(BASE_URL)


@then('I should see "{text}" in the title')
def step_title_contains(context, text):
    """Assert page title contains text."""
    assert text in context.driver.title


@then('I should not see "{text}"')
def step_not_see_text(context, text):
    """Assert text is not present in the page source."""
    assert text not in context.driver.page_source


@when('I set the "{field}" to "{value}"')
def step_set_field(context, field, value):
    """Set text field value."""
    element = context.driver.find_element(By.ID, _id_for_field(field))
    element.clear()
    element.send_keys(value)


@when('I select "{value}" in the "{field}" dropdown')
def step_select_dropdown(context, value, field):
    """Select a dropdown value by visible text (fallback to value)."""
    select = Select(context.driver.find_element(By.ID, _id_for_field(field)))
    try:
        select.select_by_visible_text(value)
    except Exception:
        select.select_by_value(value)


@when('I press the "{button}" button')
def step_press_button(context, button):
    """Press a UI button."""
    context.driver.find_element(By.ID, _id_for_button(button)).click()


@then('I should see the message "{message}"')
def step_see_message(context, message):
    """Check flash message contains text."""
    element = WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.ID, "flash_message"))
    )
    assert message in element.text


@when('I copy the "{field}" field')
def step_copy_field(context, field):
    """Copy field value."""
    element = context.driver.find_element(By.ID, _id_for_field(field))
    COPIED[field] = element.get_attribute("value")


@when('I paste the "{field}" field')
def step_paste_field(context, field):
    """Paste previously copied value into field."""
    element = context.driver.find_element(By.ID, _id_for_field(field))
    element.clear()
    element.send_keys(COPIED.get(field, ""))


@then('the "{field}" field should be empty')
def step_field_empty(context, field):
    """Assert field is empty."""
    element = context.driver.find_element(By.ID, _id_for_field(field))
    assert element.get_attribute("value") == ""


@then('I should see "{value}" in the "{field}" field')
def step_see_field_value(context, value, field):
    """Assert exact field value."""
    element = context.driver.find_element(By.ID, _id_for_field(field))
    assert element.get_attribute("value") == value


@then('I should see "{value}" in the "{field}" dropdown')
def step_see_dropdown_value(context, value, field):
    """Assert dropdown selected option text."""
    select = Select(context.driver.find_element(By.ID, _id_for_field(field)))
    assert select.first_selected_option.text == value
