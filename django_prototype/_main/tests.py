from django.test import TestCase
from django.urls import reverse, resolve

# for webpages that do not have a model
from django.test import SimpleTestCase
from .views import PetalHomeView


# each test method must start with test_ to be recognized by the test suite.
class PetalHomeTests(SimpleTestCase):

    # helper method that will run before every test so we
    # don't have repeatedly define a response variable for each test
    def setUp(self):
        url = reverse('petalhome')
        self.response = self.client.get(url)


    def test_petalhome_status_code(self):
        """
        Check that the HTTP status code equals 200 which means that it exists.
        """
        self.assertEqual(self.response.status_code, 200)

    def test_petalhome_url_name(self):
        """
        Confirm the URL name of petalhome via the reverse method
        """
        self.assertEqual(self.response.status_code, 200)

    def test_petalhome_template(self):
        """
        Confirm that the correct template is being used
        """
        self.assertTemplateUsed(self.response, "petal_main/index.html")

    def test_petalhome_incorrect_html(self):
        """
        Confirm our homepage has the correct HTML code and does not have incorrect text
        """
        self.assertNotContains(self.response, "Hello, world!")

    def test_petalhome_resolves_url_to_view(self):
        """
        Checks that the name of the view used to resolve / matches PetalHomeView.
        """
        view = resolve('/')
        self.assertEqual(
            view.func.__name__,
            PetalHomeView.as_view().__name__
        )