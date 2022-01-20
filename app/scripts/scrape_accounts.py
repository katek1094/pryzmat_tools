import os

from django.core.files import File

from app.models import Account, ScraperResult
from app.scrapers import scrape_account


def scrape(username):
    excel_file = open(f'{username}.xlsx', 'wb')
    wb = scrape_account(username).wb
    wb.save(excel_file)
    excel_file.close()
    account = Account.objects.create(name=username)
    obj = ScraperResult(account=account)
    with open(f'{username}.xlsx', 'rb') as f:
        obj.file.save(f"{username}.xlsx", File(f), save=False)
        os.remove(f'{username}.xlsx')
    obj.save()

# python manage.py shell < app/scripts.py scrape()
