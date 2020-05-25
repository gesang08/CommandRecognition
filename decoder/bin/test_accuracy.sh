#!/bin/bash
if [ $# -ne 4 ] ; then
   echo "Usage: $0 <audio_path_dir> <ip> <port> <thread_num> ]";
   echo "这是并行对测试集的准确率进行解码的脚本，可支持中英日韩四种语言"
   echo "e.g.: $0 data/accuracy/zh/test_aishell1 127.0.0.1 9800 10 测试中文测试集 "
   echo "e.g.: $0 data/accuracy/en/test_lib_clean 127.0.0.1 9810 10 测试英文测试集"
   echo "e.g.: $0 data/accuracy/jp/test_jp_part01 127.0.0.1 9820 10 测试日文测试集"
   echo "e.g.: $0 data/accuracy/ko/test_ko_part01 127.0.0.1 9830 10 测试韩文测试集"
   exit 1;
fi

dir=$1
ip=$2
port=$3
thread_num=$4
test=`basename $dir`
export LD_LIBRARY_PATH=./lib:$LD_LIBRARY_PATH
find $dir -iname '*.wav' >$dir/../${test}.scp  # 查找目录$dir下（包括子目录）所有.wav文件
python bin/asr_decoder_client.py $ip $port $thread_num < $dir/../${test}.scp 
