'''
Created on 16 Sep 2011

@author: cgueret
'''
import os
import sys
sys.path.append(os.path.join(os.path.expanduser('~'), 'Code/SemanticXO/datastore/src'))
sys.path.append(os.path.join(os.path.expanduser('~'), 'Code/SemanticXO/common/src'))

from sugar import util
from semanticxo.datastore import TripleStore
import lipsum
import random
import uuid
import gc
import time 
from datetime import datetime

import subprocess

# http://build.laptop.org/11.3.0/os5/xo-1/os5.ACTIVITIES.txt
ACTIVITIES = ["Abacus","Browse","Calculate","Chat","Clock","Distance","Etoys",
"FotoToon","HelloWorld","Help","ImageViewer","Implode","Jukebox","Log",
"Maze","Measure","Memorize","Moon","Paint","Pippy","Read","Record","Ruler",
"Scratch","Speak","TamTamEdit","TamTamJam","TamTamMini","TamTamSynthLab","Terminal",
"TurtleArt","Write"]
generator = lipsum.Generator()
tags = open('lipsum/data/dictionary.txt').readlines()

# On the XO
#DIR = "/var/lib/redstore"
#CMD = "LD_LIBRARY_PATH=/opt/redstore:$LD_LIBRARY_PATH /opt/redstore/redstore"

# On the PC
CMD = "redstore"
DIR = "/tmp/redstore"

def generate_journal_entry(store):
    # Basic data
    #entry = datastore.create()
    metadata={}
    metadata['uid'] = str(uuid.uuid4())
    metadata['mtime'] = datetime.now().isoformat()
    metadata['timestamp'] = int(time.time())
    
    # Extra attributes
    activity = ACTIVITIES[random.randint(0,len(ACTIVITIES)-1)]
    tag_set = set([tags[random.randint(0, len(tags)-1)][:-1] for i in range(0, random.randint(0, 10))])
    metadata['title'] = '%s Activity' % activity
    metadata['activity'] = 'org.laptop.%s' % activity
    metadata['mime_type'] = 'text/plain'
    metadata['description'] = generator.generate_paragraph()
    metadata['tags'] = ", ".join(tag_set)
    metadata['title_set_by_user'] = '1'
    metadata['icon-color'] = '#00588C,#00A0FF'
    metadata['activity_id'] = util.unique_id(uuid.getnode())
    metadata['share-scope'] = 'private'

    # Store the entry    
    #datastore.write(entry)
    store.store_object(metadata['uid'], metadata)
    
    return metadata['uid']

if __name__ == '__main__':
    store = TripleStore()
    gc.disable()
    for file in ['output-time-write.csv', 'output-time-read.csv', 'output-space.csv']:
        if os.path.exists(file):
            os.unlink(file)
    file_time_write = open('output-time-write.csv', 'a')
    file_time_read = open('output-time-read.csv', 'a')
    file_space = open('output-space.csv', 'a')
    for run in range(0,10):
        print "Start store"
        os.system("rm -f %s/*" % DIR)
        p = subprocess.Popen("%s -s hashes -t \"hash-type='bdb',dir='%s'\"" % (CMD, DIR), stdout=None, shell=True)
        time.sleep(1)
        for i in range(0, 2000):
            #os.system('sync')
            
            # Record an entry (monitor time)
            start = time.time()
            uid = generate_journal_entry(store)
            file_time_write.write('%.4f,' % (time.time() - start))
            
            # Try to retrieve the same entry (monitor time)
            start = time.time()
            data = store.get_object(uid, None)
            file_time_read.write('%.4f,' % (time.time() - start))
            
            # Save the space used
            p2 = subprocess.Popen("du -s %s | cut -f1" % DIR, shell=True, stdout=subprocess.PIPE)
            out = p2.stdout.read().strip()
            file_space.write('%s,' % out)
        print "Write run %d results" % run
        file_time_write.write("\n")
        file_time_read.write("\n")
        file_space.write("\n")
        p.terminate()
        sts = os.waitpid(p.pid, 0)[1]
    file_time_write.close()
    file_time_read.close()
    file_space.close()
    print "End"
    