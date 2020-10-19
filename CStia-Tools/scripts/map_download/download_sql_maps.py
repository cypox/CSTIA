#!/usr/bin/env python

import sys
import urllib2
import os


if len(sys.argv) != 4:
  print 'Incorrect number of arguments!'
  quit()

map_file = sys.argv[1]
dest_folder = sys.argv[2]
prefix = sys.argv[3]

print 'Using map file: ', map_file;

with open(map_file) as f:
  for line in f:
    fields = line.rstrip()
    fields = fields.split(',')
    map_id = fields[0][1:-1]
    map_date = fields[1][1:-1]
    swf_name = map_id + '_' + map_date + '.swf'
    save_file = '/var/www/' + dest_folder + '/dofus/maps/' + swf_name
    file_url = prefix + '/dofus/maps/' + swf_name
    if ( not os.path.isfile(save_file) ):
      try:
        ret = urllib2.urlopen(file_url)
        with open(save_file, "w") as f:
          f.write(ret.read())
          print file_url + ' ==> ' + save_file
      except urllib2.HTTPError:
        swf_name = map_id + '_' + map_date + 'X.swf'
        file_url = prefix + '/dofus/maps/' + swf_name
        save_file = '/var/www/' + dest_folder + '/dofus/maps/' + swf_name
        if ( not os.path.isfile(save_file) ):
          try:
            ret = urllib2.urlopen(file_url)
            with open(save_file, "w") as f:
              f.write(ret.read())
              print file_url + ' ==> ' + save_file
          except urllib2.HTTPError:
            print 'File ' + swf_name + ' not found on remote repository.'
            continue
        else:
          print 'File ' + swf_name + ' already exists in local repository.'
    else:
      print 'File ' + swf_name + ' already exists in local repository.'

