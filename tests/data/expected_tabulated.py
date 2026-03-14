from __future__ import annotations

EXPECTED_TABULATED_HTML = """\
<table>
    <thead>
        <tr>
            <th style="padding-left: 1em; padding-right: 1em; text-align: center">category</th>
            <th style="padding-left: 1em; padding-right: 1em; text-align: center">date</th>
            <th style="padding-left: 1em; padding-right: 1em; text-align: center">downloads</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td style="padding-left: 1em; padding-right: 1em; text-align: left; vertical-align: top">2.6</td>
            <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">2018-08-15</td>
            <td style="padding-left: 1em; padding-right: 1em; text-align: right; vertical-align: top">51</td>
        </tr>
        <tr>
            <td style="padding-left: 1em; padding-right: 1em; text-align: left; vertical-align: top">2.7</td>
            <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">2018-08-15</td>
            <td style="padding-left: 1em; padding-right: 1em; text-align: right; vertical-align: top">63,749</td>
        </tr>
        <tr>
            <td style="padding-left: 1em; padding-right: 1em; text-align: left; vertical-align: top">3.2</td>
            <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">2018-08-15</td>
            <td style="padding-left: 1em; padding-right: 1em; text-align: right; vertical-align: top">2</td>
        </tr>
        <tr>
            <td style="padding-left: 1em; padding-right: 1em; text-align: left; vertical-align: top">3.3</td>
            <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">2018-08-15</td>
            <td style="padding-left: 1em; padding-right: 1em; text-align: right; vertical-align: top">40</td>
        </tr>
        <tr>
            <td style="padding-left: 1em; padding-right: 1em; text-align: left; vertical-align: top">3.4</td>
            <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">2018-08-15</td>
            <td style="padding-left: 1em; padding-right: 1em; text-align: right; vertical-align: top">6,095</td>
        </tr>
        <tr>
            <td style="padding-left: 1em; padding-right: 1em; text-align: left; vertical-align: top">3.5</td>
            <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">2018-08-15</td>
            <td style="padding-left: 1em; padding-right: 1em; text-align: right; vertical-align: top">20,358</td>
        </tr>
        <tr>
            <td style="padding-left: 1em; padding-right: 1em; text-align: left; vertical-align: top">3.6</td>
            <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">2018-08-15</td>
            <td style="padding-left: 1em; padding-right: 1em; text-align: right; vertical-align: top">35,274</td>
        </tr>
        <tr>
            <td style="padding-left: 1em; padding-right: 1em; text-align: left; vertical-align: top">3.7</td>
            <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">2018-08-15</td>
            <td style="padding-left: 1em; padding-right: 1em; text-align: right; vertical-align: top">6,595</td>
        </tr>
        <tr>
            <td style="padding-left: 1em; padding-right: 1em; text-align: left; vertical-align: top">3.8</td>
            <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">2018-08-15</td>
            <td style="padding-left: 1em; padding-right: 1em; text-align: right; vertical-align: top">3</td>
        </tr>
        <tr>
            <td style="padding-left: 1em; padding-right: 1em; text-align: left; vertical-align: top">null</td>
            <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">2018-08-15</td>
            <td style="padding-left: 1em; padding-right: 1em; text-align: right; vertical-align: top">1,019</td>
        </tr>
    </tbody>
</table>
"""  # noqa: E501

EXPECTED_TABULATED_PRETTY = """
┌──────────┬────────────┬───────────┐
│ category │    date    │ downloads │
├──────────┼────────────┼───────────┤
│ 2.6      │ 2018-08-15 │        51 │
│ 2.7      │ 2018-08-15 │    63,749 │
│ 3.2      │ 2018-08-15 │         2 │
│ 3.3      │ 2018-08-15 │        40 │
│ 3.4      │ 2018-08-15 │     6,095 │
│ 3.5      │ 2018-08-15 │    20,358 │
│ 3.6      │ 2018-08-15 │    35,274 │
│ 3.7      │ 2018-08-15 │     6,595 │
│ 3.8      │ 2018-08-15 │         3 │
│ null     │ 2018-08-15 │     1,019 │
└──────────┴────────────┴───────────┘
"""

EXPECTED_TABULATED_MD = """
| category |    date    | downloads |
| :--------| :--------: |---------: |
| 2.6      | 2018-08-15 |        51 |
| 2.7      | 2018-08-15 |    63,749 |
| 3.2      | 2018-08-15 |         2 |
| 3.3      | 2018-08-15 |        40 |
| 3.4      | 2018-08-15 |     6,095 |
| 3.5      | 2018-08-15 |    20,358 |
| 3.6      | 2018-08-15 |    35,274 |
| 3.7      | 2018-08-15 |     6,595 |
| 3.8      | 2018-08-15 |         3 |
| null     | 2018-08-15 |     1,019 |
"""


EXPECTED_TABULATED_RST = """
.. table::

    ==========  ============  ===========
     category       date       downloads 
    ==========  ============  ===========
     2.6         2018-08-15           51 
     2.7         2018-08-15       63,749 
     3.2         2018-08-15            2 
     3.3         2018-08-15           40 
     3.4         2018-08-15        6,095 
     3.5         2018-08-15       20,358 
     3.6         2018-08-15       35,274 
     3.7         2018-08-15        6,595 
     3.8         2018-08-15            3 
     null        2018-08-15        1,019 
    ==========  ============  ===========
"""  # noqa: W291

EXPECTED_TABULATED_TSV = """
"category"\t"date"\t"downloads"
"2.6"\t"2018-08-15"\t51
"2.7"\t"2018-08-15"\t63,749
"3.2"\t"2018-08-15"\t2
"3.3"\t"2018-08-15"\t40
"3.4"\t"2018-08-15"\t6,095
"3.5"\t"2018-08-15"\t20,358
"3.6"\t"2018-08-15"\t35,274
"3.7"\t"2018-08-15"\t6,595
"3.8"\t"2018-08-15"\t3
"null"\t"2018-08-15"\t1,019
"""
