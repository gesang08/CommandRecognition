# .bash_profile

# Get the aliases and functions
if [ -f ~/.bashrc ]; then
	. ~/.bashrc
fi
export TIME_STYLE='+%Y-%m-%d %H:%M:%S'
# User specific environment and startup programs

PATH=$PATH:$HOME/.local/bin:$HOME/bin
decoderlib=~/decoder/lib

export PATH

#export LD_LIBRARY_PATH=$decoderlib:~/env_tacotron/lib/:/lib:/lib64:/usr/lib:/usr/lib64:/usr/local/lib:/usr/local/lib64
export LD_LIBRARY_PATH=~/env_tacotron/lib/:/lib:/lib64:/usr/lib:/usr/lib64:/usr/local/lib:/usr/local/lib64
