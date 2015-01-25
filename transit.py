"""Show how much per month I'm spending on transit

Input: a transactions.csv file from from mint.com"""

import csv
import datetime
from calendar import month_abbr
from itertools import groupby

def is_transit(row):
    # The third column is the raw charge description
    lower = row[2].lower()
    return 'uber' in lower or 'lyft' in lower\
            or 'hertz' in lower or 'bart' in lower

def process_row(row):
    parts = map(int, row[0].split('/'))
    date = datetime.date(parts[2], parts[0], parts[1])
    return [date, row[1], row[2], float(row[3])]

transactions = []
with open('transactions.csv') as f:
    r = csv.reader(f)
    r.next() # skip column titles
    for row in r:
        if is_transit(row):
            transactions.append(process_row(row))

groupby_key = lambda t: '%s %d' % (month_abbr[t[0].month], t[0].year)
sorted_transactions = sorted(transactions, key=lambda t: t[0])
amounts = []
for k, g in groupby(sorted_transactions, groupby_key):
    amount = sum(t[3] for t in g)
    amounts.append(amount)
    print '%s: $%.2f\t%s' % (k, amount, '#'*int(amount/10))

average = 'Average: $%.2f' % (sum(amounts) * 1.0 / len(amounts))
print '-' * len(average)
print average
