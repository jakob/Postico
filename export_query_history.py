#!/usr/bin/python

#
# This python script lets you export all queries from Postico's query history
# 
# Use a command like the following to all queries to a file:
# PYTHONIOENCODING=UTF-8 ./export_query_history.py >query_history.sql
#

import sqlite3
import zlib
import os
import sys

if (sys.stdout.encoding is None):
    print >> sys.stderr, "No encoding specified. Please set PYTHONIOENCODING=UTF-8"
    exit(1)

con = sqlite3.connect(os.environ["HOME"] + '/Library/Containers/at.eggerapps.Postico/Data/Library/Application Support/Postico/ConnectionFavorites.db')

cur = con.cursor()    
cur.execute("""
    select f."ZNICKNAME"
      ,datetime(h."ZDATE" + strftime('%s', '2001-01-01 00:00:00'), 'unixepoch', 'localtime') as date
      ,h."ZTEXT"
      ,h."ZCOMPRESSEDTEXT"
    from "ZPGEQUERYHISTORYELEMENT" h
    join "ZPGEFAVORITE" f on h."ZFAVORITE" = f."Z_PK"
    order by ZDATE DESC
    """)

for row in cur: 
    nickname = row[0]
    date = row[1]
    if row[2]:
        sql = row[2]
    elif row[3]:
        sql = zlib.decompress(row[3]).decode('utf-8')
    else:
        sql = None
        
    print "/**\n * Connection: %s\n * Date: %s\n */\n%s\n\n" % (nickname, date, sql)

con.close()