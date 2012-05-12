#!/bin/bash

VIRTUALENV_PATH=virtualenv

EASYINSTALL_INSTALLED=`which easy_install`
if [ "$EASYINSTALL_INSTALLED" == "" ]; then
    echo -e "easy_install NOT found."
    exit 1
fi

PIP_INSTALLED=`which pip`
if [ "$PIP_INSTALLED" == "" ]; then
    echo -e "pip NOT found, run sudo easy_install pip"
    exit 1
fi

VIRTUALENV_INSTALLED=`which virtualenv`
if [ "$VIRTUALENV_INSTALLED" == "" ]; then
    echo -e "virtualenv NOT found, run sudo easy_install virtualenv"
    exit 1
fi

if [ -f $VIRTUALENV_PATH/requirements.txt ]; then
    if diff $VIRTUALENV_PATH/requirements.txt requirements.txt | grep -q ^\<; then
        rm -rf $VIRTUALENV_PATH
    fi
fi

if [ "$PIP_DOWNLOAD_CACHE" == "" ]; then
    export PIP_DOWNLOAD_CACHE="~/.pip_download_cache"
fi

EXISTING_ENV=$VIRTUAL_ENV
virtualenv --no-site-packages $VIRTUALENV_PATH

cat >> $VIRTUALENV_PATH/bin/activate <<EOF

if [ -z "\$VIRTUAL_ENV_DISABLE_PROMPT" ]; then
    export PS1="(\$(basename \$(dirname \"\$VIRTUAL_ENV\")))\$_OLD_VIRTUAL_PS1"
fi
EOF

source $VIRTUALENV_PATH/bin/activate

pip install -r requirements.txt
OUT=$?
if [ $OUT -ne 0 ];then
   echo -e "Requirements installation failed!"
   exit 1
fi

cp requirements.txt $VIRTUALENV_PATH

if [ "$EXISTING_ENV" == "" ]; then
    echo "Run \"source $VIRTUALENV_PATH/bin/activate\" to activate this virtualenv."
fi
