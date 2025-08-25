from django.shortcuts import render


def index(request):
	"""Basic landing page with a link to the login page."""
	return render(request, 'home/index.html')
