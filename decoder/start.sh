lang=$1
export LD_LIBRARY_PATH=./lib:$LD_LIBRARY_PATH

case $lang in
    "zh")
    python scripts/install.py $lang
    ./bin/asr_decoder_server -c models/zh/config &
    ;;
    "en")
    python scripts/install.py $lang
    ./bin/asr_decoder_server -c models/en/config &
    ;;
    "en_v3")
    python scripts/install.py $lang
    ./bin/asr_decoder_server -c models/en_v3/config &
    ;;
    "jp")
    python scripts/install.py $lang
    ./bin/asr_decoder_server -c models/jp/config &
    ;;
    "ko")
    python scripts/install.py $lang
    ./bin/asr_decoder_server -c models/ko/config &
    ;;
    "all")
    python scripts/install.py zh
    ./bin/asr_decoder_server -c models/zh/config &
    python scripts/install.py en
    ./bin/asr_decoder_server -c models/en/config &
    python scripts/install.py jp
    ./bin/asr_decoder_server -c models/jp/config &
    python scripts/install.py ko
    ./bin/asr_decoder_server -c models/ko/config &
    ;;
    *)
    echo "you need choose the language~"
    ;;
esac
