#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from collections import defaultdict

input_file = sys.argv[1]
output_file = sys.argv[2]


def convert(s):
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


def conflict(e, c):
    ei = convert(e)
    ci = convert(c)
    return not (ei[1] < ci[0] or ei[0] > ci[1])


with open(input_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()
    n, m = list(map(int, lines[0].rstrip('\n').split(' ')))
    d = defaultdict(list)
    for i in range(n):
        l = lines[1+i].rstrip('\n').split(' ')
        num = int(l[1])
        ind = int(l[3])
        nam = l[2]
        t = l[4].split(',')
        for s in t:
            k = s.split('(')[0]
            r = s.split('(')[1].rstrip(')')
            d[k].append((r, num, ind, nam))

    with open(output_file, 'w', encoding='utf-8') as of:
        for i in range(m):
            l = lines[1+n+i].rstrip('\n').split(' ')
            num = int(l[0])
            ind = int(l[1])
            nam = l[2]
            t = l[5].split(',')
            w = set()
            for s in t:
                k = s.split('(')[0]
                r = s.split('(')[1].rstrip(')')
                for c in d[k]:
                    if conflict(r, c[0]):
                        w.add(c[1:])
            if len(w):
                of.write(f'{num} {ind} {nam}:\n')
                for t in sorted(w):
                    of.write(f'\t{t[0]} {t[1]} {t[2]}\n')
