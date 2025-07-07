import cv2
import numpy as np
import os
import mss

# Paths
HEROIMG_DIR = 'crawler/heroimg'
FRAME_DIR = 'crawler/frame'
MINIMAP_PATH = 'minimap.png'

# Frame color BGR values (approximate)
FRAME_COLORS = ['Green', 'Blue', 'Red']
TEMPLATE_THRESHOLD = 0.7  # Adjust as needed
NMS_THRESHOLD = 0.3

# Load all hero images
hero_templates = {}
for fname in os.listdir(HEROIMG_DIR):
    if fname.endswith('.jpg'):
        hero_id = os.path.splitext(fname)[0]
        img = cv2.imread(os.path.join(HEROIMG_DIR, fname), cv2.IMREAD_UNCHANGED)
        if img is not None:
            # Ensure template is 3-channel BGR
            if img.ndim == 2:
                img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
            elif img.shape[2] == 4:
                img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
            hero_templates[hero_id] = img

# Define the region of the screen to monitor (update these values!)
MONITOR_REGION = {"left": 100, "top": 100, "width": 300, "height": 300}  # <-- Set to your minimap's position and size

# Helper: classify frame color
def classify_frame_color(region):
    # region: BGR image
    mean_color = np.mean(region.reshape(-1, 3), axis=0)
    for color, (lower, upper) in FRAME_COLORS.items():
        if np.all(mean_color >= lower) and np.all(mean_color <= upper):
            return color
    return 'unknown'

# Helper: non-maximum suppression
from collections import namedtuple
Detection = namedtuple('Detection', ['x', 'y', 'w', 'h', 'score', 'hero_id'])
def nms(detections, iou_thresh=0.3):
    if not detections:
        return []
    boxes = np.array([[d.x, d.y, d.x+d.w, d.y+d.h, d.score] for d in detections])
    idxs = boxes[:,4].argsort()[::-1]
    keep = []
    while len(idxs) > 0:
        i = idxs[0]
        keep.append(detections[i])
        xx1 = np.maximum(boxes[i,0], boxes[idxs[1:],0])
        yy1 = np.maximum(boxes[i,1], boxes[idxs[1:],1])
        xx2 = np.minimum(boxes[i,2], boxes[idxs[1:],2])
        yy2 = np.minimum(boxes[i,3], boxes[idxs[1:],3])
        w = np.maximum(0, xx2 - xx1)
        h = np.maximum(0, yy2 - yy1)
        inter = w * h
        area1 = (boxes[i,2]-boxes[i,0]) * (boxes[i,3]-boxes[i,1])
        area2 = (boxes[idxs[1:],2]-boxes[idxs[1:],0]) * (boxes[idxs[1:],3]-boxes[idxs[1:],1])
        iou = inter / (area1 + area2 - inter + 1e-6)
        idxs = idxs[1:][iou < iou_thresh]
    return keep

# Main detection loop: monitor the screen region in real time
with mss.mss() as sct:
    while True:
        # Capture the region
        sct_img = sct.grab(MONITOR_REGION)
        minimap = np.array(sct_img)[..., :3]  # Remove alpha channel if present (BGRA -> BGR)

        display_img = minimap.copy()
        detections = []
        for hero_id, template in hero_templates.items():
            th, tw = template.shape[:2]
            if minimap.shape[0] < th or minimap.shape[1] < tw:
                continue
            res = cv2.matchTemplate(minimap, template, cv2.TM_CCOEFF_NORMED)
            loc = np.where(res >= TEMPLATE_THRESHOLD)
            for pt in zip(*loc[::-1]):
                score = res[pt[1], pt[0]]
                detections.append(Detection(pt[0], pt[1], tw, th, score, hero_id))
        detections = nms(detections)
        detections = sorted(detections, key=lambda d: d.score, reverse=True)[:10]
        for det in detections:
            x, y, w, h = det.x, det.y, det.w, det.h
            region = minimap[y:y+h, x:x+w]
            frame_color = classify_frame_color(region)
            color_map = {'Green': (0,255,0), 'Blue': (255,0,0), 'Red': (0,0,255), 'unknown': (128,128,128)}
            cv2.rectangle(display_img, (x, y), (x+w, y+h), color_map[frame_color], 2)
            cv2.putText(display_img, f'{det.hero_id} ({frame_color})', (x, y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color_map[frame_color], 1)
        cv2.imshow('Minimap Hero Detection', display_img)
        key = cv2.waitKey(10)
        if key == 27:  # ESC to quit
            break
cv2.destroyAllWindows() 