#!/bin/bash
export LD_LIBRARY_PATH=./lib:$LD_LIBRARY_PATH

function doAsr(){
	# 计算音频时长
	wav_length=`./bin/sox $1 -n stat 2>&1 | sed -n 's#^Length (seconds):[^0-9]*\([0-9.]*\)$#\1#p'`
	#wav_length=$wav_length
	# 开始计时
	start_time=`date --date='0 days ago' "+%Y-%m-%d %H:%M:%S"`
	# 请求同传服务
	#./bin/transcriptionClient --addr=$addr --path=$file
        ../bin/asr_decoder_client --input_file $file --ip 127.0.0.1 --port 9800 --chunk_size 0.24 --format wav
	# 结束计时，并计算运行时长
	finish_time=`date --date='0 days ago' "+%Y-%m-%d %H:%M:%S"`
	duration=$(($(($(date +%s -d "$finish_time")-$(date +%s -d "$start_time")))))
	# 计算实时率
	rtf_result=`echo $duration | awk '{printf "%.2f\n",('$duration'/'$wav_length')}'`
	echo $rtf_result >> tmp_file
}

if [ $# -ne 3 ] ; then
	echo "Usage: $0 <wav_path> <thread_num> <address>"
	echo "Exp: $0 data/1.wav 20 localhost:8101"
	exit 1
fi

# file=$1
dir=$1
threads=$2
addr=$3
for file in `find $dir -iname '*.wav'`
do
    touch tmp_file

    for(( i=0;i<${threads};i++))
    do
	doAsr $file $i &
    done

    wait
    echo ${threads}"路并发的实时率如下："
    # 输出实时率的最大值、最小值和平均值
    awk 'BEGIN {min = 65536} {if ($1+0 < min+0) min=$1} END {print "实时率最小值 =", min}' tmp_file
    awk 'BEGIN {max = 0} {if ($1+0 > max+0) max=$1} END {print "实时率最大值 =", max}' tmp_file
    cat tmp_file | awk '{sum+=$1} END {print "实时率平均值 =", sum/NR}'
    rm -rf tmp_file
done
