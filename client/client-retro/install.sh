#!/bin/bash

menu(){
    echo "Veuillez choisir une option"
    echo "1: Installation"
    echo "2: Mise à jour"
    echo "3: Quitter"

    read choice

    case $choice in
        1)
            selection;;
        2)
            update;;
        3)
            exit;;
        *)
            menu;;
    esac
}

menu-distrib(){
    echo "Quelle distribution :"
    echo "1) Ubuntu"
    echo "2) Debian"
    echo "3) Quitter"
    read type_distrib
}

menu-version-ubuntu(){
    echo "Quelle version de la distribution :"
    echo "1) 16.04"
    echo "2) 18.04"
    echo "3) 19.10 ou 20.04"
    read version
}

menu-version-debian(){
    echo "Quelle version de la distribution :"
    echo "1) 9"
    echo "2) 10"
    read version
}
#type-distrib(){
#distrib=$(cat /etc/lsb-release | grep DISTRIB_ID | cut -c 12-)
#version=$(cat /etc/lsb-release | grep DISTRIB_RELEASE | cut -c 17-)
#}

dl-wine(){
    mkdir -p dofus-installer
    cd dofus-installer
    wget https://download.ankama.com/launcher/full/linux/x64
    mv x64 Ankama-launcher.appimage
    chmod +x Ankama-launcher.appimage
    sudo mv /opt/dofus-launcher/Dofus.png /usr/share/icons/hicolor/512x512/apps/
    /opt/dofus-launcher/name.sh
    sudo mv /opt/dofus-launcher/dofus.desktop /usr/share/applications/
    ln -sf /usr/share/applications/dofus.desktop ~/Bureau/
    sudo chmod +x ~/Bureau/dofus.desktop
    sudo apt update
    sudo dpkg --add-architecture i386
    wget -qO - https://dl.winehq.org/wine-builds/winehq.key | sudo apt-key add -
    sudo apt update
    sudo apt -y install software-properties-common dirmngr apt-transport-https lsb-release ca-certificates
}

selection(){
#type-distrib
menu-distrib
case $type_distrib in
    1)
        menu-version-ubuntu;;
    2)
        menu-version-debian;;
    *)
        exit;;
esac
case $type_distrib in
    1)
        dl-wine
        case $version in
            1)
                sudo apt-add-repository 'deb https://dl.winehq.org/wine-builds/ubuntu/ xenial main'
                wget -O- -q https://download.opensuse.org/repositories/Emulators:/Wine:/Debian/xUbuntu_16.04/Release.key | sudo apt-key add -
                echo "deb http://download.opensuse.org/repositories/Emulators:/Wine:/Debian/xUbuntu_16.04 ./" | sudo tee /etc/apt/sources.list.d/wine-obs.list
                sudo apt update
                sudo apt install --install-recommends winehq-stable -y
                echo "Lancez le launcher et installez dofus puis revenez pour lancer la partie update"
                exit;;
            2)
                sudo apt-add-repository 'deb https://dl.winehq.org/wine-builds/ubuntu/ bionic main'
                wget -nc https://download.opensuse.org/repositories/Emulators:/Wine:/Debian/xUbuntu_18.04/Release.key
                sudo apt-key add Release.key
                echo "deb http://download.opensuse.org/repositories/Emulators:/Wine:/Debian/xUbuntu_18.04 ./" | sudo tee /etc/apt/sources.list.d/wine-obs.list
                sudo apt update
                sudo apt install --install-recommends winehq-stable -y
                echo "Lancez le launcher et installez dofus puis revenez pour lancer la partie update"
                exit;;
            3)
                sudo apt-add-repository 'deb https://dl.winehq.org/wine-builds/ubuntu/ eoan main'
                sudo apt update
                sudo apt install --install-recommends winehq-stable -y
                echo "Lancez le launcher et installez dofus puis revenez pour lancer la partie update"
                exit;;
            *)
                exit;;

        esac;;
    2)
        dl-wine
        case $version in
            1)
                sudo apt-add-repository https://dl.winehq.org/wine-builds/debian/
                wget -O- -q https://download.opensuse.org/repositories/Emulators:/Wine:/Debian/Debian_9.0/Release.key | sudo apt-key add -
echo "deb http://download.opensuse.org/repositories/Emulators:/Wine:/Debian/Debian_9.0 ./" | sudo tee /etc/apt/sources.list.d/wine-obs.list
                sudo apt update
                sudo apt install --install-recommends winehq-stable -y
                echo "Lancez le launcher et installez dofus puis revenez pour lancer la partie update"
                exit;;
            2)
                sudo apt-add-repository https://dl.winehq.org/wine-builds/debian/
                wget -O- -q https://download.opensuse.org/repositories/Emulators:/Wine:/Debian/Debian_10/Release.key | sudo apt-key add -
echo "deb http://download.opensuse.org/repositories/Emulators:/Wine:/Debian/Debian_10 ./" | sudo tee /etc/apt/sources.list.d/wine-obs.list
                sudo apt update
                sudo apt install --install-recommends winehq-stable -y
                echo "Lancez le launcher et installez dofus puis revenez pour lancer la partie update"
                exit;;
            *)
                exit;;
        esac;;

    *)
        exit;;
esac
}

update(){
    cat /opt/dofus-launcher/start-zaap > ~/.config/Ankama/zaap/dofus/zaap-start.sh
}
menu
