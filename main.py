#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from random import randrange
from statistics import mean

from rich.console import Console
from rich.table import Table

from LRU import Lru
from FIFO import Fifo
from Optimal import Optimal

TEST_COUNT = 1000
MIN_PAGE_LENGTH = 1
MAX_PAGE_LENGTH = 20
MAX_RANGE = 10
FRAMES = [3, 4, 5, 6]


if __name__ == '__main__':
    run_results = {}
    # provided pages
    pages1 = [7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2, 1, 2, 0, 1, 7, 0, 1]
    pages2 = [8, 1, 0, 7, 3, 0, 3, 4, 5, 3, 5, 2, 0, 6, 8, 4, 8, 1, 5, 3]
    pages3 = [4, 6, 4, 8, 6, 3, 6, 0, 5, 9, 2, 1, 0, 4, 6, 3, 0, 6, 8, 4]
    page_list = [pages1, pages2, pages3]
    # Create random versions
    for test_num in range(TEST_COUNT):
        new_list = []
        # prevent divide by 0 error
        if MIN_PAGE_LENGTH < 1:
            MIN_PAGE_LENGTH = 0
        # page length between MIN_PAGE_LENGTH and MAX_PAGE_LENGTH
        for index in range(randrange(MIN_PAGE_LENGTH, MAX_PAGE_LENGTH + 1)):
            # generate from a range of possible ints set in MAX_RANGE
            new_list.append(randrange(MAX_RANGE))
        page_list.append(new_list)
    # run tests number of TEST_COUNT times
    for frame in FRAMES:
        # faults
        fifo_fault_list = []
        opt_fault_list = []
        lru_fault_list = []
        # hit rates
        fifo_hit_rate_list = []
        opt_hit_rate_list = []
        lru_hit_rate_list = []
        # fault rates
        fifo_fault_rate_list = []
        opt_fault_rate_list = []
        lru_fault_rate_list = []

        # create objects
        fifo = Fifo()
        optimal = Optimal()
        lru = Lru()
        # set frames
        fifo.frame_count = frame
        optimal.frame_count = frame
        lru.frame_count = frame

        for pages in page_list:
            # run algorithm and append results to lists
            # fifo
            fifo.process_all(pages)
            fifo_fault_list.append(fifo.fault_count)
            fifo_hit_rate_list.append(fifo.hit_count/len(pages))
            fifo_fault_rate_list.append(fifo.fault_count/len(pages))
            #optimal
            optimal.process_all(pages)
            opt_fault_list.append(optimal.fault_count)
            opt_hit_rate_list.append(optimal.hit_count/len(pages))
            opt_fault_rate_list.append(optimal.fault_count/len(pages))
            #lru
            lru.process_all(pages)
            lru_fault_list.append(lru.fault_count)
            lru_hit_rate_list.append(lru.hit_count/len(pages))
            lru_fault_rate_list.append(lru.fault_count/len(pages))
            # clear objects for next iteration
            fifo.clear()
            optimal.clear()
            lru.clear()

        # avg fault counts
        fifo_avg_fault_count = mean(fifo_fault_list)
        opt_avg_fault_count = mean(opt_fault_list)
        lru_avg_fault_count = mean(lru_fault_list)
        # avg hit rates
        fifo_avg_hit_rate = mean(fifo_hit_rate_list)
        opt_avg_hit_rate = mean(opt_hit_rate_list)
        lru_avg_hit_rate = mean(lru_hit_rate_list)
        # avg. fault rates
        fifo_avg_fault_rate = mean(fifo_fault_rate_list)
        opt_avg_fault_rate = mean(opt_fault_rate_list)
        lru_avg_fault_rate = mean(lru_fault_rate_list)

        run_results[frame] = {
            'fifo_avg_fault_count': fifo_avg_fault_count,
            'opt_avg_fault_count': opt_avg_fault_count,
            'lru_avg_fault_count': lru_avg_fault_count,
            'fifo_avg_hit_rate': fifo_avg_hit_rate,
            'opt_avg_hit_rate': opt_avg_hit_rate,
            'lru_avg_hit_rate': lru_avg_hit_rate,
            'fifo_avg_fault_rate': fifo_avg_fault_rate,
            'opt_avg_fault_rate': opt_avg_fault_rate,
            'lru_avg_fault_rate': lru_avg_fault_rate,
        }

    for key, results in run_results.items():
        # create table
        table = Table(title=f'Paging Results for {TEST_COUNT} tests and {key} frames.')
        # add columns
        table.add_column('Algorithm', justify='center', style='cyan', no_wrap=True)
        table.add_column('Avg. Fault Count', justify='center', style='magenta', no_wrap=True)
        table.add_column('Avg. Hit Rate', justify='center', style='cyan', no_wrap=True)
        table.add_column('Avg. Fault Rate', justify='center', style='magenta', no_wrap=True)
        # add rows
        table.add_row(
            'FIFO', f'{results["fifo_avg_fault_count"]}',
            f'{results["fifo_avg_hit_rate"]}',
            f'{results["fifo_avg_fault_rate"]}'
        )
        table.add_row(
            'Optimal', f'{results["opt_avg_fault_count"]}',
            f'{results["opt_avg_hit_rate"]}',
            f'{results["opt_avg_fault_rate"]}'
        )
        table.add_row(
            'LRU',
            f'{results["lru_avg_fault_count"]}',
            f'{results["lru_avg_hit_rate"]}',
            f'{results["lru_avg_fault_rate"]}'
        )
        # print table
        console = Console(record=True)
        console.print(table, justify='center')
