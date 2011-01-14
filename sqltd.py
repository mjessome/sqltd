#!/usr/bin/env python

import sqlite3
import sys
import re

def runPage(db, html):
        def parseStrings(s, query=[False]):
                output = ''
                if s == '<sql>':
                        query[0] = True
                elif s == '</sql>':
                        query[0] = False
                elif query[0]:
                        result = dbExecute(db, s)
                        output = '<table>\n%s</table>\n' % (''.join(makeTable(result)))
                else:
                        output = ''.join(s)
                return output

        split = re.split('(<sql>|</sql>)', html)

        return ''.join([parseStrings(s) for s in split])


def dbConnect(db_path):
        db = sqlite3.connect(db_path)

        return db


def dbExecute(db, query):
        #May need a way to check that the query is valid
        c = db.cursor()
        c.execute(query)

        return c


def makeTable(rows):
        def makeRow(row):
                return ''.join(['<tr>\n', ''.join(['  <td>%s</td>\n' % str(col) for col in row]), '</tr>\n'])

        header = ''.join(['<th>%s</th>\n' % (field[0]) for field in rows.description])
        output = ''.join([makeRow(row) for row in rows.fetchall()])
        return "%s%s" %(header, output)

if __name__ == "__main__":
        if len(sys.argv) >= 2:
                DB_PATH = sys.argv[1];
        else:
                print("No sqlite database specified.")
                exit(1)

        db = dbConnect(DB_PATH)
        if(not db):
                print("Error opening database")
                exit(1);

        print(runPage(db, ''.join(sys.stdin)))

