from django import forms


class PhraseScrapeForm(forms.Form):
    phrase = forms.CharField()


class GetChartForm(forms.Form):
    username = forms.CharField()
    CHOICES = [
        ('1M', '1 miesiąc'),
        ('2M', '2 miesiące'),
        ('3M', '3 miesiące'),
    ]
    time_range = forms.ChoiceField(choices=CHOICES)


class BestOffersScraperForm(forms.Form):
    username = forms.CharField()
    MODES = (('accuracy', 'trafność'), ('popularity', 'popularność'),)
    mode = forms.ChoiceField(choices=MODES)
    target_amount = forms.IntegerField()


class UrlIdsScraperForm(forms.Form):
    url = forms.URLField()
    target_amount = forms.IntegerField()


class MacroGeneratorForm(forms.Form):
    file = forms.FileField(widget=forms.widgets.FileInput(attrs={'accept': '.xlsx'}))
