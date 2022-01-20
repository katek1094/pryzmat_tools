from django.core.files import File

from app.models import Account, ScraperResult, PlanerPhraseResult
from app.scrapers import scrape_account
from app.scrapers import scrape_planner


def scrape():
    accounts = ['animalsdog']

    excel_file = open('private.xlsx', 'wb')
    wb = scrape_account(accounts[0]).wb
    wb.save(excel_file)
    excel_file.close()
    account = Account.objects.create(name=accounts[0])
    obj = ScraperResult(account=account)
    with open('private.xlsx', 'rb') as f:
        obj.file.save(f"{accounts[0]}.xlsx", File(f), save=False)
    obj.save()


def scrape_phrase(phrase):
    excel_file = open(f'{phrase}.xlsx', 'wb')
    wb = scrape_planner(phrase)
    wb.save(excel_file)
    excel_file.close()
    obj = PlanerPhraseResult(phrase=phrase)
    with open(f'{phrase}.xlsx', 'rb') as f:
        obj.file.save(f'{phrase}.xlsx', File(f), save=False)
    obj.save()

# python manage.py shell < app/scripts.py
