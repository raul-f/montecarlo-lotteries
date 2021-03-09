from typing import List, Tuple, Dict, Union
from random import randrange
from textwrap import dedent
import time

class Lottery():
    """
        parameters:
        - drawing_weekdays: List of the weekday IDs in which the lottery is 
        drawn.
        - bet_prices: List of bet prices for each possible bet size.
        - bet_size_limits: Tuple of the minimum and maximum bet sizes.
        - lottery_numbers: number of possible number choices in a lottery.

        relevant concepts:
        - bet size: amount of numbers in a bet.
            e.g. [1, 2, 3, 4, 5, 6, 7] has a bet size of 7.
        
        Days IDs: 1 == Sunday and 7 == Saturday.

        Lottery IDs: 
        - Mega-Sena: 1
    """
    def __init__(
        self, 
        drawing_weekdays: List[int], 
        bet_sizes: List[Dict[str, int]], 
        lottery_numbers: int, 
        draw_size: int, 
        lottery_id: int, 
        lottery_name: str
    ):
        self.drawing_weekdays = drawing_weekdays
        self.draw_size = draw_size
        self.bet_sizes = bet_sizes
        self.bet_size_limits = (bet_sizes[0]['size'], bet_sizes[-1]['size'])
        self.lottery_numbers = lottery_numbers
        self.lottery_id = lottery_id
        self.lottery_name = lottery_name

    def __str__(self):
        return  dedent(f"""
            - Name: {self.lottery_name};
            - Draw days: {self.drawing_weekdays};
            - Draw size: {self.draw_size};
            - Maximum and minimum bet sizes: {self.bet_size_limits};
            - Bet sizes: {self.bet_sizes};
            - Lottery ID: {self.lottery_id};
            - Lottery numbers: {self.lottery_numbers}
        """)

class Iteration():
    """
        Days IDs: 1 == Sunday and 7 == Saturday.
        Lottery IDs: 
        - Mega-Sena: 1
    """
    def __init__(self, lotto: Lottery, bet_size: int):
        self.weekday = lotto.drawing_weekdays[0]
        self.drawing_weekdays = lotto.drawing_weekdays
        self.lottery: Lottery = lotto
        self.draw_size = lotto.draw_size
        self.total_days: int = 0
        self.total_expenditure: int = 0
        self.total_cycles: int = 0
        self.win: bool = False

        if bet_size > self.lottery.bet_size_limits[-1]:
            self.bet_size = self.lottery.bet_size_limits[-1]
        elif bet_size < self.lottery.bet_size_limits[0]:
            self.bet_size = self.lottery.bet_size_limits[0]
        else:
            self.bet_size = bet_size

        for size in lotto.bet_sizes:
            if size['size'] == self.bet_size:
                self.bet_price = size['price']

    def draw(self) -> List[int]:
        counter = 0
        draw: List[int] = []
        while counter < self.draw_size:
            num = randrange(1, self.lottery.lottery_numbers + 1, 1)
            if (num not in draw):
                draw.append(num)
                counter += 1
        return sorted(draw)

    def check(self, bet: List[int], draw: List[int]) -> bool:
        self.total_expenditure += self.bet_price
        self.total_cycles += 1

        # print(bet)
        # print(draw)
        # time.sleep(1)

        for num in draw:
            if (num not in bet):
                return False
        self.win = True
        return True

    """
        If the next day is in this same week, returns false.
        Else, returns true.
    """
    def advance_time(self) -> bool:
        for day in self.drawing_weekdays:
            if day > self.weekday:
                self.total_days += day - self.weekday
                self.weekday = day
                return False
        day = self.drawing_weekdays[0]
        self.total_days += 7 + day - self.weekday
        self.weekday = day
        return True