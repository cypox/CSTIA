#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

import sys
import os
import mysql.connector


if len(sys.argv) != 2:
  print 'Incorrect number of arguments!'
  quit()

panoplis = sys.argv[1]

cnx = mysql.connector.connect(user='root',database='cstia_game',host='localhost',password='Dexath')
cursor = cnx.cursor()

print 'Using item file: ' + panoplis

state = 1
items = []
effects = []

with open(panoplis) as f:
  for line_r in f:
    line = line_r.rstrip()
    if state == 1:
      if 'class="nom">' not in line:
        continue
      
      item_name = line.replace('<th colspan="3" class="nom">', '')[:-5]
      #print item_name
      effects.append(item_name)
      state = 2
      
    elif state == 2:
      if 'class="effet">' not in line:
        continue
      
      effect_list = line.replace('<td colspan="2" class="effet">', '')[:-5]
      for effect in effect_list.split('<br>'):
        #print effect
        effects.append(effect)
      items.append(effects)
      effects = []
      state = 1

for item in items:
  query = "SELECT id FROM item_template WHERE name like \"" + item[0] + "%\""
  #print query
  cursor.execute(query)
  ids = cursor.fetchall()
  item_id = ids[0][0]

  statTemplate = ""

  #print item_id

  for effect in item[1:]:
    eff_type = "fff"
    spell_name = ""
    spell_id = "123"
    val = "0"
    jet = "0d0+"
    
    if "PM" in effect:
      statTemplate += "80#1#0#0#0d0+1"
      continue
      
    elif "Augmente la portée " in effect:
      eff_type = "119"
      spell_name = effect.split('portée du sort ')[1][:-5]
      val = effect.split(' ')[-1]
    
    elif "Rend la portée du sort" in effect:
      eff_type = "11a"
      vals = effect.replace("Rend la portée du sort ", "")
      spell_name = vals.replace(" modifiable", "")
      val = "1"
    
    elif "dommages" in effect:
      eff_type = "11b"
      spell_name = effect.split('sur le sort ')[1]
      val = effect.split(' ')[1]

    elif "soins" in effect:
      eff_type = "11c"
      spell_name = effect.split('sur le sort ')[1]
      val = effect.split(' ')[1]

    elif "en PA" in effect:
      eff_type = "11d"
      spell_name = effect.split('PA du sort ')[1]
      val = effect.split(' ')[2]

    elif "de relance" in effect:
      eff_type = "11e"
      spell_name = effect.split('relance du sort ')[1]
      val = effect.split(" ")[2]

    elif "CC" in effect in effect:
      eff_type = "11f"
      spell_name = effect.split('sur le sort ')[1]
      val = effect.split(' ')[1]

    elif "lancer en ligne" in effect:
      eff_type = "120"
      spell_name = effect.split('ligne du sort ')[1]
      val = "1"

    elif "ligne de vue" in effect:
      eff_type = "121"
      spell_name = effect.split('vue du sort ')[1]
      val = "1"

    elif "max par tour" in effect:
      eff_type = "122"
      spell_name = effect.split('tour du sort ')[1]
      val = "1"

    elif "max par cible" in effect:
      eff_type = "123"
      spell_name = effect.split('cible du sort ')[1]
      val = "1"

    else:
      eff_type = "UNK"
      #continue

    #print '--' + effect + ' ==> ' + eff_type
  
    spell_name = spell_name.replace('"', '')
    query = "SELECT id FROM sorts WHERE nom LIKE \"" + spell_name + "%\""
    #print query
    cursor.execute("SELECT id FROM sorts WHERE nom LIKE \"" + spell_name + "%\"")
    ids = cursor.fetchall()
    spell_id = ids[0][0]

    strTemplate = eff_type + '#' + '{:x}'.format(int(spell_id)) + '#0#' + '{:x}'.format(int(val)) + '#' + jet + str(spell_id)
    statTemplate += ',' + strTemplate
    #print spell_name + ' (' + val + ') == > ' + strTemplate

  if statTemplate[0] == ',':
    statTemplate = statTemplate[1:]
  #print statTemplate
  query = 'UPDATE item_template SET statsTemplate = "' + statTemplate + '" WHERE id = ' + str(item_id) + ''
  print query
  cursor.execute(query)

cnx.commit()
cnx.close()

