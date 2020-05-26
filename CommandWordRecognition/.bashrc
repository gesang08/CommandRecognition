# .bashrc

# Source global definitions
if [ -f /etc/bashrc ]; then
	. /etc/bashrc
fi
export PATH=$PATH:~/tree-1.8.0/treeInstall/bin/
# add env var by gs 202003

if true; then
kaldi=~/kaldi.2020.01.17
export PATH=$PATH:$kaldi/egs/CommandWordRecognition_hmm/s5/hw-ofst/bin
export PATH=$PATH:$kaldi/tools/openfst/bin
export PATH=$PATH:$kaldi/tools/thrax/bin
export PATH=$kaldi/tools/python:$PATH

export PATH=$PATH:/home/sanghongbao/git-lfs-linux-amd64-v2.11.0/lfs/bin
# Uncomment the following line if you don't like systemctl's auto-paging feature:
# export SYSTEMD_PAGER=


# User specific aliases and functions
FST=/home/sanghongbao/kaldi.2020.01.17/tools/openfst-install
# added by Anaconda3 4.2.0 installer
#export PATH="/home/sanghongbao/anaconda3/bin:$PATH"
#export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:/home/sanghongbao/env_tacotron/lib/libstdc++.so.6"
export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:$FST/lib:$FST/lib/fst"
export CPATH=$FST/include:$CPATH
export CXXFLAGS="-I$FST/include -L$FST/lib -L$FST/lib/fst $CXXFLAGS"
fi
export LANG=en_US.UTF-8
