#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from random import randrange
from statistics import mean

from rich.console import Console
from rich.table import Table

from LRU import Lru
from FIFO import Fifo
from Optimal import Optimal

PAGE_LENGTHS = [10, 15, 20]
MAX_RANGE = 10
FRAMES = [3, 5, 7]
# Config is:
# {
#   frame: {
#       page_length: [
#           ref_strings_lists,
#       ]
#   }
# }
CONFIG = {}
for frame in FRAMES:
    CONFIG[frame] = {}
    for page_length in PAGE_LENGTHS:
        CONFIG[frame][page_length] = []
        new_list = []
        for i in range(page_length):
            # generate from a range of possible ints set in MAX_RANGE
            new_list.append(randrange(MAX_RANGE))
        CONFIG[frame][page_length].append(new_list)

PAGES1 = [7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2, 1, 2, 0, 1, 7, 0, 1]
PAGES2 = [8, 1, 0, 7, 3, 0, 3, 4, 5, 3, 5, 2, 0, 6, 8, 4, 8, 1, 5, 3]
PAGES3 = [4, 6, 4, 8, 6, 3, 6, 0, 5, 9, 2, 1, 0, 4, 6, 3, 0, 6, 8, 4]
# as per "The ones given would be a part of this group [rss: 20, npf: 3]
# but they would not be determined randomly. The numbers are given to you."
CONFIG[3][len(PAGES1)].append(PAGES1)
CONFIG[3][len(PAGES2)].append(PAGES2)
CONFIG[3][len(PAGES3)].append(PAGES3)

if __name__ == '__main__':
    run_results = []
    # create objects
    fifo = Fifo()
    optimal = Optimal()
    lru = Lru()
    key = 1
    for frame, page_lengths in CONFIG.items():
        for page, ref_strings in page_lengths.items():
            print(f'Config: {page}:{frame}')
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
            # set frames
            fifo.frame_count = frame
            optimal.frame_count = frame
            lru.frame_count = frame
            # add results to lists for later calculation
            for ref_str in ref_strings:
                # fifo
                fifo.process_all(ref_str)
                print(f'    FIFO fault count: {fifo.fault_count}')
                fifo_fault_list.append(fifo.fault_count)
                fifo_hit_rate_list.append(fifo.hit_count/len(ref_str))
                fifo_fault_rate_list.append(fifo.fault_count/len(ref_str))
                # optimal
                optimal.process_all(ref_str)
                print(f'    OPT fault count: {optimal.fault_count}')
                opt_fault_list.append(optimal.fault_count)
                opt_hit_rate_list.append(optimal.hit_count/len(ref_str))
                opt_fault_rate_list.append(optimal.fault_count/len(ref_str))
                # lru
                lru.process_all(ref_str)
                print(f'    LRU fault count: {lru.fault_count}')
                lru_fault_list.append(lru.fault_count)
                lru_hit_rate_list.append(lru.hit_count/len(ref_str))
                lru_fault_rate_list.append(lru.fault_count/len(ref_str))
                # clear objects for next iteration
                fifo.clear()
                optimal.clear()
                lru.clear()
            # averages
            run_results.append({
                'frame_count': frame,
                'page_length': page,
                'fifo_avg_fault_count': mean(fifo_fault_list),
                'opt_avg_fault_count': mean(opt_fault_list),
                'lru_avg_fault_count': mean(lru_fault_list),
                'fifo_avg_hit_rate': mean(fifo_hit_rate_list),
                'opt_avg_hit_rate': mean(opt_hit_rate_list),
                'lru_avg_hit_rate': mean(lru_hit_rate_list),
                'fifo_avg_fault_rate': mean(fifo_fault_rate_list),
                'opt_avg_fault_rate': mean(opt_fault_rate_list),
                'lru_avg_fault_rate': mean(lru_fault_rate_list),
            })
    print('----------------------------------------------------------------------------')
    for result in run_results:
        # create table
        table = Table(
            title=f'Paging Results with {result["frame_count"]} frames and reference length {result["page_length"]}.'
        )
        # add columns
        table.add_column('Algorithm', justify='center', style='cyan', no_wrap=True)
        table.add_column('Avg. Fault Count', justify='center', style='magenta', no_wrap=True)
        table.add_column('Avg. Hit Rate', justify='center', style='cyan', no_wrap=True)
        table.add_column('Avg. Fault Rate', justify='center', style='magenta', no_wrap=True)
        # add rows
        table.add_row(
            'FIFO', f'{result["fifo_avg_fault_count"]}',
            f'{result["fifo_avg_hit_rate"]}',
            f'{result["fifo_avg_fault_rate"]}'
        )
        table.add_row(
            'Optimal', f'{result["opt_avg_fault_count"]}',
            f'{result["opt_avg_hit_rate"]}',
            f'{result["opt_avg_fault_rate"]}'
        )
        table.add_row(
            'LRU',
            f'{result["lru_avg_fault_count"]}',
            f'{result["lru_avg_hit_rate"]}',
            f'{result["lru_avg_fault_rate"]}'
        )
        # print table
        console = Console(record=True)
        console.print(table, justify='center')
