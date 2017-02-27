#!/bin/bash
################################################################################
# @Title: install_neovim.sh
#
# @Author: Phil Smith
#
# @Date: Mon, 27-Feb-17 05:39AM
#
# @Project:
#
# @Purpose:
#
#
################################################################################

# Add software properties to be able to use add-apt-repository
sudo apt-get install software-properties-common

# Install neovim from the neovim PPA
sudo add-apt-repository ppa:neovim-ppa/stable
sudo apt-get update
sudo apt-get install -y neovim

# Install the python dependencies
sudo apt-get install -y python-dev python-pip python3-dev python3-pip

# Install the python modules for neovim
sudo pip2 install --upgrade setuptools
sudo pip3 install --upgrade setuptools
sudo pip2 install --upgrade neovim
sudo pip3 install --upgrade neovim

# Install dein_vim to manage plugins
cd $HOME
curl https://raw.githubusercontent.com/Shougo/dein.vim/master/bin/installer.sh > $HOME/installer.sh
sh $HOME/installer.sh $HOME/.dein_vim

printf "Run :UpdateRemotePlugins after starting nvim to finish installation\n"
