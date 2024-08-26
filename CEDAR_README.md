## CedarAlert - YOLOv9 Object and Fire Detection for IP Security Cameras in Python3

This application was developed, tested, and is in use on an Ubuntu 22.04.04 X86_64 desktop PC.

The YOLOv9 code is based upon 'detect_dual.py' and 'yolo9-c.pt' weights from https://github.com/WongKinYiu/yolov9.

The 'yolo9-cfire.pt' weights is from https://github.com/spacewalk01/yolov5-fire-detection.

### Install Libraries

```
sudo apt install -y build-essential libssl-dev libffi-dev python3-dev python3-pip python3-venv

cd ~

mkdir environments

cd environments

python3 -m venv CedarAlert

# activate CedarAlert python environment

~/environments/source/CedarAlert/bin/activate

```

### Install and Verify yolov5-fire-detection (supports YOLOv9 also)

```
cd ~

git clone https://github.com/spacewalk01/yolov5-fire-detection.git

cd yolov5-fire-detection.git

pip install -r requirements.txt

# verify yolov5-fire-detection

```

### Install and Verify YOLOv9

```

cd ~

git clone https://github.com/WongKinYiu/yolov9.git

cd yolov9

pip install -r requirements.txt

# verify

```


