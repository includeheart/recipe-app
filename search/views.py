from django.shortcuts import render
from .forms import SearchForm
from recipes.models import Recipe


def search_view(request):
    """Search recipes by name, show results in a table with links, and build a pandas DataFrame."""
    form = SearchForm(request.POST or None)
    recipes = None
    results_html = None
    query = None

    if request.method == 'POST' and form.is_valid():
        query = form.cleaned_data['query']
        chart_type = form.cleaned_data['chart_type']

        qs = Recipe.objects.filter(name__icontains=query).order_by('name')
        recipes = qs

        try:
            import pandas as pd
            df = pd.DataFrame(list(qs.values('id', 'name', 'ingredients', 'cooking_time', 'difficulty')))
            if not df.empty:
                df.rename(columns={
                    'id': 'ID',
                    'name': 'Name',
                    'ingredients': 'Ingredients',
                    'cooking_time': 'Cooking Time (min)',
                    'difficulty': 'Difficulty',
                }, inplace=True)
                results_html = df.to_html(index=False, classes='table', border=0, escape=True)
        except Exception:
            results_html = None

    context = {
        'form': form,
        'recipes': recipes,
        'results_html': results_html,
        'query': query,
    }
    return render(request, 'search/search.html', context)