import argparse
import os
import platform
import sys
from pathlib import Path

import torch

FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]  # YOLO root directory
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH
ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  # relative

from models.common import DetectMultiBackend
from utils.dataloaders import IMG_FORMATS, VID_FORMATS, LoadImages, LoadScreenshots, LoadStreams
from utils.general import (LOGGER, Profile, check_file, check_img_size, check_imshow, check_requirements, colorstr, cv2,
                           increment_path, non_max_suppression, print_args, scale_boxes, strip_optimizer, xyxy2xywh)
from utils.plots import Annotator, colors, save_one_box
from utils.torch_utils import select_device, smart_inference_mode

import time
from pprint import pprint
import traceback
import json

#
# cedar
#

from cedar_vars import cedar_vars_json_obj
cj = cedar_vars_json_obj() # for stand-alone

import cedar_timestamp
from cedar_timestamp import ts_now
from cedar_timestamp import ts_jpg
from cedar_timestamp import ts_txt
from cedar_timestamp import ts_from_time_string

import cedar_sqlite

@smart_inference_mode()
def run(
        
        weights			= './yolov9-c-converted.pt', 			# models
        source			= './data/images/horses.jpg',  			# file/dir/URL/glob/screen/0(webcam)
        data			= './data/coco.yaml',  					# dataset.yaml path
        imgsz			= (640, 640),  # inference size (height, width)
        conf_thres		= 0.25,  # confidence threshold
        iou_thres		= 0.45,  # NMS IOU threshold
        max_det			= 1000,  # maximum detections per image
        device			=' cpu',  # cuda device, i.e. 0 or 0,1,2,3 or cpu
        view_img		= False,  # show results       
        
        save_txt		= True,  # save results to *.txt
        save_conf		= True,  # save confidences in --save-txt labels
               
        save_crop		= False,  # save cropped prediction boxes
        nosave			= False,  # do not save images/videos
        classes			= None,  # filter by class: --class 0, or --class 0 2 3
        agnostic_nms	= False,  # class-agnostic NMS
        augment			= False,  # augmented inference
        visualize		= False,  # visualize features
        update			= False,  # update all models
        project			= './runs/detect',  # save results to project/name
        name			= 'exp',  # save results to project/name
        exist_ok		= False,  # existing project/name ok, do not increment
        line_thickness	= 3,  # bounding box thickness (pixels)
        hide_labels		= False,  # hide labels
        hide_conf		= False,  # hide confidences
        half			= False,  # use FP16 half-precision inference
        dnn				= False,  # use OpenCV DNN for ONNX inference
        vid_stride		= 1,  # video frame-rate stride
):
    source = str(source)
    save_img = not nosave and not source.endswith('.txt')  # save inference images
    is_file = Path(source).suffix[1:] in (IMG_FORMATS + VID_FORMATS)
    is_url = source.lower().startswith(('rtsp://', 'rtmp://', 'http://', 'https://'))
    webcam = source.isnumeric() or source.endswith('.txt') or (is_url and not is_file)
    screenshot = source.lower().startswith('screen')
    if is_url and is_file:
        source = check_file(source)  # download

    # Directories
    save_dir = increment_path(Path(project) / name, exist_ok=exist_ok)  # increment run
    (save_dir / 'labels' if save_txt else save_dir).mkdir(parents=True, exist_ok=True)  # make dir

    # Load model
    device = select_device(device)
    model = DetectMultiBackend(weights, device=device, dnn=dnn, data=data, fp16=half)
    stride, names, pt = model.stride, model.names, model.pt
    imgsz = check_img_size(imgsz, s=stride)  # check image size

    # Dataloader
    bs = 1  # batch_size
    if webcam:
        view_img = check_imshow(warn=True)
        dataset = LoadStreams(source, img_size=imgsz, stride=stride, auto=pt, vid_stride=vid_stride)
        bs = len(dataset)
    elif screenshot:
        dataset = LoadScreenshots(source, img_size=imgsz, stride=stride, auto=pt)
    else:
		
		#
		# cedarmod 08-18-2024
		#
		
        try:
            
            dataset = LoadImages(source, img_size=imgsz, stride=stride, auto=pt, vid_stride=vid_stride)
            vid_path, vid_writer = [None] * bs, [None] * bs
            
        except Exception as e:
            
            tb = f"%s, %s" %(e, traceback.format_exc())
            print("cedar_detect_dual run() tb: %s, type(tb): %s" % (tb, type(tb)))
	
            jstr = '{"exception":"ERROR cedar_detect_dual run()", "conf":"none", "weights":"none", "source":"none", "save_path":"none", "ts":"%s", "email_ts":"none", "sms_ts":"none", "exception": "%s"}' % (ts_now(), tb)
            print("ERROR cedar_detect_dual run() jstr: %s" % jstr)        
	
            cedar_log_add(jstr)
            cedar_sqlite.log_add(jstr)
            
            return
            
        finally:
		   
            print("cedar_detect_dual run() LoadImages OK, source: %s ===" % source)
        

    # Run inference
    model.warmup(imgsz=(1 if pt or model.triton else bs, 3, *imgsz))  # warmup
    seen, windows, dt = 0, [], (Profile(), Profile(), Profile())
    for path, im, im0s, vid_cap, s in dataset:
        with dt[0]:
            im = torch.from_numpy(im).to(model.device)
            im = im.half() if model.fp16 else im.float()  # uint8 to fp16/32
            im /= 255  # 0 - 255 to 0.0 - 1.0
            if len(im.shape) == 3:
                im = im[None]  # expand for batch dim

        weightstr = ""

        # print("cedar_detect_dual run() found weights: %s, type(weights): %s" % (weights, type(weights)))
                       
        if isinstance(weights, list):
          weightstr = weights[0]
          # print("cedar_detect_dual run() found list weightstr: %s, type(weightstr): %s" % (weightstr, type(weightstr)))
                       
        elif isinstance(weights, str):
          weightstr = weights
          # print("cedar_detect_dual run() found str weightstr: %s, type(weightstr): %s" % (weightstr, type(weightstr)))
                         
          # print("cedar_detect_dual run() found weightstr: %s, type(weightstr): %s" % (weightstr, type(weightstr)))
        # Inference
        with dt[1]:
            visualize = increment_path(save_dir / Path(path).stem, mkdir=True) if visualize else False
            pred = model(im, augment=augment, visualize=visualize)

            if 'converted' in weightstr:
              pred = pred[0]
            else:
              pred = pred[0][1]
         
            # print("pred: %s" % pred)

        # NMS
        with dt[2]:
            pred = non_max_suppression(pred, conf_thres, iou_thres, classes, agnostic_nms, max_det=max_det)

        # Second-stage classifier (optional)
        # pred = utils.general.apply_classifier(pred, classifier_model, im, im0s)
        
        # Process predictions
        for i, det in enumerate(pred):  # per image
            seen += 1
            if webcam:  # batch_size >= 1
                p, im0, frame = path[i], im0s[i].copy(), dataset.count
                s += f'{i}: '
            else:
                p, im0, frame = path, im0s.copy(), getattr(dataset, 'frame', 0)

            p = Path(p)  # to Path
            save_path = str(save_dir / p.name)  # im.jpg
            txt_path = str(save_dir / 'labels' / p.stem) + ('' if dataset.mode == 'image' else f'_{frame}')  # im.txt
            s += '%gx%g ' % im.shape[2:]  # print string
            gn = torch.tensor(im0.shape)[[1, 0, 1, 0]]  # normalization gain whwh
            imc = im0.copy() if save_crop else im0  # for save_crop
            annotator = Annotator(im0, line_width=line_thickness, example=str(names))


            if len(det):
                # Rescale boxes from img_size to im0 size
                det[:, :4] = scale_boxes(im.shape[2:], det[:, :4], im0.shape).round()

                for c in det[:, 5].unique():
                    n = (det[:, 5] == c).sum()  # detections per class
                    s += f"{n} {names[int(c)]}{'s' * (n > 1)}, "  # add to string

                # Write results
                for *xyxy, conf, cls in reversed(det):
                    
                    if save_txt:  # Write to file
                    #if 1 == 1:
                        xywh = (xyxy2xywh(torch.tensor(xyxy).view(1, 4)) / gn).view(-1).tolist()  # normalized xywh
                        line = (cls, *xywh, conf) if save_conf else (cls, *xywh)  # label format
                        
                        #os.makedirs(os.path.dirname(f'{txt_path}.txt'), exist_ok=True)
                        
                        with open(f'{txt_path}.txt', 'a') as f:									
                            f.write(('%g ' * len(line)).rstrip() % line + '\n')

                    if save_img or save_crop or view_img:  # Add bbox to image
                       c = int(cls)  # integer class

                       label = None if hide_labels else (names[c] if hide_conf else f'{names[c]} {conf:.2f}')
                       
                       annotator.box_label(xyxy, label, color=colors(c, True))

                       #
                       # cedarmod 08-07-2024
                       #
                       
                       jstr = '{"found":"%s", "conf":"%.3f", "weights":"%s", "source":"%s", "save_path":"%s", "ts":"%s", "email_ts":"email_none", "sms_ts":"sms_none", "exception": "exception_none"}' % (names[c], conf, weightstr, source, save_path, ts_now())
                       # print("cedar_detect_dual run() found jstr: %s" % jstr)
                       
                       cedar_log_add(jstr)       
                       cedar_sqlite.log_add(jstr)
                       
                       #
                       # alerts
                       #
                       
                       #alert_last_float = alert_last_float_get()
                       
                       if time.time() - alert_last_float_get() > cj['cedar_alert_seconds']: # ok to send alert after cedar_alert_seconds
						   
                         # alert_last_float_dt = ts_from_time_string(alert_last_float)
                         # print("\n=== cedar_detect_dual run() ok to send alert, alert_last_float %f, alert_last_float_dt: %s ===\n" % (alert_last_float, alert_last_float_dt))
                       
                         if names[c] == "fire": 
                           jstr = '{"alert":"%s", "conf":"%.3f", "weights":"%s", "source":"%s", "save_path":"%s", "ts":"%s", "email_ts":"email_not_sent", "sms_ts":"sms_not_sent", "exception": "exception_none"}' % (names[c], conf, weightstr, source, save_path, ts_now())
                           cedar_alert_folder_add(jstr)
                           alert_log_db(jstr)
                           update_alert_last()
                         
                         elif names[c] == "person":
                           jstr = '{"alert":"%s", "conf":"%.3f", "weights":"%s", "source":"%s", "save_path":"%s", "ts":"%s", "email_ts":"email_not_sent", "sms_ts":"sms_not_sent", "exception": "exception_none"}' % (names[c], conf, weightstr, source, save_path, ts_now())
                           cedar_alert_folder_add(jstr)
                           alert_log_db(jstr)
                           update_alert_last()

                         elif names[c] == "bicycle":
                           jstr = '{"alert":"%s", "conf":"%.3f", "weights":"%s", "source":"%s", "save_path":"%s", "ts":"%s", "email_ts":"email_not_sent", "sms_ts":"sms_not_sent", "exception": "exception_none"}' % (names[c], conf, weightstr, source, save_path, ts_now())
                           cedar_alert_folder_add(jstr)
                           alert_log_db(jstr)
                           update_alert_last()
                           			   
                         elif names[c] == "bear":
                           jstr = '{"alert":"%s", "conf":"%.3f", "weights":"%s", "source":"%s", "save_path":"%s", "ts":"%s", "email_ts":"email_not_sent", "sms_ts":"sms_not_sent", "exception": "exception_none"}' % (names[c], conf, weightstr, source, save_path, ts_now())
                           cedar_alert_folder_add(jstr)
                           alert_log_db(jstr)
                           update_alert_last()
                           
                    
                    if save_crop:
                        save_one_box(xyxy, imc, file=save_dir / 'crops' / names[c] / f'{p.stem}.jpg', BGR=True)


            #
            # cedarmod 08-11-2024
            #

            
            # Stream results
            im0 = annotator.result()
            if view_img:
                if platform.system() == 'Linux' and p not in windows:
                    windows.append(p)
                    cv2.namedWindow(str(p), cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO)  # allow window resize (Linux)
                    cv2.resizeWindow(str(p), im0.shape[1], im0.shape[0])
                cv2.imshow(str(p), im0)
                cv2.waitKey(1)  # 1 millisecond

            # Save results (image with detections)
            if save_img:
                if dataset.mode == 'image':
                    cv2.imwrite(save_path, im0)
                    
                    print("save_img, cv2.imwrite(save_path, im0), save_path: %s" % save_path) # cedarmod
                    
                else:  # 'video' or 'stream'
                    if vid_path[i] != save_path:  # new video
                        vid_path[i] = save_path
                        if isinstance(vid_writer[i], cv2.VideoWriter):
                            vid_writer[i].release()  # release previous video writer
                        if vid_cap:  # video
                            fps = vid_cap.get(cv2.CAP_PROP_FPS)
                            w = int(vid_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                            h = int(vid_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                        else:  # stream
                            fps, w, h = 30, im0.shape[1], im0.shape[0]
                        save_path = str(Path(save_path).with_suffix('.mp4'))  # force *.mp4 suffix on results videos
                        vid_writer[i] = cv2.VideoWriter(save_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (w, h))
                    vid_writer[i].write(im0)

        # Print time (inference-only)
        # LOGGER.info(f"{s}{'' if len(det) else '(no detections), '}{dt[1].dt * 1E3:.1f}ms")
        LOGGER.info(f"{s} {'' if len(det) else '(no detections), '}{dt[1].dt * 1E3:.1f}ms {weightstr} ")

        #
        # log no_detections
        #
        if cj['cedar_log_no_detections']:
            jstr = '{"found":"no_detections", "conf":"n/a", "weights":"%s", "source":"%s", "save_path":"%s", "ts":"%s", "email_ts":"n/a", "sms_ts":"n/a", "exception": "exception_none"}' % (weightstr, source, save_path, ts_now())
            print("run() no_detections jstr: %s" % jstr)
            cedar_log_add(jstr)      
            cedar_sqlite.log_add(jstr)

    # Print results
    t = tuple(x.t / seen * 1E3 for x in dt)  # speeds per image
    LOGGER.info(f'Speed: %.1fms pre-process, %.1fms inference, %.1fms NMS per image at shape {(1, 3, *imgsz)} {weightstr}' % t)
    if save_txt or save_img:
        s = f"\n{len(list(save_dir.glob('labels/*.txt')))} labels saved to {save_dir / 'labels'}" if save_txt else ''
        LOGGER.info(f"Results saved to {colorstr('bold', save_dir)}{s}")
    if update:
        strip_optimizer(weights[0])  # update model (to fix SourceChangeWarning)


def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('--weights', nargs='+', type=str, default='./weights/yolov9-c-converted.pt', help='model path or triton URL')
    parser.add_argument('--source', type=str, default='./data/images/horses,jpg', help='file/dir/URL/glob/screen/0(webcam)')
    parser.add_argument('--data', type=str, default='./data/coco128.yaml', help='(optional) dataset.yaml path')
    parser.add_argument('--imgsz', '--img', '--img-size', nargs='+', type=int, default=[640], help='inference size h,w')
    
    #parser.add_argument('--conf-thres', type=float, default=0.25, help='confidence threshold')
    #parser.add_argument('--conf-thres', type=float, default=0.40, help='confidence threshold')
    #parser.add_argument('--conf-thres', type=float, default=0.50, help='confidence threshold')
    parser.add_argument('--conf-thres', type=float, default=0.70, help='confidence threshold')
    
    parser.add_argument('--iou-thres', type=float, default=0.45, help='NMS IoU threshold')
    parser.add_argument('--max-det', type=int, default=1000, help='maximum detections per image')
    
    #parser.add_argument('--device', default='', help='cuda device, i.e. 0 or 0,1,2,3 or cpu')
    parser.add_argument('--device', default='cpu', help='cuda device, i.e. 0 or 0,1,2,3 or cpu')
    
    parser.add_argument('--view-img', action='store_true', help='show results')
    parser.add_argument('--save-txt', action='store_true', help='save results to *.txt')
    parser.add_argument('--save-conf', action='store_true', help='save confidences in --save-txt labels')
    parser.add_argument('--save-crop', action='store_true', help='save cropped prediction boxes')
    parser.add_argument('--nosave', action='store_true', help='do not save images/videos')
    parser.add_argument('--classes', nargs='+', type=int, help='filter by class: --classes 0, or --classes 0 2 3')
    parser.add_argument('--agnostic-nms', action='store_true', help='class-agnostic NMS')
    parser.add_argument('--augment', action='store_true', help='augmented inference')
    parser.add_argument('--visualize', action='store_true', help='visualize features')
    parser.add_argument('--update', action='store_true', help='update all models')
    parser.add_argument('--project', default='./runs/detect', help='save results to project/name')
    parser.add_argument('--name', default='CedarAlert', help='save results to project/name')
    parser.add_argument('--exist-ok', action='store_true', help='existing project/name ok, do not increment')
    parser.add_argument('--line-thickness', default=3, type=int, help='bounding box thickness (pixels)')
    parser.add_argument('--hide-labels', default=False, action='store_true', help='hide labels')
    parser.add_argument('--hide-conf', default=False, action='store_true', help='hide confidences')
    parser.add_argument('--half', action='store_true', help='use FP16 half-precision inference')
    parser.add_argument('--dnn', action='store_true', help='use OpenCV DNN for ONNX inference')
    parser.add_argument('--vid-stride', type=int, default=1, help='video frame-rate stride')
    opt = parser.parse_args()
    opt.imgsz *= 2 if len(opt.imgsz) == 1 else 1  # expand
    #print_args(vars(opt))
    return opt

def main(opt):
    # check_requirements(exclude=('tensorboard', 'thop'))
    run(**vars(opt))
    
def update_alert_last():
	alert_last_float = time.time()
	alert_last_str	= str(alert_last_float)
	print("update_alert_last(): write(%s)" % alert_last_str)
	f = open(cj['cedar_alert_last'],"w")
	f.write(alert_last_str)
	f.close()
	
	print("update_alert_last() return")
	return
    
def alert_log_db(jstr):
	
	print("alert_log_db() jstr: %s" % jstr)
	
	f = open(cj['cedar_log'],"a")
	f.write('\n' + jstr)
	f.close()
	
	cedar_sqlite.log_add(jstr)
	
def cedar_log_add(jstr):
	
	if cj['disable_log']:
		return
	
	print("cedar_log_add() jstr: %s" % jstr)
	
	f = open(cj['cedar_log'], "a")
	f.write("\n" + jstr)
	f.close()		
	
def cedar_alert_folder_add(jstr):
	
	print("cedar_alert_folder() jstr: %s" % jstr)
	
	j 		= json.loads(jstr)
	
	fn 		= ts_now() + ".txt"
	
	path 	= cj['cedar_alert_folder'] + "/" + fn
	
	print("cedar_alert_folder() fn: %s, path: %s, jstr: %s" % (fn, path, jstr))

	f = open(path, "w")
	f.write(jstr)
	f.close()	

def alert_last_float_get():
	f = open(cj['cedar_alert_last'],"r")
	alert_last_str 	= f.read()
	f.close()
	alert_last_float	= float(alert_last_str)
	#print("read() alert_last_str: %s" % alert_last_str)
	return alert_last_float
	
if __name__ == "__main__":
    
    opt = parse_opt()
    # print(opt)
    main(opt)
