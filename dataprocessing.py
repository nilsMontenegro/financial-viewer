def _balance_for_month_and_year(transactions, month, year):
    current_transactions = [i for i in transactions
        if i["month"] == month and i["year"] == year]

    wins   = sum([i["sum"] for i in current_transactions if i["sum"] > 0])
    losses = sum([i["sum"] for i in current_transactions if i["sum"] < 0])

    return (wins, losses)

def _find_first_date(transactions):
    _all_dates = [(i["year"], i["month"]) for i in transactions]
    return min(_all_dates)

def _find_last_date(transactions):
    _all_dates = [(i["year"], i["month"]) for i in transactions]
    return max(_all_dates)

def _calc_all_dates(transactions):
    first_date = _find_first_date(transactions)
    last_date = _find_last_date(transactions)

    return [(year, month)
        for year in range(first_date[0], last_date[0] + 1)
        for month in range(1, 13)
        if (year, month) >= first_date and (year, month) <= last_date]


def calc_wins_losses_table(transactions):
    wins = []
    losses = []
    dates_str = []

    for (year, month) in _calc_all_dates(transactions):
        (current_wins, current_losses) = \
            _balance_for_month_and_year(transactions, month, year)
        wins.append(current_wins / 100)
        losses.append(abs(current_losses / 100))
        dates_str.append(str((year, month)))

    return wins, losses, dates_str
