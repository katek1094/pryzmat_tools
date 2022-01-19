from django.db import models


class Account(models.Model):
    name = models.CharField(max_length=60)

    def __str__(self):
        return self.name


def scraper_result_path(instance, filename):
    return '/scraper_results/' + instance.account.name + '/' + filename


class ScraperResult(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to=scraper_result_path)

    def __str__(self):
        return f'{self.account.name} - {self.date}'


def planer_phrase_result_path(_, filename):
    return '/scraper_results/' + filename


class PlanerPhraseResult(models.Model):
    phrase = models.CharField(max_length=100)
    file = models.FileField(upload_to=planer_phrase_result_path)

    def __str__(self):
        return self.phrase
