import datetime as dt


class Record:
    """Класс записи."""

    def __init__(self, amount, comment, date=None) -> None:
        self.amount = amount
        self.comment = comment
        if date is not None:
            self.moment = dt.datetime.strptime(date, '%d.%m.%Y')
            self.date = self.moment.date()
        else:
            self.moment = dt.datetime.now()
            self.date = self.moment.date()


class Calculator:
    """Родительский класс."""

    def __init__(self, limit) -> None:
        self.records = []
        self.limit = limit

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        self.summ = 0
        self.moment = dt.datetime.now()
        self.cur_date = self.moment.date()
        for i in range(len(self.records)):
            if self.cur_date == self.records[i].date:
                self.summ += self.records[i].amount
        return self.summ

    def get_week_stats(self):
        self.summ = 0
        self.moment = dt.datetime.now()
        self.cur_date = self.moment.date()
        for i in range(len(self.records)):
            if (self.cur_date - dt.timedelta(days=7)
                    < self.records[i].date
                    <= self.cur_date):
                self.summ += self.records[i].amount
        return self.summ

    def print_val(self):
        print('Записей в базе - ', len(self.records))
        for i in range(len(self.records)):
            print(f'Значение в записи № {i} - {self.records[i].amount}')
            print(f'Комментарий в записи №{i} - {self.records[i].comment}')
            print(f'Дата в записи №{i} - {self.records[i].date}')


class CaloriesCalculator(Calculator):
    """Калькулятор каллорий."""

    def get_calories_remained(self):
        self.difference = self.limit - self.get_today_stats()
        if self.difference > 0:
            return ('Сегодня можно съесть что-нибудь ещё, но '
                    f'с общей калорийностью не более {self.difference} кКал')
        else:
            return 'Хватит есть!'


class CashCalculator(Calculator):

    USD_RATE = 71.88
    EURO_RATE = 83.14

    def get_today_cash_remained(self, currency):
        self.currency = currency
        if self.currency == 'usd':
            self.divider = self.USD_RATE
            self.cur_sign = 'USD'
        elif self.currency == 'eur':
            self.divider = self.EURO_RATE
            self.cur_sign = 'Euro'
        else:
            self.divider = 1
            self.cur_sign = 'руб'
        self.difference = self.limit - self.get_today_stats()
        if self.difference > 0:
            return ('На сегодня осталось '
                    f'{round(self.difference / self.divider, 2)} '
                    f'{self.cur_sign}')
        elif self.difference == 0:
            return 'Денег нет, держись'
        else:
            return ('Денег нет, держись: твой долг - '
                    f'{round(abs(self.difference / self.divider), 2)} '
                    f'{self.cur_sign}')


cash_calculator = CashCalculator(189)

cash_calculator.add_record(Record(amount=1186,
                                  comment='Кусок тортика. И ещё один.',
                                  date='24.02.2019'))
cash_calculator.add_record(Record(amount=84, comment='Йогурт.',
                                  date='23.02.2019'))
cash_calculator.add_record(Record(amount=1140, comment='Баночка чипсов.'))
cash_calculator.add_record(Record(amount=145, comment='кофе'))
cash_calculator.add_record(Record(amount=300, comment='Серёге за обед'))
cash_calculator.add_record(Record(amount=3000,
                                  comment='бар в Танин др',
                                  date='07.10.2021'))

cash_calculator.get_today_stats()
cash_calculator.get_week_stats()
print(cash_calculator.get_today_cash_remained('usd'))
