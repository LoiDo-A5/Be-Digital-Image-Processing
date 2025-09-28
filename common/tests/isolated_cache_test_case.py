from django.contrib.sites.models import SITE_CACHE
from rest_framework.test import APITestCase as RestAPITestCase


class APITestCase(RestAPITestCase):
    def setUp(self) -> None:
        super().setUp()
        SITE_CACHE.clear()

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
