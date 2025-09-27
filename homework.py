import datetime as dt


class Record:
    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        return sum(record.amount for record in self.records
                   if record.date == dt.date.today())

    def get_week_stats(self):
        today = dt.date.today()
        week_start = today - dt.timedelta(days=7)
        return sum(record.amount for record in self.records
                   if week_start <= record.date <= today)


class CashCalculator(Calculator):
    USD_RATE = 75.0
    EURO_RATE = 100.0

    def get_today_cash_remained(self, currency):
        pattern = self.limit - self.get_today_stats()
        remaining = {
            'usd': (round(pattern / self.USD_RATE, 2), 'USD'),
            'eur': (round(pattern / self.EURO_RATE, 2), 'Euro'),
            'rub': (round(pattern, 2), 'руб')
            }
        if remaining[currency][0] > 0:
            return (
                f'На сегодня осталось {remaining[currency][0]} '
                f'{remaining[currency][1]}'
            )
        if remaining[currency][0] == 0:
            return 'Денег нет, держись'
        return (
            f'Денег нет, держись: твой долг - '
            f'{abs(remaining[currency][0])} {remaining[currency][1]}'
        )


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        remaining = round(self.limit - self.get_today_stats(), 2)
        if remaining > 0:
            return (
                f'Сегодня можно съесть что-нибудь ещё, '
                f'но с общей калорийностью не более {remaining} кКал'
            )
        return 'Хватит есть!'
