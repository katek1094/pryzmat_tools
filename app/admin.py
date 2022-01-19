from django.contrib import admin

from .models import Account, PlanerPhraseResult, ScraperResult

admin.site.register(Account)
admin.site.register(PlanerPhraseResult)
admin.site.register(ScraperResult)
