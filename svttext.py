# -*- coding: utf-8 -*-
from collections import namedtuple
import re


Row = namedtuple('Row', 'game_no home_team away_team \
                        home_score away_score')

GAME_NO_END = 2
HOME_TEAM_START = 4
HOME_TEAM_END = 13
AWAY_TEAM_START = 14
AWAY_TEAM_END = 23
HOME_SCORE_START = 25
AWAY_SCORE_START = 27


def read_fixture():
    with open('fixtures/svttext.html') as f:
        return f.read()


def page_to_lines(html):
    pre_start = html.find("<pre class=\"root\"")
    pre_end = html.find("</pre>", pre_start)

    lines = []
    pre = html[pre_start:pre_end]
    rows = pre.split("\n")
    for r in rows[2:]:
        line = ''
        for s in r.split("</span>"):
            line += s[s.find(">") + 1:]
        lines.append(line)
    return lines


def parse_game(line):
    game_no = int(line[0:GAME_NO_END])
    home_team = line[HOME_TEAM_START:HOME_TEAM_END]
    away_team = line[AWAY_TEAM_START:AWAY_TEAM_END]
    home_score = 0
    away_score = 0

    m = re.search('(\d)-(\d)', line)
    if m:
        home_score = m.group(1)
        away_score = m.group(2)

    return Row(game_no,
               home_team.rstrip(),
               away_team.rstrip(),
               home_score,
               away_score)


def parse_utdelning(lines):
    utdelning = []
    for i, line in enumerate(lines):
        pengar = 0
        try:
            pengar = int(line[9:24].replace(".", ""))
        except:
            pass
        utdelning.append((13 - i, pengar))
    return utdelning


def parse_svttext(html):
    lines = page_to_lines(html)
    if len(lines) < 20:
        return None, None
    rows = []
    # Parse games
    for line in lines[:13]:
        rows.append(parse_game(line))

    # Parse utdelning
    return rows, parse_utdelning(lines[15:19])


def mock_row():
    rows = [
        Row(1, 'Lag ett', 'Lag tva', 1, 2),
        Row(2, 'Lag ett', 'Lag tva', 1, 2),
        Row(3, 'Lag ett', 'Lag tva', 1, 2),
        Row(4, 'Lag ett', 'Lag tva', 1, 2),
        Row(5, 'Lag ett', 'Lag tva', 1, 2),
        Row(6, 'Lag ett', 'Lag tva', 1, 2),
        Row(7, 'Lag ett', 'Lag tva', 1, 2),
        Row(8, 'Lag ett', 'Lag tva', 1, 2),
        Row(9, 'Lag ett', 'Lag tva', 1, 2),
        Row(10, 'Lag ett', 'Lag tva', 1, 2),
        Row(11, 'Lag ett', 'Lag tva', 1, 2),
        Row(12, 'Lag ett', 'Lag tva', 1, 2),
        Row(13, 'Lag ett', 'Lag tva', 1, 2),
    ]
    utdelning = ((13, 0), (12, 0), (11, 0), (10, 0))
    return utdelning, rows

if __name__ == '__main__':

    with open("fixtures/onelate.html") as f:
        html = f.read()
        print parse_svttext(html)

    #for fname in os.listdir("fixtures/allday"):
    #    with open("fixtures/allday/%s" % fname) as f:
    #        html = f.read()
    #        parse_svttext(html)
#    html = read_fixture()
#
#    parse2(html)
