import threading

from django.shortcuts import render
from django.views.generic.edit import FormView
from django.views.generic.list import ListView

from .forms import PhraseScrapeForm, BestOffersScraperForm, UrlIdsScraperForm, GetChartForm
from .models import ScraperResult, PlanerPhraseResult
from .scrapers import BestOffersScraper, UrlIdsScraper
from .scripts import scrape_phrase, get_chart_data


# Create your views here.
def home(request):
    return render(request, 'home.html')


class ScraperResultListView(ListView):
    model = ScraperResult
    template_name = 'account_scraper.html'

    def get_queryset(self):
        return self.model.objects.order_by('account__name', '-date')


class PlanerPhraseResultListView(ListView):
    model = PlanerPhraseResult
    template_name = 'planer_scraper.html'

    def get_queryset(self):
        return self.model.objects.order_by('-date')


class PhraseScrapeFormView(FormView):
    template_name = 'scrape_phrase.html'
    form_class = PhraseScrapeForm
    success_url = '/phrase_scraped'  # TODO: change later

    def form_valid(self, form):
        t = threading.Thread(target=scrape_phrase, args=(form.cleaned_data['phrase'],))
        t.setDaemon(True)
        t.start()
        return super().form_valid(form)


def phrase_scraped(request):
    return render(request, 'phrase_scraped.html')


def ids_scraper(request):
    best_offers_scraper_form = BestOffersScraperForm
    url_ids_scraper_form = UrlIdsScraperForm
    context = {
        'form1': best_offers_scraper_form,
        'form2': url_ids_scraper_form
    }
    return render(request, 'ids_scraper.html', context)


def print_ids(request):
    if request.method == 'POST':
        best_offers_scraper_form = BestOffersScraperForm(request.POST)
        url_ids_scraper_form = UrlIdsScraperForm(request.POST)
        if best_offers_scraper_form.is_valid():
            scraper = BestOffersScraper(**best_offers_scraper_form.cleaned_data)
            ids = str(scraper.ids)[1:-1]
            return render(request, 'print_ids.html', {'ids': ids})
        elif url_ids_scraper_form.is_valid():
            scraper = UrlIdsScraper(**url_ids_scraper_form.cleaned_data)
            ids = str(scraper.ids)[1:-1]
            return render(request, 'print_ids.html', {'ids': ids})
    return render(request, 'phrase_scraped.html')




def get_accuracy_chart(request):
    return render(request, 'get_chart.html', {'form': GetChartForm})


def show_chart(request):
    if request.POST:
        username = request.POST.get('username')
        time_range = request.POST.get('time_range')
        data = get_chart_data(username, time_range)
        if all(v == 0 for v in data[1]):
            return render(request, 'wrong_username.html')
        return render(request, 'chart.html', {'data': data, 'username': username})
