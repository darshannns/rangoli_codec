import math
from typing import List, Tuple

def quad_bezier(p0: Tuple[float, float], p1: Tuple[float, float], p2: Tuple[float, float], steps: int = 48) -> List[Tuple[float, float]]:
    pts = []
    for i in range(steps + 1):
        t = i / steps
        u = 1.0 - t
        x = u * u * p0[0] + 2 * u * t * p1[0] + t * t * p2[0]
        y = u * u * p0[1] + 2 * u * t * p1[1] + t * t * p2[1]
        pts.append((x, y))
    return pts

def control_for_arc(a: Tuple[float, float], b: Tuple[float, float], center: Tuple[float, float], curvature: float, arc_scale: float = 0.75) -> Tuple[float, float]:
    ax, ay = a
    bx, by = b
    mx, my = (ax + bx) / 2.0, (ay + by) / 2.0
    vx, vy = (bx - ax), (by - ay)
    nx, ny = -vy, vx
    nv = math.hypot(nx, ny) or 1.0
    nx, ny = nx / nv, ny / nv
    cx, cy = center
    to_cx, to_cy = cx - mx, cy - my
    sgn = 1.0 if (nx * to_cx + ny * to_cy) >= 0 else -1.0
    k = (curvature - 0.5) * 2.0
    base = arc_scale * 0.55 * math.hypot(vx, vy)
    mag = base * abs(k)
    direction = sgn if k >= 0 else -sgn
    return (mx + nx * direction * mag, my + ny * direction * mag)