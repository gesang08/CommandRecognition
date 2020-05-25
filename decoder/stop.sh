lang=$1

case $lang in
    "zh")
    ps aux | grep 'asr_decoder_server' |grep 'zh' | perl -ne "@s=split /\s+/;print \"\$s[1]\n\";" | xargs kill -9
    ;;
    "en")
    ps aux | grep 'asr_decoder_server' |grep 'en' | perl -ne "@s=split /\s+/;print \"\$s[1]\n\";" | xargs kill -9
    ;;
    "jp")
    ps aux | grep 'asr_decoder_server' |grep 'jp' | perl -ne "@s=split /\s+/;print \"\$s[1]\n\";" | xargs kill -9
    ;;
    "ko")
    ps aux | grep 'asr_decoder_server' |grep 'ko' | perl -ne "@s=split /\s+/;print \"\$s[1]\n\";" | xargs kill -9
    ;;
    "all")
    ps aux | grep 'asr_decoder_server' |grep -E 'zh|en|jp|ko' | perl -ne "@s=split /\s+/;print \"\$s[1]\n\";" | xargs kill -9
    ;;
    *)
    echo "you need choose the language~"
    ;;
esac
