import os

from django.core.files import File

from app.models import PlanerPhraseResult
from app.scrapers import scrape_planner


def scrape_phrase(phrase):
    print(phrase)
    print(1)
    excel_file = open(f'{phrase}.xlsx', 'wb')
    wb = scrape_planner(phrase)
    wb.save(excel_file)
    excel_file.close()
    obj = PlanerPhraseResult(phrase=phrase)
    print(2)
    with open(f'{phrase}.xlsx', 'rb') as f:
        obj.file.save(f'{phrase}.xlsx', File(f), save=False)
        os.remove(f'{phrase}.xlsx')
    obj.save()
    print(3)

# def scrape_phrase(phrase):
#     wb = scrape_planner(phrase)
#     virtual_workbook = BytesIO()
#     wb.save(virtual_workbook)
#     obj = PlanerPhraseResult(phrase=phrase)
#     virtual_workbook.seek(0)
#     obj.file.save(f'{phrase}.xlsx', ContentFile(virtual_workbook.read()), save=False)
#     obj.save()
