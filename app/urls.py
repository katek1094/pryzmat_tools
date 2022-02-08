from django.urls import path

from . import views

url_patterns = [
    path('', views.home, name='home'),
    path('account_scraper', views.ScraperResultListView.as_view(), name='account_scraper'),
    path('planer_scraper', views.PlanerPhraseResultListView.as_view(), name='planer_scraper'),
    path('scrape_phrase', views.PhraseScrapeFormView.as_view(), name='scrape_phrase'),
    path('phrase_scraped', views.phrase_scraped, name='phrase_scraped'),
    path('ids_scraper', views.ids_scraper, name='ids_scraper'),
    path('print_ids', views.print_ids, name='print_ids'),
    path('get_accuracy_chart', views.get_accuracy_chart, name='get_accuracy_chart'),
    path('show_chart', views.show_chart, name='show_chart'),
]
