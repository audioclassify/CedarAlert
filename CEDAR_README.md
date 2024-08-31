## CedarAlert - YOLOv9 Object and Fire Detection for IP Security Cameras in Python3

The CedarAlert application was developed on, and has been tested on, two Ubuntu 22.04.4 X86_64 desktop PCs:
* NUC5i7RYH (approx 10 year old Intel i7 CPU with 16 GB RAM and 500 GB SSD)
* Beelink Mini S12, Intel N100 CPU with 16 GB RAM and 500 GB SSD

The file 'cedar_vars.py' defines variables and creates a JSON object. The values with 'CHANGEME' ***must*** be set (e.g. your SMTP email server domain name 'cedar_email_server').

The YOLOv9 inference code is based upon 'detect_dual.py' and 'yolov9-s-converted.pt' model (weights) from [https://github.com/WongKinYiu/yolov9](https://github.com/WongKinYiu/yolov9).

The 'yolo9-s-fire-converted.pt' model (weights) is based the  [https://github.com/spacewalk01/yolov5-fire-detection]([https://github.com/spacewalk01/yolov5-fire-detection] and was created by from the 'datasets' folder using 'train_dual.py' from [https://github.com/WongKinYiu/yolov9](https://github.com/WongKinYiu/yolov9) in a python env with this command:

'''
cd ~
sudo apt update
sudo apt upgrade
sudo apt install -y build-essential libssl-dev libffi-dev python3-dev python3-pip python3-env

# Clone Repository
git clone https://github.com/audioclassify/CedarAlert.git

# Create New Python Environment
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
'''

The CedarAlert specific files start with 'cedar_' to distinguish them from files from [https://github.com/WongKinYiu/yolov9](https://github.com/WongKinYiu/yolov9).

The application can optionally write to a log file and also to a SQLite3 database.

The application runs as a service which starts on boot and restarts on error. 'CedarAlert.service' and 'CedarAlert.sh' must be modified with '/home/YOURUSER'.

This DIY application is provided as a free open source codebase as a courtesy without any promise of support nor guarantee of any kind.

This software is covered by the [GNU General Public License v3.0](https://github.com/WongKinYiu/yolov9/blob/main/LICENSE.md) and any other licenses from other open source code referenced.

### Verify CedarAlert Object Detecton with yolov9-s-converted.pt (COCO model)

'''
(CedarAlert) cedar@NUC5i7RYH:~/CedarAlert$ python cedar_detect_dual.py \
--source "./data/images/horses.jpg" \
--weights "./yolov9-s-converted.pt"

# Output (5 horses,  386.3ms)

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
'''
### Verify CedarAlert Fire Detecton with yolov9-s-fire-converted.pt (Fire model)
'''
(CedarAlert) cedar@NUC5i7RYH:~/CedarAlert$ python cedar_detect_dual.py \
--source "./fire/fire/train/images/114.jpg" \
--weights "./fire/yolov9-s-fire-converted.pt"

# Output (11 fires,  349.0ms)

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
'''


