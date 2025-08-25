from django import forms

CHART_CHOICES = (
    (1, 'Bar Chart'),
    (2, 'Line Chart'),
    (3, 'Pie Chart')
)

class SearchForm(forms.Form):
    query = forms.CharField(max_length=100, help_text="Enter recipe name")
    # chart_type = forms.ChoiceField(choices=CHART_CHOICES)