#!/usr/bin/env python

import sys
import urllib
import os


if len(sys.argv) != 4:
  print 'Incorrect number of arguments!'
  quit()

map_file = sys.argv[1]
dest_folder = sys.argv[2]
prefix = sys.argv[3]

print 'Using map file: ', map_file;
print 'Download files from server: ', prefix;
print 'Storing files in local server: ', dest_folder;

swf_download = urllib.URLopener()

with open(map_file) as f:
  for line in f:
    filename = line.rstrip()
    file_url = prefix + '/dofus/maps/' + filename
    save_file = '/var/www/' + dest_folder + '/dofus/maps/' + filename
    if ( not os.path.isfile(save_file) ):
      print file_url + ' ==> ' + save_file
      swf_download.retrieve(file_url, save_file)
    else:
      print save_file + ' already exists.'


