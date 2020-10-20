#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

import sys
import os
import mysql.connector


cnx = mysql.connector.connect(user='root',database='cstia_game',host='localhost',password='Dexath')
cursor = cnx.cursor()

query = "SELECT id,name FROM item_template WHERE type = 85"
cursor.execute(query)
names = cursor.fetchall()

for i in xrange(len(names)):
  #print names[i][0]
  row_id = names[i][0]
  row_name = names[i][1]

  if "Gemme Spirituelle de " not in row_name:
    continue

  boss_name = row_name.replace("Gemme Spirituelle de ", "")

  query = 'SELECT id FROM monsters WHERE name LIKE "' + boss_name + '%"'
  #print query
  cursor.execute(str(query))
  boss_id_list = cursor.fetchall()
  boss_id = boss_id_list[0][0]
  print boss_name + ' (' + str(boss_id) + ') :'
  query = 'SELECT groupData FROM mobgroups_fix WHERE groupData LIKE "%' + str(boss_id) + ',%"'
  #print query
  cursor.execute(query)
  group_data_list = cursor.fetchall()
  group_data = ""
  if len(group_data_list) == 1:
    group_data = group_data_list[0][0]
  else:
    for row in xrange(len(group_data_list)):
      curr_groupe = group_data_list[row][0]
      mobs = curr_groupe.split(';')
      for mob in mobs:
        curr_mob = mob.split(',')
        if curr_mob[0] == str(boss_id):
          group_data = curr_groupe
  #if group_data == "":
    #group_data = group_data_list
  #print group_data

  query = 'UPDATE item_template SET statsTemplate = "' + str(group_data) + '" WHERE id = ' + str(row_id)
  print query
  cursor.execute(query)

cnx.commit()
cnx.close()

