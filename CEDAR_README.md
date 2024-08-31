## CedarAlert - YOLOv9 Object and Fire Detection for IP Security Cameras in Python3

The CedarAlert application was developed, tested, and has been tested on two Ubuntu 22.04.4 X86_64 desktop PCs:
* NUC5i7RYH (approx 10 year old Intel i7 CPU with 16 GB RAM and 500 GB SSD)
* Beelink Mini S12, Intel N100 CPU with 16 GB RAM and 500 GB SSD

The file 'cedar_cars.py' defines variables and creates a JSON object. The values with 'CHANGEME' ***must*** be set (e.g. your SMTP email server domain name 'cedar_email_server').

The YOLOv9 inference code is based upon 'detect_dual.py' and 'yolov9-s-converted.pt' model (weights) from [https://github.com/WongKinYiu/yolov9](https://github.com/WongKinYiu/yolov9).

The 'yolo9-s-fire-converted.pt' model (weights) is based the  [https://github.com/spacewalk01/yolov5-fire-detection]([https://github.com/spacewalk01/yolov5-fire-detection] and was created by from the 'datasets' folder using 'train_dual.py' from [https://github.com/WongKinYiu/yolov9](https://github.com/WongKinYiu/yolov9) in a python env with this command:

'''
# clone this repository
cd ~
git clone https://github.com/audioclassify/CedarAlert.git

# create new python env
cd ~
mkdir -p environments
cd environments
python3 -m venv CedarAlert
source ~/environments/CedarAlert/bin/activate

# CedarAlert is the python env name and the folder name
cd ~/CedarAlert

# install requirements
pip install -r requirements.txt
pip install -r cedar_requirements.txt

# create yolo9-s-fire-converted.pt
python train_dual.py \
--workers 4 \
--device cpu \
--batch 8 \
--data fire/fire.yaml \
--img 640 \
--cfg models/detect/yolov9-s.yaml \
--weights '' \
--name yolov9-s-c-fire \
--hyp hyp.scratch-high.yaml \
--min-items 0 \
--epochs 500 \
--close-mosaic 15
'''

The CedarAlert specific files start with 'cedar_' to distinguish them from files from [https://github.com/WongKinYiu/yolov9](https://github.com/WongKinYiu/yolov9).

The application can optionally write to a log file and also to a SQLite3 database.

User specific variables are defined in 'cedar_config.json', which must be updated for the application to run.

The application runs as a service which starts on boot and restarts on error.

This DIY application is provided as a free open source codebase as a courtesy without any promise of support nor guarantee of any kind.

This software is covered by the [GNU General Public License v3.0](https://github.com/WongKinYiu/yolov9/blob/main/LICENSE.md).


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

# /home/cedar/environments/source/CedarAlert/bin/activate

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


