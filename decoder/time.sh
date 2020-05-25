#!/bin/bash

# 测试解码时间

dir=$1
lang=$2

starttime=`date +'%Y-%m-%d %H:%M:%S'`
sh test.sh $dir $lang >decodeRes.log
endtime=`date +'%Y-%m-%d %H:%M:%S'`
start_seconds=$(date --date="$starttime" +%s);
end_seconds=$(date --date="$endtime" +%s);
echo "$dir本次运行时间： "$((end_seconds-start_seconds))"s" >>run_time  # 程序执行时间秒数

python3 reslove.py decodeRes.log $dir text755
