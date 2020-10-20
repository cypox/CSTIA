#!/usr/bin/env python

import sys
import urllib
import os


if len(sys.argv) != 1:
  print 'Incorrect number of arguments!'
  quit()

#note: file_list is obtained using 'find lang/ -type f -name *.swf' in /ver/www/dofus/dofus (old server website)
swf_tree = 'file_list'
dest_folder = './dofus'
prefix = 'http://dofusretro.cdn.ankama.com/'

print 'Download files from server: ', prefix;
print 'Storing files in local server: ', dest_folder;

swf_download = urllib.URLopener()

with open(swf_tree) as f:
  for line in f:
    filename = line.rstrip()
    if 'Tuto' in filename or filename.split('.')[-1] == 'bu2' or filename.split('.')[-1] == 'html' or filename.split('.')[-1] == 'bu':
      continue
    version = filename.split('.')[0].split('_')[-1]
    if version.isdigit():
      filename = filename.replace(version, '1011')
    file_url = prefix + filename
    save_file = dest_folder + '/' + filename
    if ( not os.path.isfile(save_file) ):
      print file_url + ' ==> ' + save_file
      swf_download.retrieve(file_url, save_file)
    else:
      print save_file + ' already exists.'

