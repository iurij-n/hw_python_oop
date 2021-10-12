import datetime as dt
from typing import Optional, List, Dict


class Record:
    """Класс записи."""

    def __init__(self, amount: int, comment: str,
                 date: Optional[str] = None) -> None:
        """Конструктор класса."""
        self.amount: int = amount
        self.comment: str = comment
        self.DATE_FORMAT: str = '%d.%m.%Y'
        if date is not None:
            self.moment = dt.datetime.strptime(date, self.DATE_FORMAT)
            self.date = self.moment.date()
        else:
            self.moment = dt.datetime.now()
            self.date = self.moment.date()


class Calculator:
    """Родительский класс."""

    def __init__(self, limit: int) -> None:
        """Конструктор класса."""
        self.records: List = []
        self.limit: int = limit

    def add_record(self, record) -> None:
        """Добавляет новую запись."""
        self.records.append(record)

    def get_today_stats(self) -> int:
        """Статистика за день."""
        self.moment = dt.datetime.now()
        self.cur_date = self.moment.date()
        return sum([self.records[i].amount for i in range(len(self.records))
                   if self.cur_date == self.records[i].date])

    def get_week_stats(self) -> int:
        """Статистика за неделю."""
        self.moment = dt.datetime.now()
        self.cur_date = self.moment.date()
        return sum([self.records[i].amount for i in range(len(self.records))
                   if (self.cur_date - dt.timedelta(days=7)
                   < self.records[i].date
                   <= self.cur_date)])

    def difference(self) -> int:
        """Сравниваем дневную статистик с лимитом"""
        return self.limit - self.get_today_stats()


class CaloriesCalculator(Calculator):
    """Калькулятор каллорий."""

    def get_calories_remained(self) -> str:
        """Определяем сколько ещё калорий можно/нужно получить сегодня."""
        if self.difference() > 0:
            return ('Сегодня можно съесть что-нибудь ещё, но '
                    f'с общей калорийностью не более {self.difference()} кКал')
        if self.difference() <= 0:
            return 'Хватит есть!'


class CashCalculator(Calculator):
    """Калькулятор денег."""

    USD_RATE: float = 60.0
    EURO_RATE: float = 70.0
    A_C: Dict = {
        'usd': ['USD', USD_RATE],
        'eur': ['Euro', EURO_RATE],
        'rub': ['руб', 1]
    }

    POSITIVE_BALANCE: str = 'На сегодня осталось {balance} {currency_name}'
    ZERO_BALANCE: str = 'Денег нет, держись'
    NEGATIVE_BALANCE: str = 'Денег нет, держись: твой \
долг - {balance} {currency_name}'

    def get_today_cash_remained(self, currency: str) -> str:
        """Определяем сколько еще денег можно потратить сегодня."""
        if self.difference() > 0:
            return (self.POSITIVE_BALANCE.format(balance=str(round(
                    self.difference()/self.A_C[currency][1], 2)),
                    currency_name=self.A_C[currency][0]))
        if self.difference() == 0:
            return self.ZERO_BALANCE
        if self.difference() < 0:
            return (self.NEGATIVE_BALANCE.format(balance=str(round(
                    abs(self.difference()/self.A_C[currency][1]), 2)),
                    currency_name=self.A_C[currency][0]))


if __name__ == "__main__":
    cash_calculator = CashCalculator(0)

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
    print(cash_calculator.get_today_cash_remained('eur'))
