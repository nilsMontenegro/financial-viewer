################## SAVING  DATA ############################
_transaction_database_current = []

# For ctrl z:
_transaction_database_index = -1
_transaction_database_steps = []

def update_transaction_database(new_transactions):
    global _transaction_database_current
    _transaction_database_current += new_transactions

def get_transaction_database():
    global _transaction_database_current
    return _transaction_database_current

################## PARSING DATA ############################
import csv

def parse_german_camt(transaction):
    sum_value = transaction["Betrag"]
    sum_value = sum_value.split(",")
    sum_value = int(sum_value[0]) * 100 + int(sum_value[1])

    category = 0

    date = transaction["Buchungstag"]
    date = date.split(".")

    day = int(date[0])
    month = int(date[1])
    year = int(date[2])

    if year < 100:
          year += 2000

    return {
        "day": day, "month": month, "year": year,
        "sum": sum_value, "category": category
    }

'''
Future Idea:
def parse(format, transaction):
  bla bla

german_camt = {"decimalDelimiter":",",
              "sum": "Betrag",
              "date": "Buchungstag",
              "dateFormat": "dd.mm.yy"}

parse(german_camt, i)
'''

def parse_csv_string(csv_string):
    myreader = csv.DictReader(csv_string.splitlines(), delimiter = ";")

    new_transactions = []
    for i in myreader:
        new_transactions.append(parse_german_camt(i))

    return new_transactions

