#!/bin/bash

log=$1
ref=$2
export LD_LIBRARY_PATH=./lib:$LD_LIBRARY_PATH
if [ ! -d ${log}_result ]; then
  mkdir ${log}_result
fi
cp $log ${log}_result/hyp
cp $ref ${log}_result/reference
#cat ${log}_result/hyp |cut -f 2 |awk -F '/' '{print $NF}'|cut -c 7-|sed 's/\.wav//g' >${log}_result/hyp_uttid
#cat ${log}_result/hyp |cut -f 1 |awk -F '/' '{print $NF}'|sed 's/\.wav//g' >${log}_result/hyp_uttid
cat ${log}_result/hyp |cut -f 1 |awk -F '/' '{print $NF}'|sed 's/\.wav//g'|cut -c 5- |sed 's/S/_a_S/g' >${log}_result/hyp_uttid
#cat ${log}_result/hyp |cut -f 1 |awk -F '/' '{print $NF}'|sed 's/\.wav//g'|sed 's/IC/C/g' |sed 's/BAC009//g' >${log}_result/hyp_uttid
cat ${log}_result/hyp |cut -f 2- |python bin/remove_punctuation_without_space.py |perl bin/zh-char-seg.pl >${log}_result/hyp_sentence_char
paste -d ' ' ${log}_result/hyp_uttid ${log}_result/hyp_sentence_char |tr -s ' '  |sort -u >${log}_result/hyp_decode
bin/compute-wer ark:${log}_result/reference ark:${log}_result/hyp_decode
