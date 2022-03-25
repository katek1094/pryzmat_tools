import datetime
import os
from collections import namedtuple
from statistics import mean

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv


def create_session():
    return requests.Session()


def login(s: requests.Session):
    load_dotenv()

    password = os.getenv('NIEZBEDNIK_PASSWORD')

    s.headers.update({'referer': 'https://niezbedniksprzedawcy.pl/accounts/login/'})

    soup = BeautifulSoup(s.get('https://niezbedniksprzedawcy.pl/accounts/login/').content, 'html5lib')
    csrftoken = soup.find('input', dict(name='csrfmiddlewaretoken'))['value']

    r = s.post('https://niezbedniksprzedawcy.pl/accounts/login/', {
        'csrfmiddlewaretoken': csrftoken,
        'login': 'info@pryzmat.media',
        'password': password
    })

    if r.status_code != 200:
        raise Exception('CAN NOT LOGIN INTO NIEZBEDNIK SPRZEDAWCY')


def get_account_raw_data(s: requests.Session, account_name: str, time_range: str):
    api_url = 'https://niezbedniksprzedawcy.pl/StatystykiAllegro/get_offers_stats?format=json'
    params = {'q': account_name,
              'p': 1,  # pagination control
              'l': 600,  # amount of data on one page
              'f': time_range,  # time range of data requested
              'offerPositionLimit': 600}  # minimum position in accuracy ranking for offer to show; max=600
    r = s.get(api_url, params=params)
    return r.json()


"""
return value structure:
{
    limit: int, the same value as in request
    pages: int, how many pages there are to see
    offset: int, number of page returned
    offers: data about offers, nested deeper
    series: [
        {
            name: offer id
            data: data for 30 days (array) : [
                [
                    timestamp - in miliseconds,
                    value - offer position in accuracy
                ]
            ]
        }
    ]

}
"""

Record = namedtuple('Record', 'date value')
OfferData = namedtuple('OfferData', 'id_number records')


def create_record(record):
    timestamp_in_ms, position = record
    record_date = datetime.datetime.fromtimestamp(timestamp_in_ms / 1000).date()
    return Record(record_date, position)


def format_account_data(data):
    formatted_data = []
    for offer in data['series']:
        records = []
        for record in offer['data']:
            records.append(create_record(record))
        formatted_data.append(OfferData(offer['name'], tuple(records)))

    return formatted_data


def generate_columns_for_dates_dict(time_range: str, skip=1):
    result = {}
    start_date = datetime.date.today()
    if time_range == '1M':
        day_count = 30
    elif time_range == '2M':
        day_count = 60
    elif time_range == '3M':
        day_count = 90
    else:
        raise ValueError('time range wrong value')
    for index, date in enumerate(start_date - datetime.timedelta(day_count - n) for n in range(day_count)[0::skip]):
        result[date] = index + 2
    return result


class Range:
    def __init__(self, floor: int, ceiling: int, points):
        if floor > ceiling:
            raise ValueError('floor value can not be greater than ceiling value!')
        else:
            self.floor = floor
            self.ceiling = ceiling
            self.points = points

    def check_if_value_in_range(self, value):
        return self.ceiling > value >= self.floor

    def __repr__(self):
        return f'{self.floor} - {self.ceiling}'


ranges = [
    (1, 1, 14),
    (2, 3, 8),
    (4, 5, 5),
    (6, 8, 3.5),
    (9, 12, 2.5),
    (13, 20, 2),
    (21, 40, 1),
    (41, 60, 0.8),
    (61, 120, 0.4),
    (121, 180, 0.2),
    (181, 600, 0.1)
]

range_objects = []

for rng in ranges:
    range_objects.append(Range(*rng))


def get_point_for_day_data(arr):
    points = 0
    for dt in arr:
        for range_obj in range_objects:
            if range_obj.check_if_value_in_range(dt):
                points += range_obj.points
    return round(points, 2)


"""
data format for table:
3-dniowe okresy -> dict of ranges -> average amount of offers in this day in this range
"""


def generate_table_data_for_days(days):
    results = []
    amount_of_periods = int(len(days) / 6)
    for period_index in range(amount_of_periods):
        period_days = days[period_index * 6:(period_index * 6) + 6]
        range_counters = []
        for _ in range(len(ranges)):
            range_counters.append(0)
        # print(range_counters)
        not_empty_counter = 0
        for period_day in period_days:
            if len(period_day):
                not_empty_counter += 1
            for index, range_obj in enumerate(range_objects):
                for val in period_day:
                    # print(val)
                    # print(range_obj)
                    if range_obj.check_if_value_in_range(val):
                        # print(range_counters[index])
                        range_counters[index] += 1
                    # else:
                        # print('DUPA')
        for index, rng_counter in enumerate(range_counters):
            if not_empty_counter:
                range_counters[index] = round(rng_counter / not_empty_counter, 1)
        results.append(range_counters)

    return results, range_objects


def create_chart_data(data: [OfferData], username: str, time_range):
    # # WRITE DATES
    # for date, column in columns_for_dates.items():
    #     ws.cell(row=1, column=column).value = date.strftime('%d-%m')
    #
    # # WRITE DATA
    # row = 2
    # for offer_data in data:
    #     ws.cell(row=row, column=1).value = offer_data.id_number
    #     for record in offer_data.records:
    #         ws.cell(row=row, column=columns_for_dates[record.date]).value = record.value
    #     row += 1
    #
    # reformat data into days of records
    if time_range == '1M':
        day_count = 30
    elif time_range == '2M':
        day_count = 60
    elif time_range == '3M':
        day_count = 90
    else:
        raise ValueError('time range wrong value')
    days = []
    for _ in range(day_count):
        days.append([])
    for offer_data in data:
        for index, record in enumerate(offer_data.records):
            if index == 0 and time_range == '3M' or index == 0 and time_range == '2M':
                continue
            days[generate_columns_for_dates_dict(time_range)[record.date] - 2].append(record.value)

    points = []
    table_data = generate_table_data_for_days(days)

    for day in days:
        points.append(get_point_for_day_data(day))

    # for date, column in columns_for_dates.items():
    #     ws.cell(row=1, column=column).value = date.strftime('%d-%m')
    # for col, point in enumerate(points):
    #     ws.cell(row=2, column=col + 2).value = point

    dates = []
    for date in generate_columns_for_dates_dict(time_range, 3).keys():
        dates.append(date.strftime('%d-%m'))

    avg_points = []
    for x in range(int(day_count / 3)):
        # print(x)
        # print(x * 3, x * 3 + 2)
        avg_points.append(round(mean(points[x * 3:x * 3 + 2]), 2))

    return dates, avg_points, table_data


def create_account_stats_report(s, account_name, time_range):
    raw_data = get_account_raw_data(s, account_name, time_range)
    results = format_account_data(raw_data)
    return create_chart_data(results, account_name, time_range)


def get_chart_data(username, time_range):
    session = create_session()
    login(session)

    return create_account_stats_report(session, username, time_range)
