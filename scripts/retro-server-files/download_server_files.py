#!/usr/bin/env python

import sys
import urllib
import os


if len(sys.argv) != 1:
  print 'Incorrect number of arguments!'
  quit()

swf_tree = 'file_list'
dest_folder = './dofus'
prefix = 'http://dofusretro.cdn.ankama.com/'

print 'Download files from server: ', prefix;
print 'Storing files in local server: ', dest_folder;

swf_download = urllib.URLopener()

with open(swf_tree) as f:
  for line in f:
    filename = line.rstrip()
    if filename.split('/')[-1] != 'versions.swf':
        retro_filename = filename.replace(filename.split('.')[0].split('_')[-1], '1011')
    else:
        retro_filename = filename
    file_url = prefix + retro_filename
    save_file = dest_folder + '/' + retro_filename
    if ( not os.path.isfile(save_file) ):
      print file_url + ' ==> ' + save_file
      swf_download.retrieve(file_url, save_file)
    else:
      print save_file + ' already exists.'

