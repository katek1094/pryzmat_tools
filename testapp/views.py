import threading
import time

from django.http import HttpResponse

from .models import Account


def scrape_phrase(phrase):
    time.sleep(30)
    Account(name=phrase).save()
    print('saved')


def testview(request):
    args = ('makrama', )
    t = threading.Thread(target=scrape_phrase, args=args)
    t.setDaemon(True)
    t.start()

    return HttpResponse()
