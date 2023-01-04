import pytest
from django.urls import reverse
from rest_framework.test import APIClient


@pytest.fixture
def client():
    return APIClient()


@pytest.mark.django_db
def test_user_list(client):
    # Arrange
    url = reverse('backend:user-list')
    # Act
    response = client.get(url)
    # Assert
    assert response.status_code == 200


@pytest.mark.django_db
def test_product_list(client):
    # Arrange
    url = reverse('backend:product-list')
    # Act
    response = client.get(url)
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 0
