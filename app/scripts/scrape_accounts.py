from django.core.files import File

from app.models import Account, ScraperResult
from app.scrapers import scrape_account

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


# python manage.py shell < app/scripts.py scrape()
