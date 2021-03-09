from typing import List, Tuple, Union
from datetime import datetime, timedelta
from random import randrange
import locale
import json
from mysql import connector
from textwrap import dedent
from classes import Lottery, Iteration
MySQLConnection, CMySQLConnection = connector.MySQLConnection, connector.CMySQLConnection

def main() -> None:
    #combinations: int = 50_063_860
    runs: List[Iteration] = []
    full_data = []
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
    counter = 0

    db = connector.connect(
        host = 'localhost',
        user = 'root',
        password = '04B438u?y', 
        database = 'simulador_loterias'
    )
    cursor = db.cursor()

    lottery = get_lottery(1, db)

    while (counter < 2048):
        runs.append(simulate_run(lottery, [1, 2, 3, 4, 5, 6]))
        run_data = {
            'days': runs[counter].total_days,
            'cents': runs[counter].total_expenditure,
            'years': f'{runs[counter].total_days/365:,.2f}',
            'BRL': locale.currency(runs[counter].total_expenditure/100, grouping=True),
            'id_lottery': runs[counter].lottery.lottery_id,
            'bet_size': runs[counter].bet_size,
            'draws': runs[counter].total_cycles
        }
        full_data.append(run_data)
        query = """
            INSERT INTO Iterations (Days, Centavos, Years, BRL, idLottery, BetSize, Draws)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        values = (run_data['days'], run_data['cents'], run_data['years'], run_data['BRL'], run_data['id_lottery'], run_data['bet_size'], run_data['draws'])
        cursor.execute(query, values)
        db.commit()

        print(dedent(f"""
            Run #{counter + 1} complete.
            Run results:
            - {full_data[counter]['years']} years have passed.
            - {full_data[counter]['BRL']} BRL spent.
            - {full_data[counter]['draws']:,} draws were done.
            - The bet size was {full_data[counter]['bet_size']}.
            """)
        )
        counter += 1
    print(f"\nThe average timespan was {reduce(lambda x, y: x + y[0], runs)/(len(runs) * 365):,.2f} years")
    print(f"The average expenditure was {locale.currency(reduce(lambda x, y: x + y[1], runs)/(len(runs) * 100), grouping=True)} BRL")

def reduce(func, ipt_list, init_val = 0):
    val = init_val
    for item in ipt_list[0:]:
        val = func(val, item)
    return val

def simulate_run(lottery: Lottery, bet: List[int]) -> Iteration:
    run = Iteration(lottery, len(bet))
    while(not run.check(bet, run.draw())):
        run.advance_time()
    return run

def get_lottery(lottery_id: int, database: Union[MySQLConnection, CMySQLConnection]) -> Lottery:
    cursor = database.cursor()
    lottery_query = """
        SELECT * 
        FROM Lotteries
        WHERE idLottery = %s;
    """
    cursor.execute(lottery_query, tuple([lottery_id]))

    op_results = cursor.fetchall()
    lottery = {
        'id': op_results[0][0],
        'numbers': op_results[0][1],
        'draw_size': op_results[0][2],
        'name': op_results[0][3],
    }

    bet_sizes_query = """
        SELECT 
            idBetSize, 
            size,
            price
        FROM BetSizes
        WHERE idLottery = %s AND active = 1
        ORDER BY size;
    """
    cursor.execute(bet_sizes_query, tuple([lottery_id]))

    op_results = cursor.fetchall()
    lottery['bet_sizes'] = list(map(lambda x: {'size': x[1], 'price': x[2]}, op_results))

    drawing_days_query = """
        SELECT 
            idDrawingDay, 
            idWeekday
        FROM DrawingDays
        WHERE idLottery = %s AND active = 1
        ORDER BY idWeekday;
    """
    cursor.execute(drawing_days_query, tuple([lottery_id]))

    op_results = cursor.fetchall()
    lottery['drawing_days'] = list(map(lambda x: x[1], op_results))
    
    return Lottery(
        lottery['drawing_days'], 
        lottery['bet_sizes'],
        lottery['numbers'],
        lottery['draw_size'],
        lottery['id'],
        lottery['name']
    )

def test() -> None:
    db = connector.connect(
        host = 'localhost',
        user = 'root',
        password = '04B438u?y', 
        database = 'simulador_loterias'
    )
    
    lottery = get_lottery(1, db)

    run = simulate_run(lottery, [1, 2, 3, 4, 5, 6])

    # run = simulate_run(10000)
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
    run_data = {
        'days': run.total_days,
        'centavos': run.total_expenditure,
        'years': f'{run.total_days/365:,.2f}',
        'BRL': locale.currency(run.total_expenditure/100, grouping=True)
    }
    print(dedent(
        f"""
        Run results:
            - {run_data['years']} years have passed.
            - {run_data['BRL']} BRL spent.
        Raw data:
            - {run_data['days']} days.
            - {run_data['centavos']} centavos.
        """
    ))

main()
#test()
