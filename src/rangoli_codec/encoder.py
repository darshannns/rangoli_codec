import math
from typing import List
import matplotlib.pyplot as plt
from .core import quad_bezier, control_for_arc

CELL = 80
MARGIN = 20
LINE_W = 2.0
AXIS_W = 0.5
BG = "#ffffff"
ARC_COLOR = "#000000"
AXIS_COLOR = "#aaaaaa"
SCALE_COLOR = "#FF00FF"

def text_to_binary(text: str) -> str:
    return ''.join(format(byte, '08b') for byte in text.encode('utf-8'))

def binary_to_segments(binary_str: str) -> List[str]:
    if not binary_str:
        return ["00000000"]
    pad_len = ((len(binary_str) + 7) // 8) * 8
    binary_str = binary_str.zfill(pad_len)
    return [binary_str[i:i+8] for i in range(0, len(binary_str), 8)]

def draw_tile_kaleidoscope(ax, x0_base: float, y0_base: float, byte: str):
    x1_base, y1_base = x0_base + CELL, y0_base + CELL
    cx_base, cy_base = (x0_base + x1_base)/2.0, (y0_base + y1_base)/2.0
    N_base, E_base, S_base, W_base = (cx_base, y1_base), (x1_base, cy_base), (cx_base, y0_base), (x0_base, cy_base)
    
    bits = byte.zfill(8)
    b = bits[::-1]
    rim_pairs_base = [(N_base, E_base), (E_base, S_base), (S_base, W_base), (W_base, N_base)]
    curves_to_plot = []

    for i in range(4):
        a, d = rim_pairs_base[i]
        if b[i] == "1":
            p1_out = control_for_arc(a, d, (cx_base, cy_base), 0.0, arc_scale=1.0)
            curves_to_plot.append(quad_bezier(a, p1_out, d, steps=60))
        if b[i+4] == "1":
            p1_in = control_for_arc(a, d, (cx_base, cy_base), 1.0, arc_scale=1.0)
            curves_to_plot.append(quad_bezier(a, p1_in, d, steps=60))

    for pts_qii in curves_to_plot:
        x_qii = [p[0] for p in pts_qii]
        y_qii = [p[1] for p in pts_qii]
        
        ax.plot([-x for x in x_qii], y_qii, lw=LINE_W, color=ARC_COLOR)
        ax.plot(x_qii, y_qii, lw=LINE_W, color=ARC_COLOR)
        ax.plot(x_qii, [-y for y in y_qii], lw=LINE_W, color=ARC_COLOR)
        ax.plot([-x for x in x_qii], [-y for y in y_qii], lw=LINE_W, color=ARC_COLOR)

def encode_to_image(text: str, output_path: str = "rangoli_output.png", show: bool = False) -> str:
    binary_str = text_to_binary(text)
    bytes_seq = binary_to_segments(binary_str)
    
    s = len(bytes_seq)
    R = math.ceil(math.sqrt(s))
    W_quad = R * CELL
    H_quad = R * CELL
    W_total = 2 * W_quad + 2 * MARGIN
    H_total = 2 * H_quad + 2 * MARGIN

    fig, ax = plt.subplots(figsize=(W_total/90, H_total/90), dpi=90)
    ax.set_facecolor(BG)
    fig.patch.set_facecolor(BG)

    k = 0
    for r in range(R):
        for c in range(R):
            x0_base = -W_quad + c * CELL
            y0_base = H_quad - (r + 1) * CELL
            if k < s:
                draw_tile_kaleidoscope(ax, x0_base, y0_base, bytes_seq[k])
            k += 1

    scale_x_v = -W_quad - (MARGIN / 2)
    scale_y_top = H_quad
    scale_y_bottom = H_quad - CELL
    ax.plot([scale_x_v, scale_x_v], [scale_y_top, scale_y_bottom], color=SCALE_COLOR, lw=LINE_W * 2, solid_capstyle="butt")

    scale_y_h = H_quad + (MARGIN / 2)
    scale_x_left = -W_quad
    scale_x_right = -W_quad + CELL
    ax.plot([scale_x_left, scale_x_right], [scale_y_h, scale_y_h], color=SCALE_COLOR, lw=LINE_W * 2, solid_capstyle="butt")

    ax.set_xlim(-W_quad - MARGIN, W_quad + MARGIN)
    ax.set_ylim(-H_quad - MARGIN, H_quad + MARGIN)
    ax.set_aspect('equal', adjustable='box')
    ax.axhline(0, color=AXIS_COLOR, lw=AXIS_W, zorder=0)
    ax.axvline(0, color=AXIS_COLOR, lw=AXIS_W, zorder=0)
    ax.axis("off")
    plt.tight_layout(pad=0.1)

    plt.savefig(output_path, dpi=200, bbox_inches="tight", facecolor=BG)
    
    # Pop up an interactive visual window if requested
    if show:
        plt.show()

    plt.close(fig)
    return output_path