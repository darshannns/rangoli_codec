import cv2
import numpy as np
from typing import Tuple, List, Optional

def binary_to_text(binary_data: str) -> str:
    byte_list = []
    for i in range(0, len(binary_data), 8):
        byte = binary_data[i:i+8]
        if len(byte) < 8:
            continue
        try:
            byte_list.append(int(byte, 2))
        except ValueError:
            pass
    # Strip null padding bytes added by the grid rounding
    return bytearray(byte_list).decode('utf-8', errors='replace').rstrip('\x00')
def check_pixel_area(roi: np.ndarray, p: Tuple[int, int]) -> bool:
    y, x = p
    y_start, y_end = max(0, y-3), min(roi.shape[0], y+4)
    x_start, x_end = max(0, x-3), min(roi.shape[1], x+4)
    area = roi[y_start:y_end, x_start:x_end]
    return bool(area.size > 0 and np.min(area) == 0)

def find_scale_bars(img_color: np.ndarray) -> Optional[Tuple[float, float, int, int, int, int]]:
    h, w = img_color.shape[:2]
    center_x, center_y = w // 2, h // 2
    hsv = cv2.cvtColor(img_color, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, np.array([140, 100, 100]), np.array([160, 255, 255]))
    mask[0:center_y, center_x:w] = 0
    mask[center_y:h, 0:w] = 0
    
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours or len(contours) < 2:
        return None

    v_bar, h_bar, v_contour, h_contour = None, None, None, None
    for c in contours:
        x, y, wb, hb = cv2.boundingRect(c)
        if wb > hb:
            h_bar, h_contour = (x, y, wb, hb), c
        elif hb > wb:
            v_bar, v_contour = (x, y, wb, hb), c
            
    if v_bar is None or h_bar is None:
        return None
        
    cell_w = float(max(cv2.minAreaRect(h_contour)[1]))
    cell_h = float(max(cv2.minAreaRect(v_contour)[1]))
    grid_x_start = h_bar[0]
    grid_y_start = v_bar[1]
    
    return cell_w, cell_h, grid_x_start, grid_y_start, center_x, center_y

def decode_tile(tile_roi: np.ndarray) -> List[int]:
    ch, cw = tile_roi.shape[:2]
    if ch < 10 or cw < 10:
        return [0] * 8
    points = {
        0: (int(ch*0.1), int(cw*0.9)),
        1: (int(ch*0.9), int(cw*0.9)),
        2: (int(ch*0.9), int(cw*0.1)),
        3: (int(ch*0.1), int(cw*0.1)),
        4: (int(ch*0.4), int(cw*0.6)),
        5: (int(ch*0.6), int(cw*0.6)),
        6: (int(ch*0.6), int(cw*0.4)),
        7: (int(ch*0.4), int(cw*0.4))
    }
    return [1 if check_pixel_area(tile_roi, points[i]) else 0 for i in range(8)]

def decode_from_image(image_path: str) -> str:
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"Cannot load image {image_path}")

    anchor_data = find_scale_bars(img)
    if not anchor_data:
        raise ValueError("Could not find calibration scale bars in top-left quadrant.")

    cell_w, cell_h, gx_start, gy_start, cx, cy = anchor_data
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)

    grid_w = cx - gx_start
    grid_h = cy - gy_start
    grid_roi = thresh[gy_start:cy, gx_start:cx]

    R = int(round(grid_h / cell_h))
    C = int(round(grid_w / cell_w))

    bits_stream = []
    for r in range(R):
        for c in range(C):
            tx0 = int(c * cell_w)
            ty0 = int(r * cell_h)
            roi = grid_roi[ty0:min(ty0 + int(cell_h), grid_h), tx0:min(tx0 + int(cell_w), grid_w)]
            tile_bits = decode_tile(roi)
            binary_str = "".join(map(str, tile_bits[::-1]))
            bits_stream.append(binary_str)

    return binary_to_text("".join(bits_stream))