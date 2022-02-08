from django import forms


class PhraseScrapeForm(forms.Form):
    phrase = forms.CharField()


class GetChartForm(forms.Form):
    username = forms.CharField()


class BestOffersScraperForm(forms.Form):
    username = forms.CharField()
    MODES = (('accuracy', 'trafność'), ('popularity', 'popularność'),)
    mode = forms.ChoiceField(choices=MODES)
    target_amount = forms.IntegerField()


class UrlIdsScraperForm(forms.Form):
    url = forms.URLField()
    target_amount = forms.IntegerField()
