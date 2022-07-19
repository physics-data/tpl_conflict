#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from collections import defaultdict

input_file = sys.argv[1]
output_file = sys.argv[2]


# convert description of week range to interval
def to_interval(s):
    i = [0, 0]
    if s == u'全周':
        i = [1, 16]
    elif s == u'前八周':
        i = [1, 8]
    elif s == u'后八周':
        i = [9, 16]
    else:
        l = int(s.split('-')[0])
        r = int(s.split('-')[1])
        i = [l, r]
    return i


# check whether two week ranges conflict
def conflict(e, c):
    ei = to_interval(e)
    ci = to_interval(c)
    return not (ei[1] < ci[0] or ei[0] > ci[1])


with open(input_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()
    n, m = list(map(int, lines[0].rstrip('\n').split(' ')))
    time_slots = defaultdict(list)  # all available slots

    # read selected courses
    for i in range(n):
        l = lines[1+i].rstrip('\n').split(' ')
        num, index, name = int(l[1]), int(l[3]), l[2]
        # process time list
        for s in l[4].split(','):
            slot = s.split('(')[0]
            weeks = s.split('(')[1].rstrip(')')
            time_slots[slot].append((weeks, num, index, name))

    with open(output_file, 'w', encoding='utf-8') as of:
        # read candidate courses
        for i in range(m):
            l = lines[1+n+i].rstrip('\n').split(' ')
            num, index, name = int(l[0]), int(l[1]), l[2]
            conflicts = set()
            # check week range conflicts
            for s in l[5].split(','):
                slot = s.split('(')[0]
                req_weeks = s.split('(')[1].rstrip(')')  # requested range
                for curr_weeks, *info in time_slots[slot]:
                    if conflict(req_weeks, curr_weeks):
                        conflicts.add(tuple(info))
            # output conflicts if not empty
            if len(conflicts) != 0:
                of.write(f'{num} {index} {name}:\n')
                for info in sorted(conflicts):
                    of.write(f'\t{"{} {} {}".format(*info)}\n')
