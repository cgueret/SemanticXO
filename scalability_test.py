'''
Created on 16 Sep 2011

@author: cgueret
'''
import sys
sys.path.append('/home/cgueret/Code/semanticXO')

from sugar.datastore import datastore
from sugar import util
import lipsum
import random
import uuid
import gc
import time 

# http://build.laptop.org/11.3.0/os5/xo-1/os5.activities.txt
activities = ["Abacus","Browse","Calculate","Chat","Clock","Distance","Etoys",
"FotoToon","HelloWorld","Help","ImageViewer","Implode","Jukebox","Log",
"Maze","Measure","Memorize","Moon","Paint","Pippy","Read","Record","Ruler",
"Scratch","Speak","TamTamEdit","TamTamJam","TamTamMini","TamTamSynthLab","Terminal",
"TurtleArt","Write"]
generator = lipsum.Generator()
tags = open('lipsum/data/dictionary.txt').readlines()

def generate_journal_entry():
    entry = datastore.create()
    activity = activities[random.randint(0,len(activities)-1)]
    tag_set = set([tags[random.randint(0, len(tags)-1)][:-1] for i in range(0, random.randint(0, 10))])
    entry.metadata['title'] = '%s Activity' % activity
    entry.metadata['activity'] = 'org.laptop.%s' % activity
    entry.metadata['mime_type'] = 'text/plain'
    entry.metadata['description'] = generator.generate_paragraph()
    entry.metadata['tags'] = ", ".join(tag_set)
    entry.metadata['title_set_by_user'] = '1'
    entry.metadata['icon-color'] = '#00588C,#00A0FF'
    entry.metadata['activity_id'] = util.unique_id(uuid.getnode())
    entry.metadata['share-scope'] = 'private'
    datastore.write(entry)
    
if __name__ == '__main__':
    gc.disable()
    for i in range(0, 50):
        start = time.time()
        generate_journal_entry()
        end = time.time()
        print '%d -> time %.6f seconds' % (i, end - start)
