from django.test import TestCase, Client
from django.urls import reverse
from recipes.models import Recipe
import importlib.util


class SearchFormTest(TestCase):
	def test_form_fields_and_help_text(self):
		from .forms import SearchForm
		form = SearchForm()
		self.assertIn('query', form.fields)
		self.assertIn('chart_type', form.fields)
		self.assertEqual(form.fields['query'].max_length, 100)
		self.assertIn('Enter recipe name', form.fields['query'].help_text)

	def test_valid_form_data(self):
		from .forms import SearchForm
		form = SearchForm(data={'query': 'tea', 'chart_type': 1})
		self.assertTrue(form.is_valid())

	def test_query_max_length_enforced(self):
		from .forms import SearchForm
		long_query = 'x' * 101
		form = SearchForm(data={'query': long_query, 'chart_type': 2})
		self.assertFalse(form.is_valid())
		self.assertIn('query', form.errors)


class SearchViewTest(TestCase):
	@classmethod
	def setUpTestData(cls):
		# Create a few recipes
		Recipe.objects.create(name='Tea', ingredients='water, tea leaves', cooking_time=5)
		Recipe.objects.create(name='Iced Tea', ingredients='water, tea, ice', cooking_time=7)
		Recipe.objects.create(name='Coffee', ingredients='water, coffee grounds', cooking_time=6)

	def setUp(self):
		self.client = Client()

	def test_get_renders_form(self):
		url = reverse('search:search')
		resp = self.client.get(url)
		self.assertEqual(resp.status_code, 200)
		self.assertIn('form', resp.context)
		# No results on initial GET
		self.assertIsNone(resp.context.get('recipes'))

	def test_post_filters_by_name_case_insensitive(self):
		url = reverse('search:search')
		resp = self.client.post(url, data={'query': 'tea', 'chart_type': 1})
		self.assertEqual(resp.status_code, 200)
		recipes = resp.context['recipes']
		names = [r.name for r in recipes]
		self.assertIn('Tea', names)
		self.assertIn('Iced Tea', names)
		self.assertNotIn('Coffee', names)

	def test_post_no_matches(self):
		url = reverse('search:search')
		resp = self.client.post(url, data={'query': 'nonexistent', 'chart_type': 1})
		self.assertEqual(resp.status_code, 200)
		self.assertQuerySetEqual(resp.context['recipes'], [])
		self.assertContains(resp, 'No matching recipes', status_code=200)

	def test_links_to_details_present(self):
		url = reverse('search:search')
		resp = self.client.post(url, data={'query': 'tea', 'chart_type': 2})
		self.assertEqual(resp.status_code, 200)
		# Each recipe should render a link using get_absolute_url
		for r in resp.context['recipes']:
			self.assertContains(resp, r.get_absolute_url(), html=False)

	def test_results_html_present_if_pandas_installed(self):
		pandas_installed = importlib.util.find_spec('pandas') is not None
		url = reverse('search:search')
		resp = self.client.post(url, data={'query': 'tea', 'chart_type': 3})
		if pandas_installed:
			# When pandas is available and results exist, results_html should be non-empty HTML
			results_html = resp.context.get('results_html')
			self.assertIsNotNone(results_html)
			self.assertIn('<table', results_html)
		else:
			# If pandas is not installed, view sets results_html to None
			self.assertIsNone(resp.context.get('results_html'))
