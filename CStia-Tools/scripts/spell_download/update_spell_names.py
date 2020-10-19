#!/usr/bin/env python

import sys
import os
import mysql.connector


if len(sys.argv) != 2:
  print 'Incorrect number of arguments!'
  quit()

spell_file = sys.argv[1]

cnx = mysql.connector.connect(user='root',database='cstia_game',host='localhost',password='Dexath')
cursor = cnx.cursor()


print 'Using spell file: ', spell_file;

with open(spell_file) as f:
  for line_r in f:
    line = line_r.rstrip()
    spell_id = line.split('=')[0][2:-2]
    spell_str = line.split('=')[1][1:-1]
    spell_str = spell_str.split(',')
    spell_name = spell_str[0].split(':')[1][1:-1]
    if spell_name != "" and len(spell_name) > 4:
      query = 'UPDATE sorts SET nom = \'' + spell_name + '\' WHERE id = ' + spell_id
      print query
      cursor.execute(query)

cnx.commit()
cnx.close()

