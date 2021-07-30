#!/bin/bash

echo "            ooooooooo                                       ooooooooo           "
echo "            M                                                       M           "
echo "            M                                                       M           "
echo "            M                                                       M           "
echo "            M                                                       M           "
echo "                                     oooooooo                                   "
echo "                                ooMMMMMMMMMMMMMoo                               "
echo "                             ooMMMMMMMMMMMMMMMMMMMo                             "
echo "                            oMMMMMMMMMMMMMMMMMMMMMMMo                           "
echo "                           MMMMMMMMMMMMMMMMMMMMMMMMMMo                          "
echo "                          MMMMMMMMMMMMMMMMMMMMMMMMMMMM                       oo "
echo "                         oMMMMMMMMMMMMMMMMMMMMMMMMMMMMo                     oM  "
echo "                         oMMMMMMMMMMMMMMMMMMMMMMMMMMMMM                    Mo   "
echo "                         oMMMMMMMMMMMMMMMMMMMMMMMMMMMMM        ooo    ooooMo    "
echo "                         oMMMMMMMMMMMMMMMMMMMMMMMMMMMMo       o         oMo     "
echo "                          oMMMMMMMMMMMMMMMMMMMMMMMMMMM       oMo      oMo o     "
echo "                           MMMMMMMMMMMMMMMMMMMMMMMMMMo       o  oMo  oM   o     "
echo "                            oMMMMMMMMMMMMMMMMMMMMMMo          o   ooMo   oo     "
echo "                              oMMMMMMMMMMMMMMMMMMoo            oo       oo      "
echo "                                ooMMMMMMMMMMMMoo                 oooooo         "
echo "                           ooMoo     oooooo      oMMoo                          "
echo "                        oMMMMMMMMooo         ooMMMMMMMMMo                       "
echo "                     oMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMo                     "
echo "                   oMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMo                   "
echo "            M     MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMo     M           "
echo "            M   oMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMo   M           "
echo "            M  oMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMo  M           "
echo "            M                                                       M           "
echo "            ooooooooo            Smart Absence              ooooooooo           "
echo ""
echo "            MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMo           "
echo "            MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMo           "
echo "            MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMo           "
echo "            oMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM            "
echo "             oMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMo             "
echo "               ooMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMoo              "
echo "                  ooMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMoo                  "
echo "                      oooMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMoo                      "
echo "                            ooooMMMMMMMMMMMMMMMMMoooo                           "
echo ""
echo ""

echo "[+] Installing dependencies :"
apt update && apt upgrade
apt -y install python3 idle3 python3-dev
apt -y install build-essential cmake pkg-config libjpeg-dev libtiff5-dev libjasper-dev libpng12-dev 
apt -y install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
apt -y install libxvidcore-dev libx264-dev
apt -y install libgtk2.0-dev libgtk-3-dev
apt -y install libatlas-base-dev gfortran
wget https://bootstrap.pypa.io/get-pip.py
sudo python3 get-pip.py
python3 -m pip install opencv-contrib-python==4.5.1.48
#python3 -m pip install "picamera[array]"
python3 -m pip install dlib face_recognition imutils pyqt5 pysqlite3 pickle numpy pil logging pathlib
echo "[+] Installing Smart Absence :"
mkdir -p /opt/Smart_Absence/Models
mkdir -p /opt/Smart_Absence/Data
mkdir -p /opt/Smart_Absence/Dataset
mkdir -p /opt/Smart_Absence/Database
mkdir -p /opt/Smart_Absence/icons
chmod 777 /opt/Smart_Absence/*
mv DAO.py View.py Models.py db_create.py /opt/Smart_Absence
mv Models/* /opt/Smart_Absence/Models/
chmod 777 /opt/Smart_Absence/Models/*
mv Database/* /opt/Smart_Absence/Database/
chmod 777 /opt/Smart_Absence/Database/*
mv icons/* /opt/Smart_Absence/icons/
chmod 777 /opt/Smart_Absence/icons/*
rm -r Models
rm -r Database
rm -r icons
echo "[+] Creating Database :"
python3 /opt/Smart_Absence/db_create.py