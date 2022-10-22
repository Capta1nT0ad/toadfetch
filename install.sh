echo -e "\033[34;1m(i) toadfetch Installer, (c) 2022 Capta1nT0ad."
echo "(i) Checking python version..."
PYVER=$(python3 --version | cut --characters=8-14)
SUPPORTEDPYVER="3.9.0"
if [ $? == 0 ];
then
        echo -n ""
else
        echo -e "\033[31;1m(E) It looks like Python is not installed. Please install it through your package manager or <https://python.org>."
        exit
fi
if [ "$(printf '%s\n' "$SUPPORTEDPYVER" "$PYVER" | sort -V | head -n1)" = "$SUPPORTEDPYVER" ]
then
        echo -n ""
else
        echo -e "\033[31;1m(E) It looks like your Python version is too old. toadfetch only supports Python 3.9 or later. Install the latest version through your package manager or get it from <https://python.org>."
        exit
fi
echo -e '\033[34;1m(i) Installing python dependencies...'
echo -e "     - Installing 'command'..."
python3 -m pip install command 1> /dev/null
if [ $? == 0 ];
then
        echo -n ""
else
        echo -e "\033[31;1m(E) 'command' failed to install. Is your internet connection up? Are there any package conflicts?"
        exit
fi
echo "     - Installing 'colorama'..."
python3 -m pip install colorama 1> /dev/null
if [ $? == 0 ];
then
        echo -n ""
else
        echo -e "\033[31;1m(E) 'colorama' failed to install. Is your internet connection up? Are there any package conflicts?"
        exit
fi

echo "(i) We need root (sudo) access to finish installing toadfetch. You might need to enter your password below."
sudo su root -c '
echo "(i) Attempting to install dependency "catimg" if not installed..."
catimg -h 1> /dev/null
if [ $? != 0 ];
then
        pacman -S catimg 2> /dev/null
        if [ $? == 0 ];
        then
                echo -n ""
        else
                echo -e "\033[33;1m(W) Failed to install with pacman, now falling back to apt..."
                apt install catimg 2> /dev/null
                if [ $? == 0 ];
                then
                        echo -n ""
                else
                        echo -e "\033[33;1m(W) Failed to install with apt, now falling back to dnf..."
                        dnf -y install catimg 2> /dev/null
                        if [ $? == 0 ];
                        then
                                echo -n ""
                        else
                                echo -e "\033[31;1m(E) Failed to install with all available, it looks like you will have to install catimg manually. Please clone the catimg repository, go to <https://github.com/posva/catimg#building> and follow the instructions. Now exiting.\033[0m"
                                pkill bash
                        fi
                fi
        fi
fi
echo -e "\033[32;1m(i) catimg was already installed or it installed successfully."
echo -e "\033[34;1m(i) Creating neccessary directories..."
mkdir -p /usr/share/toadfetch/
echo -e "\033[34;1m(i) Downloading toadfetch..."
echo -e -n "\033[31;1m"
git clone --depth=1 https://github.com/Capta1nT0ad/toadfetch /usr/share/toadfetch
if [ $? == 0 ];
        then
                echo -n ""
        else
                echo -e "\033[31;1m(E) Failed to "git clone" the toadfetch GitHub repository. Either git is not installed, it failed for an unknown reason, toadfetch is already installed, or your internet connection is down.\033[0m"
                pkill bash
        fi
echo -e "\033[34;1m(i) Installing toadfetch..."
mkdir -p /usr/bin/
mv /usr/share/toadfetch/toadfetch.py /usr/bin/toadfetch
rm /usr/share/toadfetch/install.sh
'
if [ $? == 0 ]
then
        echo -e "\033[32;1m(i) Done installing toadfetch. Run it with 'toadfetch'."
else
        exit
fi
