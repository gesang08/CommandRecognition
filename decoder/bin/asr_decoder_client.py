#!/root/env python2

import os,sys
import time
import threading
import json

if len(sys.argv) < 4:
    print >>sys.stderr,"%s ip port thread_num < wav.scp > hyp.text"%(__file__)
    sys.exit(1)

ip=sys.argv[1]
port=sys.argv[2]
thread_num=int(sys.argv[3])

input_list=[]
mutex = threading.Lock()
class worker(threading.Thread):
    def __init__(self, tid):
        threading.Thread.__init__(self)
        self._tid=tid
    def run(self):
        i=self._tid
        input_list_len=len(input_list)
        while (i<input_list_len):
            k, line=input_list[i]
            i+=thread_num
            result=""
            root=os.path.dirname(os.path.abspath(__file__))
            #result=os.popen(root + '/asr_decoder_client --ip ' + ip + ' --port ' + port + ' --chunk_size 0.24 --format wav --input_file '+ line)
            mutex.acquire()
            #print str(k.encode('utf-8'))+"\t"+line.encode('utf-8')+"\t"+hyp.encode('utf-8')+"\n"
            print os.popen(root + '/asr_decoder_client --ip ' + ip + ' --port ' + port + ' --chunk_size 0.24 --format wav --input_file '+ line).read()
            mutex.release()

k=0
for line in sys.stdin:
    line=line.strip().replace("\n"," ").replace("\r"," ")
    input_list.append(["%010d"%k,line])
    k+=1
threads=[]
for i in range(thread_num):
    threads.append(worker(i))


start=time.time()
for t in threads:
    t.start()
while threading.active_count() > 1:
    time.sleep(0.1)
finish=time.time()
print >>sys.stderr, "%.lf ms"% ((finish-start)*1000.0/len(input_list))
