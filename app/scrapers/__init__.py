from .account_scraper import AccountScraper
from .excel_writer import ExcelWriter
from .planer_scraper import scrape_planner
from .ids_scrapers import BestOffersScraper, UrlIdsScraper


def scrape_account(username: str):
    scraper = AccountScraper(username)
    return ExcelWriter(username, scraper.categories, scraper.max_level)
