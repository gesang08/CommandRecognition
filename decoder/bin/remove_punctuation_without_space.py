#!/usr/bin/env python
#coding:utf-8

# Usage: cat file | python remove_punction.py

import sys
import re
import chardet
from zhon.hanzi import punctuation

r1 = u'[’!"#$%&\'()*+,,-./:;<=>?@，?★、…【】？。！《》“”‘’[\\]^_`{|}~]'

for line in sys.stdin:
   # remove '\n' '\r' '\t' ''
   line = line.strip()
   # to check the encoding
   #print chardet.detect(line) -> utf-8
   # decode line to unicode
   line = line.decode('utf-8')
   # remove all Chinese punctuation
   no_punc_line_c = re.sub(r'[%s]|'%punctuation,'',line)
   no_punc_line = re.sub(r1,'',no_punc_line_c)
   #no_punc_line = re.sub(r1,'',line)
   # encode to utf-8
   no_punc_line = no_punc_line.encode('utf-8')
   # remove ．
   no_punc_line = no_punc_line.replace('．','')
   # remove ""
   no_punc_line = no_punc_line.replace('"','')
   # remove " "
#   no_punc_line = no_punc_line.replace(' ','')
   print no_punc_line

