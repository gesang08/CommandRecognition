#!/bin/sh

# 两个文件一行行对比，输出相同的行内容

file1=$1
file2=$2

cat $file1 | while read lineb
do
    cat $file2 | while read linea
        do
            if [ "$lineb" = "$linea" ];then
                echo $lineb >>11
            fi
        done
done
#for i in `cat $file1`;do
#    for j in `cat $file2`;do
#        if [ "$i" = "$j" ];then
#            echo $i
#        fi
#    done
#done

#for i in $(cat $file1);do
#    grep "\<$i\>" $file2
#done
