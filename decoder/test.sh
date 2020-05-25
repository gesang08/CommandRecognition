#!/bin/bash
dir=$1
lang=$2
export LD_LIBRARY_PATH=./lib:$LD_LIBRARY_PATH

function timediff() {

    # time format:date +"%s.%N", such as 1502758855.907197692
        start_time=$1
        end_time=$2
                
        start_s=${start_time%.*}
        start_nanos=${start_time#*.}
        end_s=${end_time%.*}
        end_nanos=${end_time#*.}
                
        if [ "$end_nanos" -lt "$start_nanos" ];then
            end_s=$(( 10#$end_s - 1 ))
            end_nanos=$(( 10#$end_nanos + 10**9 ))
        fi
                                            
        time=$(( 10#$end_s - 10#$start_s )).`printf "%03d\n" $(( (10#$end_nanos - 10#$start_nanos)/10**6 ))`
        echo $time
}

case $lang in
    "zh")
    if [ -e rtf ];then
        cp rtf rtf_bak
        rm rtf
    fi
    for i in $dir/*.wav
    do
        wav_length=`sox $i -n stat 2>&1 | sed -n 's#^Length (seconds):[^0-9]*\([0-9.]*\)$#\1#p'`
        # start_time=`date --date='0 days ago' "+%Y-%m-%d %H:%M:%S"`  # 时间单位：秒级别
        start_time=$(date +"%s.%N") # 时间单位：毫秒级
        ./bin/asr_decoder_client --input_file $i --ip 127.0.0.1 --port 9800 --chunk_size 0.24 --format wav 
        # finish_time=`date --date='0 days ago' "+%Y-%m-%d %H:%M:%S"`
        finish_time=$(date +"%s.%N")
        # duration=$(($(($(date +%s -d "$finish_time")-$(date +%s -d "$start_time")))))
        duration=`timediff $start_time $finish_time`
        rtf_result=`echo $duration | awk '{printf "%.2f\n",('$duration'/'$wav_length')}'`
        echo "$i $duration $wav_length $rtf_result" >>rtf
    done
    echo "test recognition client for zh"
    ;;
    "en")
    for i in $dir/*.wav
    do
    ./bin/asr_decoder_client --input_file $i --ip 127.0.0.1 --port 9810 --chunk_size 0.24 --format wav
    done
    echo "test recognition client for en"
    ;;
    "jp")
    for i in $dir/*.wav
    do
    ./bin/asr_decoder_client --input_file $i --ip 127.0.0.1 --port 9820 --chunk_size 0.24 --format wav
    done
    echo "test recognition client for jp"
    ;;
    "ko")
    for i in $dir/*.wav
    do
    ./bin/asr_decoder_client --input_file $i --ip 127.0.0.1 --port 9830 --chunk_size 0.24 --format wav
    done
    echo "test recognition client for ko"
    ;;
    *)
   echo "you need choose one language model to test~"
    ;;
esac


