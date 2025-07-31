# config.py
# filename: config.py
# date: 2025-07-31 17:17:59
# Configuration file for date formats and quarter definitions
DATE_FORMATS = [
    '%Y-%m-%d',
    '%m/%d/%Y',
    '%d/%m/%Y',
    '%Y/%m/%d',
    '%d-%m-%Y',
    '%m-%d-%Y'
]

QUARTER_DEFINITIONS = {
    'Q1': {'start': '01-01', 'end': '03-31'},
    'Q2': {'start': '04-01', 'end': '06-30'},
    'Q3': {'start': '07-01', 'end': '09-30'},
    'Q4': {'start': '10-01', 'end': '12-31'}
}