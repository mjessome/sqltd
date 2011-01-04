#!/usr/bin/env python

import sqlite3
import sys
import re

def runPage(db, html):
        query = False
        split = re.split('(<sql>|</sql>)', html)

        for s in split:
                if s == '<sql>':
                        query = True
                elif s == '</sql>':
                        query = False
                elif query:
                        result = dbExecute(db, s).fetchall()
                        print makeTable(result),
                else:
                        print s,
        
        return output


def dbConnect(db_path):
        db = sqlite3.connect(db_path)

        return db


def dbExecute(db, query):
        #May need a way to check that the query is valid
        c = db.cursor()
        c.execute(query)

        return c

if __name__ == "__main__":
        if len(sys.argv) >= 2:
                DB_PATH = sys.argv[1];
        else:
                print "No sqlite database specified."
                exit(1)

        db = dbConnect(DB_PATH)
        if(not db):
                print "Error opening database"
                exit(1);

        print runPage(db, ''.join(sys.stdin))

