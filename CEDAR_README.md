## CedarAlert - YOLOv9 Object and Fire Detection for IP Security Cameras in Python3

The CedarAlert application was developed, tested, and is in use on an Ubuntu 22.04.04 X86_64 desktop PC.

The user is 'cedar' and the home path is '/home/cedar'. Your user and home path may likely be different.

The YOLOv9 inference code is based upon 'detect_dual.py' and 'yolo9-c.pt' model (weights) from [https://github.com/WongKinYiu/yolov9](https://github.com/WongKinYiu/yolov9).

The 'yolo9-cfire.pt' model (weights) is from [https://github.com/spacewalk01/yolov5-fire-detection]([https://github.com/spacewalk01/yolov5-fire-detection].

The application can write to a log file and also to a SQLite3 database.

User specific variables are defined in 'cedar_config.json', which must be updated for the application to run.

The application runs as a service which starts on boot and restarts on error.

This DIY application is provided as a free open source codebase as a courtesy without any promise of support nor guarantee of any kind.

This software is covered by the [GNU General Public License v3.0](https://github.com/audioclassify/CedarAlert/LICENSE) .


### Install Libraries and Create CedarAlert Python3 Environment

```

sudo apt install -y build-essential libssl-dev libffi-dev python3-dev python3-pip python3-venv

cd ~

mkdir -p environments

cd environments

python3 -m venv CedarAlert

# activate CedarAlert python environment

~/environments/source/CedarAlert/bin/activate

# use full path for systemd and cron

/home/cedar/environments/source/CedarAlert/bin/activate

```
### Install CedarAlert

```
cd ~

git clone https://github.com/audioclassify/CedarAlert.git

cd CedarAlert

pip install -r requirements.txt # from [https://github.com/WongKinYiu/yolov9](https://github.com/WongKinYiu/yolov9)

pip install -r cedar_requirements.txt # unique to CedarAlert

# verify python and pip version

python -V
# Python 3.10.12

pip -V
# pip 24.2 from /home/cedar/environments/CedarAlert/lib/python3.10/site-packages/pip (python 3.10)

# download yolov9-c-fire.pt from [https://drive.google.com/file/d/1nV5C3dbc_Q3CoczHaERTojr78-SFPdMI/view?usp=sharing](https://drive.google.com/file/d/1nV5C3dbc_Q3CoczHaERTojr78-SFPdMI/view?usp=sharing)

mv ~/Downloads/yolov9-c-fire.pt ~/CedarAlert/yolov9-c-fire.pt

```
### Verify CedarAlert

```
# object detecton with yolov9-c.pt

cd ~/CedarAlert

python cedar_detect_dual.py \
--source "cedar-object-detect-test.jpg" \
--img 640 \
--weights "./yolov9-c.pt" \
--name yolov9_c_640_detect \
--device cpu

# fire detection with yolov9-cfire.pt

python cedar_detect_dual.py \
--source "cedar-fire-detect-test.jpg" \
--img 640 \
--weights "./yolov9-cfire.pt" \
--name yolov9-cfire_640_detect \
--device cpu

```


