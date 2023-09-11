# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_analytic_quoted_currency 1'] = [
    {
        'charcode': 'TVD',
        'date': '2023-06-10T00:00:00+03:00',
        'id': 37,
        'is_max_value': True,
        'is_min_value': False,
        'is_threshold_exceeded': True,
        'percentage_ratio': '406.62%',
        'threshold_match_type': 'exceeded',
        'value': 9063.5187
    },
    {
        'charcode': 'TVD',
        'date': '2023-06-10T00:00:00+03:00',
        'id': 38,
        'is_max_value': False,
        'is_min_value': True,
        'is_threshold_exceeded': False,
        'percentage_ratio': '44.76%',
        'threshold_match_type': 'less',
        'value': 997.7162
    },
    {
        'charcode': 'TVD',
        'date': '2023-06-10T00:00:00+03:00',
        'id': 39,
        'is_max_value': False,
        'is_min_value': False,
        'is_threshold_exceeded': True,
        'percentage_ratio': '100.00%',
        'threshold_match_type': 'equal',
        'value': 2229.0
    }
]

snapshots['test_cached_quotes_list_by_anon 1'] = [
    {
        'charcode': 'NPR',
        'date': '2023-06-09 21:00:00+00',
        'id': 10,
        'value': 6036.4963
    },
    {
        'charcode': 'NPR',
        'date': '2023-06-09 21:00:00+00',
        'id': 11,
        'value': 8833.265
    },
    {
        'charcode': 'NPR',
        'date': '2023-06-09 21:00:00+00',
        'id': 12,
        'value': 8127.9149
    },
    {
        'charcode': 'ALL',
        'date': '2023-06-09 21:00:00+00',
        'id': 13,
        'value': 4343.0352
    },
    {
        'charcode': 'ALL',
        'date': '2023-06-09 21:00:00+00',
        'id': 14,
        'value': 9410.327
    },
    {
        'charcode': 'ALL',
        'date': '2023-06-09 21:00:00+00',
        'id': 15,
        'value': 9536.2533
    },
    {
        'charcode': 'KPW',
        'date': '2023-06-09 21:00:00+00',
        'id': 16,
        'value': 403.2423
    },
    {
        'charcode': 'KPW',
        'date': '2023-06-09 21:00:00+00',
        'id': 17,
        'value': 5545.1006
    },
    {
        'charcode': 'KPW',
        'date': '2023-06-09 21:00:00+00',
        'id': 18,
        'value': 7182.565
    }
]

snapshots['test_quotes_list_by_anon 1'] = [
    {
        'charcode': 'NPR',
        'date': '2023-06-09 21:00:00+00',
        'id': 1,
        'value': 6036.4963
    },
    {
        'charcode': 'NPR',
        'date': '2023-06-09 21:00:00+00',
        'id': 2,
        'value': 8833.265
    },
    {
        'charcode': 'NPR',
        'date': '2023-06-09 21:00:00+00',
        'id': 3,
        'value': 8127.9149
    },
    {
        'charcode': 'ALL',
        'date': '2023-06-09 21:00:00+00',
        'id': 4,
        'value': 4343.0352
    },
    {
        'charcode': 'ALL',
        'date': '2023-06-09 21:00:00+00',
        'id': 5,
        'value': 9410.327
    },
    {
        'charcode': 'ALL',
        'date': '2023-06-09 21:00:00+00',
        'id': 6,
        'value': 9536.2533
    },
    {
        'charcode': 'KPW',
        'date': '2023-06-09 21:00:00+00',
        'id': 7,
        'value': 403.2423
    },
    {
        'charcode': 'KPW',
        'date': '2023-06-09 21:00:00+00',
        'id': 8,
        'value': 5545.1006
    },
    {
        'charcode': 'KPW',
        'date': '2023-06-09 21:00:00+00',
        'id': 9,
        'value': 7182.565
    }
]

snapshots['test_quotes_list_by_user 1'] = [
    {
        'charcode': 'TVD',
        'date': '2023-06-09 21:00:00+00',
        'id': 19,
        'value': 9063.5187
    },
    {
        'charcode': 'TVD',
        'date': '2023-06-09 21:00:00+00',
        'id': 19,
        'value': 9063.5187
    },
    {
        'charcode': 'TVD',
        'date': '2023-06-09 21:00:00+00',
        'id': 19,
        'value': 9063.5187
    },
    {
        'charcode': 'TVD',
        'date': '2023-06-09 21:00:00+00',
        'id': 20,
        'value': 997.7162
    },
    {
        'charcode': 'TVD',
        'date': '2023-06-09 21:00:00+00',
        'id': 20,
        'value': 997.7162
    },
    {
        'charcode': 'TVD',
        'date': '2023-06-09 21:00:00+00',
        'id': 20,
        'value': 997.7162
    },
    {
        'charcode': 'TVD',
        'date': '2023-06-09 21:00:00+00',
        'id': 21,
        'value': 2229.0
    },
    {
        'charcode': 'TVD',
        'date': '2023-06-09 21:00:00+00',
        'id': 21,
        'value': 2229.0
    },
    {
        'charcode': 'TVD',
        'date': '2023-06-09 21:00:00+00',
        'id': 21,
        'value': 2229.0
    }
]
