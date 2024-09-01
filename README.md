## CedarAlert - DIY YOLOv9 Object and Fire Detection for IP Security Cameras in Python

The purpose of this DIY project is to enhance four low cost outdoor motion detecting security cameras (Amcrest IP4M-1026W) with object and fire detection in a rural high risk fire area, and to provide email alerts with the image in question plus SMS alerts via the Verizon Wireless SMS portal.

Alerts are sent upon recognition of 'fire', 'person', 'bicycle', and 'bear', although the COCO dataset recognizes 80 classes of objects. The alert classes can be changed in the 'run()' code.

All object recognition events and alert conditions are logged in a log file and SQLite3 database by default.

In order to avoid too many alerts in a short period of time, alerts are sent no more frequently that 15 minutes, as defined by 'cedar_alert_seconds'. The Amcrest security cameras have a free Android and iOS app, so the cameras can be viewed in real-time whenever an alert is received.

The four Amcrest cameras are configured to take three photos two seconds apart at each motion event, and send the images via FTP to a local desktop PC for AI analysis and storage.

This DIY application is provided as a free open source codebase as a courtesy without any promise of support nor guarantee of any kind.

This software is covered by the [GNU General Public License v3.0](https://github.com/WongKinYiu/yolov9/blob/main/LICENSE.md) and any other licenses from other open source code referenced.

The CedarAlert application was developed on, and has been tested on, two Ubuntu 22.04.4 X86_64 desktop PCs *without GPUs or TPUs for AI in use* that by today's standard may be considered as low performance:
* Intel NUC5i7RYH (5th generation Intel i7 CPU) with 16 GB RAM and 500 GB SSD
* Beelink Mini S12 (12th generation Intel N100 CPU) with 16 GB RAM and 500 GB SSD (about $160 USD)

The CedarAlert specific files start with 'cedar_' to distinguish them from files from [https://github.com/WongKinYiu/yolov9](https://github.com/WongKinYiu/yolov9) and [https://github.com/spacewalk01/yolov5-fire-detection](https://github.com/spacewalk01/yolov5-fire-detection).

The file 'cedar_vars.py' defines variables and creates a JSON object. The values with 'CHANGEME' ***must*** be set (e.g. your SMTP email server domain name 'cedar_email_server').

The YOLOv9 inference code is based upon 'detect_dual.py' and 'yolov9-s-converted.pt' model (weights) from [https://github.com/WongKinYiu/yolov9](https://github.com/WongKinYiu/yolov9).

The 'yolo9-s-fire-converted.pt' model (weights) is based the [https://github.com/spacewalk01/yolov5-fire-detection](https://github.com/spacewalk01/yolov5-fire-detection) and was created by from the 'datasets' folder using 'train_dual.py' from [https://github.com/WongKinYiu/yolov9](https://github.com/WongKinYiu/yolov9) in a python env with these commands:

```
cd ~
sudo apt update
sudo apt upgrade
sudo apt install -y build-essential libssl-dev libffi-dev python3-dev python3-pip python3-env git

# clone this repository
git clone https://github.com/audioclassify/CedarAlert.git

# create Python environment
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

# check python and pip versions
python -V
# Python 3.10.12

pip -V
# pip 22.0.2 from /home/cedar/environments/CedarAlert/lib/python3.10/site-packages/pip (python 3.10)

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
```
### Verify CedarAlert Object Detecton with yolov9-s-converted.pt (COCO model)

```
(CedarAlert) cedar@NUC5i7RYH:~/CedarAlert$ python cedar_detect_dual.py \
--source "./data/images/horses.jpg" \
--weights "./yolov9-s-converted.pt"

# Output (5 horses, 386.3ms)

YOLO 🚀 1a55998 Python-3.10.12 torch-2.4.0+cu121 CPU

/home/cedar/CedarAlert/models/experimental.py:243: FutureWarning: You are using `torch.load` with `weights_only=False` (the current default value), which uses the default pickle module implicitly. It is possible to construct malicious pickle data which will execute arbitrary code during unpickling (See https://github.com/pytorch/pytorch/blob/main/SECURITY.md#untrusted-models for more details). In a future release, the default value for `weights_only` will be flipped to `True`. This limits the functions that could be executed during unpickling. Arbitrary objects will no longer be allowed to be loaded via this mode unless they are explicitly allowlisted by the user via `torch.serialization.add_safe_globals`. We recommend you start setting `weights_only=True` for any use case where you don't have full control of the loaded file. Please open an issue on GitHub for any issues related to this experimental feature.
  ckpt = torch.load(attempt_download(w), map_location='cpu')  # load
Fusing layers... 
gelan-s summary: 489 layers, 7105888 parameters, 34224 gradients, 26.4 GFLOPs
cedar_detect_dual run() LoadImages OK, source: ./data/images/horses.jpg ===
cedar_log_add() jstr: {"found":"horse", "conf":"0.734", "weights":"./yolov9-s-converted.pt", "source":"./data/images/horses.jpg", "save_path":"runs/detect/CedarAlert355/horses.jpg", "ts":"2024-08-31_10-51-23-083410", "email_ts":"email_none", "sms_ts":"sms_none", "exception": "exception_none"}
log_add() j: {'found': 'horse', 'conf': '0.734', 'weights': './yolov9-s-converted.pt', 'source': './data/images/horses.jpg', 'save_path': 'runs/detect/CedarAlert355/horses.jpg', 'ts': '2024-08-31_10-51-23-083410', 'email_ts': 'email_none', 'sms_ts': 'sms_none', 'exception': 'exception_none'}
log_add() sql: INSERT INTO LOG (fa, name, conf, weights, source, save_path, ts, email_ts, sms_ts, exception) VALUES ('found', 'horse', '0.734', './yolov9-s-converted.pt', './data/images/horses.jpg', 'runs/detect/CedarAlert355/horses.jpg', '2024-08-31_10-51-23-083410', 'email_none', 'sms_none', 'exception_none');
[]
cedar_log_add() jstr: {"found":"horse", "conf":"0.753", "weights":"./yolov9-s-converted.pt", "source":"./data/images/horses.jpg", "save_path":"runs/detect/CedarAlert355/horses.jpg", "ts":"2024-08-31_10-51-23-090671", "email_ts":"email_none", "sms_ts":"sms_none", "exception": "exception_none"}
log_add() j: {'found': 'horse', 'conf': '0.753', 'weights': './yolov9-s-converted.pt', 'source': './data/images/horses.jpg', 'save_path': 'runs/detect/CedarAlert355/horses.jpg', 'ts': '2024-08-31_10-51-23-090671', 'email_ts': 'email_none', 'sms_ts': 'sms_none', 'exception': 'exception_none'}
log_add() sql: INSERT INTO LOG (fa, name, conf, weights, source, save_path, ts, email_ts, sms_ts, exception) VALUES ('found', 'horse', '0.753', './yolov9-s-converted.pt', './data/images/horses.jpg', 'runs/detect/CedarAlert355/horses.jpg', '2024-08-31_10-51-23-090671', 'email_none', 'sms_none', 'exception_none');
[]
cedar_log_add() jstr: {"found":"horse", "conf":"0.875", "weights":"./yolov9-s-converted.pt", "source":"./data/images/horses.jpg", "save_path":"runs/detect/CedarAlert355/horses.jpg", "ts":"2024-08-31_10-51-23-098571", "email_ts":"email_none", "sms_ts":"sms_none", "exception": "exception_none"}
log_add() j: {'found': 'horse', 'conf': '0.875', 'weights': './yolov9-s-converted.pt', 'source': './data/images/horses.jpg', 'save_path': 'runs/detect/CedarAlert355/horses.jpg', 'ts': '2024-08-31_10-51-23-098571', 'email_ts': 'email_none', 'sms_ts': 'sms_none', 'exception': 'exception_none'}
log_add() sql: INSERT INTO LOG (fa, name, conf, weights, source, save_path, ts, email_ts, sms_ts, exception) VALUES ('found', 'horse', '0.875', './yolov9-s-converted.pt', './data/images/horses.jpg', 'runs/detect/CedarAlert355/horses.jpg', '2024-08-31_10-51-23-098571', 'email_none', 'sms_none', 'exception_none');
[]
cedar_log_add() jstr: {"found":"horse", "conf":"0.941", "weights":"./yolov9-s-converted.pt", "source":"./data/images/horses.jpg", "save_path":"runs/detect/CedarAlert355/horses.jpg", "ts":"2024-08-31_10-51-23-103017", "email_ts":"email_none", "sms_ts":"sms_none", "exception": "exception_none"}
log_add() j: {'found': 'horse', 'conf': '0.941', 'weights': './yolov9-s-converted.pt', 'source': './data/images/horses.jpg', 'save_path': 'runs/detect/CedarAlert355/horses.jpg', 'ts': '2024-08-31_10-51-23-103017', 'email_ts': 'email_none', 'sms_ts': 'sms_none', 'exception': 'exception_none'}
log_add() sql: INSERT INTO LOG (fa, name, conf, weights, source, save_path, ts, email_ts, sms_ts, exception) VALUES ('found', 'horse', '0.941', './yolov9-s-converted.pt', './data/images/horses.jpg', 'runs/detect/CedarAlert355/horses.jpg', '2024-08-31_10-51-23-103017', 'email_none', 'sms_none', 'exception_none');
[]
cedar_log_add() jstr: {"found":"horse", "conf":"0.950", "weights":"./yolov9-s-converted.pt", "source":"./data/images/horses.jpg", "save_path":"runs/detect/CedarAlert355/horses.jpg", "ts":"2024-08-31_10-51-23-107553", "email_ts":"email_none", "sms_ts":"sms_none", "exception": "exception_none"}
log_add() j: {'found': 'horse', 'conf': '0.950', 'weights': './yolov9-s-converted.pt', 'source': './data/images/horses.jpg', 'save_path': 'runs/detect/CedarAlert355/horses.jpg', 'ts': '2024-08-31_10-51-23-107553', 'email_ts': 'email_none', 'sms_ts': 'sms_none', 'exception': 'exception_none'}
log_add() sql: INSERT INTO LOG (fa, name, conf, weights, source, save_path, ts, email_ts, sms_ts, exception) VALUES ('found', 'horse', '0.950', './yolov9-s-converted.pt', './data/images/horses.jpg', 'runs/detect/CedarAlert355/horses.jpg', '2024-08-31_10-51-23-107553', 'email_none', 'sms_none', 'exception_none');
[]
save_img, cv2.imwrite(save_path, im0), save_path: runs/detect/CedarAlert355/horses.jpg
image 1/1 /home/cedar/CedarAlert/data/images/horses.jpg: 448x640 5 horses,  386.3ms ./yolov9-s-converted.pt 
Speed: 1.5ms pre-process, 386.3ms inference, 1.2ms NMS per image at shape (1, 3, 640, 640) ./yolov9-s-converted.pt
Results saved to runs/detect/CedarAlert355
```
### Verify CedarAlert Fire Detecton with yolov9-s-fire-converted.pt (Fire model)
```
(CedarAlert) cedar@NUC5i7RYH:~/CedarAlert$ python cedar_detect_dual.py \
--source "./fire/fire/train/images/114.jpg" \
--weights "./fire/yolov9-s-fire-converted.pt"

# Output (11 fires, 349.0ms)

YOLO 🚀 1a55998 Python-3.10.12 torch-2.4.0+cu121 CPU

/home/cedar/CedarAlert/models/experimental.py:243: FutureWarning: You are using `torch.load` with `weights_only=False` (the current default value), which uses the default pickle module implicitly. It is possible to construct malicious pickle data which will execute arbitrary code during unpickling (See https://github.com/pytorch/pytorch/blob/main/SECURITY.md#untrusted-models for more details). In a future release, the default value for `weights_only` will be flipped to `True`. This limits the functions that could be executed during unpickling. Arbitrary objects will no longer be allowed to be loaded via this mode unless they are explicitly allowlisted by the user via `torch.serialization.add_safe_globals`. We recommend you start setting `weights_only=True` for any use case where you don't have full control of the loaded file. Please open an issue on GitHub for any issues related to this experimental feature.
  ckpt = torch.load(attempt_download(w), map_location='cpu')  # load
Fusing layers... 
yolov9-s summary: 658 layers, 9598022 parameters, 0 gradients, 38.7 GFLOPs
cedar_detect_dual run() LoadImages OK, source: ./fire/fire/train/images/114.jpg ===
cedar_log_add() jstr: {"found":"fire", "conf":"0.507", "weights":"./fire/yolov9-s-fire-converted.pt", "source":"./fire/fire/train/images/114.jpg", "save_path":"runs/detect/CedarAlert353/114.jpg", "ts":"2024-08-31_10-47-16-189830", "email_ts":"email_none", "sms_ts":"sms_none", "exception": "exception_none"}
log_add() j: {'found': 'fire', 'conf': '0.507', 'weights': './fire/yolov9-s-fire-converted.pt', 'source': './fire/fire/train/images/114.jpg', 'save_path': 'runs/detect/CedarAlert353/114.jpg', 'ts': '2024-08-31_10-47-16-189830', 'email_ts': 'email_none', 'sms_ts': 'sms_none', 'exception': 'exception_none'}
log_add() sql: INSERT INTO LOG (fa, name, conf, weights, source, save_path, ts, email_ts, sms_ts, exception) VALUES ('found', 'fire', '0.507', './fire/yolov9-s-fire-converted.pt', './fire/fire/train/images/114.jpg', 'runs/detect/CedarAlert353/114.jpg', '2024-08-31_10-47-16-189830', 'email_none', 'sms_none', 'exception_none');
[]
cedar_alert_folder() jstr: {"alert":"fire", "conf":"0.507", "weights":"./fire/yolov9-s-fire-converted.pt", "source":"./fire/fire/train/images/114.jpg", "save_path":"runs/detect/CedarAlert353/114.jpg", "ts":"2024-08-31_10-47-16-196845", "email_ts":"email_not_sent", "sms_ts":"sms_not_sent", "exception": "exception_none"}
cedar_alert_folder() fn: 2024-08-31_10-47-16-196909.txt, path: /home/cedar/CedarAlert/cedar_alert_folder/2024-08-31_10-47-16-196909.txt, jstr: {"alert":"fire", "conf":"0.507", "weights":"./fire/yolov9-s-fire-converted.pt", "source":"./fire/fire/train/images/114.jpg", "save_path":"runs/detect/CedarAlert353/114.jpg", "ts":"2024-08-31_10-47-16-196845", "email_ts":"email_not_sent", "sms_ts":"sms_not_sent", "exception": "exception_none"}
alert_log_db() jstr: {"alert":"fire", "conf":"0.507", "weights":"./fire/yolov9-s-fire-converted.pt", "source":"./fire/fire/train/images/114.jpg", "save_path":"runs/detect/CedarAlert353/114.jpg", "ts":"2024-08-31_10-47-16-196845", "email_ts":"email_not_sent", "sms_ts":"sms_not_sent", "exception": "exception_none"}
log_add() j: {'alert': 'fire', 'conf': '0.507', 'weights': './fire/yolov9-s-fire-converted.pt', 'source': './fire/fire/train/images/114.jpg', 'save_path': 'runs/detect/CedarAlert353/114.jpg', 'ts': '2024-08-31_10-47-16-196845', 'email_ts': 'email_not_sent', 'sms_ts': 'sms_not_sent', 'exception': 'exception_none'}
log_add() sql: INSERT INTO LOG (fa, name, conf, weights, source, save_path, ts, email_ts, sms_ts, exception) VALUES ('alert', 'fire', '0.507', './fire/yolov9-s-fire-converted.pt', './fire/fire/train/images/114.jpg', 'runs/detect/CedarAlert353/114.jpg', '2024-08-31_10-47-16-196845', 'email_not_sent', 'sms_not_sent', 'exception_none');
[]
update_alert_last(): write(1725126436.200969)
update_alert_last() return
cedar_log_add() jstr: {"found":"fire", "conf":"0.576", "weights":"./fire/yolov9-s-fire-converted.pt", "source":"./fire/fire/train/images/114.jpg", "save_path":"runs/detect/CedarAlert353/114.jpg", "ts":"2024-08-31_10-47-16-201678", "email_ts":"email_none", "sms_ts":"sms_none", "exception": "exception_none"}
log_add() j: {'found': 'fire', 'conf': '0.576', 'weights': './fire/yolov9-s-fire-converted.pt', 'source': './fire/fire/train/images/114.jpg', 'save_path': 'runs/detect/CedarAlert353/114.jpg', 'ts': '2024-08-31_10-47-16-201678', 'email_ts': 'email_none', 'sms_ts': 'sms_none', 'exception': 'exception_none'}
log_add() sql: INSERT INTO LOG (fa, name, conf, weights, source, save_path, ts, email_ts, sms_ts, exception) VALUES ('found', 'fire', '0.576', './fire/yolov9-s-fire-converted.pt', './fire/fire/train/images/114.jpg', 'runs/detect/CedarAlert353/114.jpg', '2024-08-31_10-47-16-201678', 'email_none', 'sms_none', 'exception_none');
[]
cedar_log_add() jstr: {"found":"fire", "conf":"0.600", "weights":"./fire/yolov9-s-fire-converted.pt", "source":"./fire/fire/train/images/114.jpg", "save_path":"runs/detect/CedarAlert353/114.jpg", "ts":"2024-08-31_10-47-16-206369", "email_ts":"email_none", "sms_ts":"sms_none", "exception": "exception_none"}
log_add() j: {'found': 'fire', 'conf': '0.600', 'weights': './fire/yolov9-s-fire-converted.pt', 'source': './fire/fire/train/images/114.jpg', 'save_path': 'runs/detect/CedarAlert353/114.jpg', 'ts': '2024-08-31_10-47-16-206369', 'email_ts': 'email_none', 'sms_ts': 'sms_none', 'exception': 'exception_none'}
log_add() sql: INSERT INTO LOG (fa, name, conf, weights, source, save_path, ts, email_ts, sms_ts, exception) VALUES ('found', 'fire', '0.600', './fire/yolov9-s-fire-converted.pt', './fire/fire/train/images/114.jpg', 'runs/detect/CedarAlert353/114.jpg', '2024-08-31_10-47-16-206369', 'email_none', 'sms_none', 'exception_none');
[]
cedar_log_add() jstr: {"found":"fire", "conf":"0.618", "weights":"./fire/yolov9-s-fire-converted.pt", "source":"./fire/fire/train/images/114.jpg", "save_path":"runs/detect/CedarAlert353/114.jpg", "ts":"2024-08-31_10-47-16-213894", "email_ts":"email_none", "sms_ts":"sms_none", "exception": "exception_none"}
log_add() j: {'found': 'fire', 'conf': '0.618', 'weights': './fire/yolov9-s-fire-converted.pt', 'source': './fire/fire/train/images/114.jpg', 'save_path': 'runs/detect/CedarAlert353/114.jpg', 'ts': '2024-08-31_10-47-16-213894', 'email_ts': 'email_none', 'sms_ts': 'sms_none', 'exception': 'exception_none'}
log_add() sql: INSERT INTO LOG (fa, name, conf, weights, source, save_path, ts, email_ts, sms_ts, exception) VALUES ('found', 'fire', '0.618', './fire/yolov9-s-fire-converted.pt', './fire/fire/train/images/114.jpg', 'runs/detect/CedarAlert353/114.jpg', '2024-08-31_10-47-16-213894', 'email_none', 'sms_none', 'exception_none');
[]
cedar_log_add() jstr: {"found":"fire", "conf":"0.699", "weights":"./fire/yolov9-s-fire-converted.pt", "source":"./fire/fire/train/images/114.jpg", "save_path":"runs/detect/CedarAlert353/114.jpg", "ts":"2024-08-31_10-47-16-218385", "email_ts":"email_none", "sms_ts":"sms_none", "exception": "exception_none"}
log_add() j: {'found': 'fire', 'conf': '0.699', 'weights': './fire/yolov9-s-fire-converted.pt', 'source': './fire/fire/train/images/114.jpg', 'save_path': 'runs/detect/CedarAlert353/114.jpg', 'ts': '2024-08-31_10-47-16-218385', 'email_ts': 'email_none', 'sms_ts': 'sms_none', 'exception': 'exception_none'}
log_add() sql: INSERT INTO LOG (fa, name, conf, weights, source, save_path, ts, email_ts, sms_ts, exception) VALUES ('found', 'fire', '0.699', './fire/yolov9-s-fire-converted.pt', './fire/fire/train/images/114.jpg', 'runs/detect/CedarAlert353/114.jpg', '2024-08-31_10-47-16-218385', 'email_none', 'sms_none', 'exception_none');
[]
cedar_log_add() jstr: {"found":"fire", "conf":"0.712", "weights":"./fire/yolov9-s-fire-converted.pt", "source":"./fire/fire/train/images/114.jpg", "save_path":"runs/detect/CedarAlert353/114.jpg", "ts":"2024-08-31_10-47-16-223146", "email_ts":"email_none", "sms_ts":"sms_none", "exception": "exception_none"}
log_add() j: {'found': 'fire', 'conf': '0.712', 'weights': './fire/yolov9-s-fire-converted.pt', 'source': './fire/fire/train/images/114.jpg', 'save_path': 'runs/detect/CedarAlert353/114.jpg', 'ts': '2024-08-31_10-47-16-223146', 'email_ts': 'email_none', 'sms_ts': 'sms_none', 'exception': 'exception_none'}
log_add() sql: INSERT INTO LOG (fa, name, conf, weights, source, save_path, ts, email_ts, sms_ts, exception) VALUES ('found', 'fire', '0.712', './fire/yolov9-s-fire-converted.pt', './fire/fire/train/images/114.jpg', 'runs/detect/CedarAlert353/114.jpg', '2024-08-31_10-47-16-223146', 'email_none', 'sms_none', 'exception_none');
[]
cedar_log_add() jstr: {"found":"fire", "conf":"0.770", "weights":"./fire/yolov9-s-fire-converted.pt", "source":"./fire/fire/train/images/114.jpg", "save_path":"runs/detect/CedarAlert353/114.jpg", "ts":"2024-08-31_10-47-16-227578", "email_ts":"email_none", "sms_ts":"sms_none", "exception": "exception_none"}
log_add() j: {'found': 'fire', 'conf': '0.770', 'weights': './fire/yolov9-s-fire-converted.pt', 'source': './fire/fire/train/images/114.jpg', 'save_path': 'runs/detect/CedarAlert353/114.jpg', 'ts': '2024-08-31_10-47-16-227578', 'email_ts': 'email_none', 'sms_ts': 'sms_none', 'exception': 'exception_none'}
log_add() sql: INSERT INTO LOG (fa, name, conf, weights, source, save_path, ts, email_ts, sms_ts, exception) VALUES ('found', 'fire', '0.770', './fire/yolov9-s-fire-converted.pt', './fire/fire/train/images/114.jpg', 'runs/detect/CedarAlert353/114.jpg', '2024-08-31_10-47-16-227578', 'email_none', 'sms_none', 'exception_none');
[]
cedar_log_add() jstr: {"found":"fire", "conf":"0.840", "weights":"./fire/yolov9-s-fire-converted.pt", "source":"./fire/fire/train/images/114.jpg", "save_path":"runs/detect/CedarAlert353/114.jpg", "ts":"2024-08-31_10-47-16-232326", "email_ts":"email_none", "sms_ts":"sms_none", "exception": "exception_none"}
log_add() j: {'found': 'fire', 'conf': '0.840', 'weights': './fire/yolov9-s-fire-converted.pt', 'source': './fire/fire/train/images/114.jpg', 'save_path': 'runs/detect/CedarAlert353/114.jpg', 'ts': '2024-08-31_10-47-16-232326', 'email_ts': 'email_none', 'sms_ts': 'sms_none', 'exception': 'exception_none'}
log_add() sql: INSERT INTO LOG (fa, name, conf, weights, source, save_path, ts, email_ts, sms_ts, exception) VALUES ('found', 'fire', '0.840', './fire/yolov9-s-fire-converted.pt', './fire/fire/train/images/114.jpg', 'runs/detect/CedarAlert353/114.jpg', '2024-08-31_10-47-16-232326', 'email_none', 'sms_none', 'exception_none');
[]
cedar_log_add() jstr: {"found":"fire", "conf":"0.919", "weights":"./fire/yolov9-s-fire-converted.pt", "source":"./fire/fire/train/images/114.jpg", "save_path":"runs/detect/CedarAlert353/114.jpg", "ts":"2024-08-31_10-47-16-236834", "email_ts":"email_none", "sms_ts":"sms_none", "exception": "exception_none"}
log_add() j: {'found': 'fire', 'conf': '0.919', 'weights': './fire/yolov9-s-fire-converted.pt', 'source': './fire/fire/train/images/114.jpg', 'save_path': 'runs/detect/CedarAlert353/114.jpg', 'ts': '2024-08-31_10-47-16-236834', 'email_ts': 'email_none', 'sms_ts': 'sms_none', 'exception': 'exception_none'}
log_add() sql: INSERT INTO LOG (fa, name, conf, weights, source, save_path, ts, email_ts, sms_ts, exception) VALUES ('found', 'fire', '0.919', './fire/yolov9-s-fire-converted.pt', './fire/fire/train/images/114.jpg', 'runs/detect/CedarAlert353/114.jpg', '2024-08-31_10-47-16-236834', 'email_none', 'sms_none', 'exception_none');
[]
cedar_log_add() jstr: {"found":"fire", "conf":"0.962", "weights":"./fire/yolov9-s-fire-converted.pt", "source":"./fire/fire/train/images/114.jpg", "save_path":"runs/detect/CedarAlert353/114.jpg", "ts":"2024-08-31_10-47-16-241596", "email_ts":"email_none", "sms_ts":"sms_none", "exception": "exception_none"}
log_add() j: {'found': 'fire', 'conf': '0.962', 'weights': './fire/yolov9-s-fire-converted.pt', 'source': './fire/fire/train/images/114.jpg', 'save_path': 'runs/detect/CedarAlert353/114.jpg', 'ts': '2024-08-31_10-47-16-241596', 'email_ts': 'email_none', 'sms_ts': 'sms_none', 'exception': 'exception_none'}
log_add() sql: INSERT INTO LOG (fa, name, conf, weights, source, save_path, ts, email_ts, sms_ts, exception) VALUES ('found', 'fire', '0.962', './fire/yolov9-s-fire-converted.pt', './fire/fire/train/images/114.jpg', 'runs/detect/CedarAlert353/114.jpg', '2024-08-31_10-47-16-241596', 'email_none', 'sms_none', 'exception_none');
[]
cedar_log_add() jstr: {"found":"fire", "conf":"0.987", "weights":"./fire/yolov9-s-fire-converted.pt", "source":"./fire/fire/train/images/114.jpg", "save_path":"runs/detect/CedarAlert353/114.jpg", "ts":"2024-08-31_10-47-16-246211", "email_ts":"email_none", "sms_ts":"sms_none", "exception": "exception_none"}
log_add() j: {'found': 'fire', 'conf': '0.987', 'weights': './fire/yolov9-s-fire-converted.pt', 'source': './fire/fire/train/images/114.jpg', 'save_path': 'runs/detect/CedarAlert353/114.jpg', 'ts': '2024-08-31_10-47-16-246211', 'email_ts': 'email_none', 'sms_ts': 'sms_none', 'exception': 'exception_none'}
log_add() sql: INSERT INTO LOG (fa, name, conf, weights, source, save_path, ts, email_ts, sms_ts, exception) VALUES ('found', 'fire', '0.987', './fire/yolov9-s-fire-converted.pt', './fire/fire/train/images/114.jpg', 'runs/detect/CedarAlert353/114.jpg', '2024-08-31_10-47-16-246211', 'email_none', 'sms_none', 'exception_none');
[]
save_img, cv2.imwrite(save_path, im0), save_path: runs/detect/CedarAlert353/114.jpg
image 1/1 /home/cedar/CedarAlert/fire/fire/train/images/114.jpg: 480x640 11 fires,  349.0ms ./fire/yolov9-s-fire-converted.pt 
Speed: 1.4ms pre-process, 349.0ms inference, 0.9ms NMS per image at shape (1, 3, 640, 640) ./fire/yolov9-s-fire-converted.pt
Results saved to runs/detect/CedarAlert353
```
### Verify Application For Analyzing New Images from Cameras via FTP

```
(CedarAlert) cedar@NUC5i7RYH:~/CedarAlert$ python cedar_watch_object_fire_mp_pool.py
=== __main__ START at 2024-08-31_11-41-51-785716
=== __main__ cedar_ftp_path: /home/cedar/ftp
=== __main__ cedar_log: /home/cedar/CedarAlert/cedar_log.txt ===
=== __main__ cedar_email_timeout: 10.0
=== __main__ cedar_alert_folder: /home/cedar/CedarAlert/cedar_alert_folder
=== __main__ start watching image directory '/home/cedar/ftp'
=== __main__ start watching cedar_alert_folder '/home/cedar/CedarAlert/cedar_alert_folder'
```
When a new image arrives in the local desktop PC FTP folder structure ('cedar_ftp_path'), the 'ImageHandler()' sends the image to 'cedar_detect_dual.main(opt)' via a multiprocessing pool for analysis for objects (yolov9-s-converted.pt) and fire (yolov9-s-fire-converted.pt).

You can test this by moving a '.jpg' image file to any folder within the 'cedar_ftp_path' folder.

Whan an alert condition is found, a JSON object is sent to 'cedar_alert_folder', which acts as a semiphore in order to decouple the image from the alert functions since the alert functions depend upon a remote mail server.

The 'alert_email_process()' connects to an email server via SSL and attaches the image with caused the alert. The 'alert_email_process()' defaults to 3 attempts and will log failed attempts.

The 'alert_sms_process()' connects to an email server via SSL. The 'alert_sms_process()' defaults to 3 attempts and will log failed attempts. SMS messages are sent via the Verizon SMS portal (<yourcellnumber>@vtext.com), so you may need to change the 'alert_sms_process()' code if you have a different wireless carrier or wish to use a SMS service.

The application writes to a log file and also to a SQLite3 database by default. Either can be disabled with 'disable_log' or 'disable_sqlite3'.

The application runs as a service which starts on boot and restarts on error. 'CedarAlert.service' and 'CedarAlert.sh' must be modified with your '/home/YOURUSER'.

### FTP Server

A FTP server for the security camera image uploads can be installed as shown below. If desired, this user can also be used to run the CedarALert application.

The FTP path for image uploads (e.g. '/home/cedar/ftp/inbox') is defined by 'cedar_ftp_path' in 'cedar_vars.py'.

```
sudo adduser cedar
sudo apt install vsftpd
sudo systemctl status vsftpd --no-pager -l
sudo mkdir /home/cedar/ftp
sudo mkdir /home/cedar/ftp/inbox
sudo chown -R nobody:nogroup /home/cedar/ftp
sudo chmod -R a-w /home/cedar/ftp

sudo nano /etc/vsftpd.conf
```
add these lines to the end of file:
```
anonymous_enable=No
local_enable=YES
write_enable=YES
chroot_local_user=YES
user_sub_token=$USER
local_root=/home/$USER/ftp
userlist_enable=YES
userlist_file=/etc/vsftpd.userlist
userlist_deny=NO
```
The next commands are:
```
echo "cedar" | sudo tee -a /etc/vsftpd.userlist
sudo systemctl restart vsftpd
sudo systemctl enable vsftpd
sudo systemctl status vsftpd
```
### Verify FTP Server from a FTP Client (e.g. FileZilla)

You should now be able to upload files to the FTP Server folder '/home/cedar/ftp/inbox' (('cedar_ftp_path').

The CedarAlert application will analyze new image files from '/home/cedar/ftp/inbox' when the are uploaded.

The 'ImageHandler()' is recursive, so all folders under '/home/cedar/ftp/inbox' will be included.

If you have image file types other than '.jpg', the code in 'ImageHandler()' can be changed to allow other formats. The supported image formats are defined in 'utils/dataloads.py':

```
IMG_FORMATS = 'bmp', 'dng', 'jpeg', 'jpg', 'mpo', 'png', 'tif', 'tiff', 'webp', 'pfm'  # include image suffixes
```
### Support and Improvements

As stated above, this DIY application is provided as a free open source codebase as a courtesy without any promise of support nor guarantee of any kind, and was tested on two dfferent Ubuntu 22.04.4 X86_64 desktop computers.

When time permits, support questions will be answered. Questions pertaining to OS versions other than Ubuntu 22.04.4 may be difficult to answer.

Please provide your feedback and help answer questions in the Issues section.

Please also provide code improvements via a repository fork.

