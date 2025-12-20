# collition.py

from typing import Tuple
import math
import pygame

EPS = 1e-9

def predict_segment_rect(
    start: pygame.Vector2,
    end: pygame.Vector2,
    rect: pygame.Rect,
    radius: float = 0.0
) -> Tuple[str, pygame.Vector2]:
    start_v = pygame.Vector2(start)
    vel = pygame.Vector2(end) - start_v

    if vel.length_squared() < EPS:
        return "none", pygame.Vector2(end)

    expanded = pygame.Rect(
        rect.left - radius,
        rect.top - radius,
        rect.width + 2 * radius,
        rect.height + 2 * radius,
    )

    res = _ray_aabb_time(start_v, vel, expanded)
    if res is None:
        return "none", pygame.Vector2(end)

    t_entry, t_exit, normal = res
    
    if t_entry < -EPS or t_entry > 1.0 + EPS:
        return "none", pygame.Vector2(end)

    collision_point = start_v + vel * max(0.0, min(1.0, t_entry))

    if abs(normal.x) > 0.5:
        return "vertical", collision_point
    if abs(normal.y) > 0.5:
        return "horizontal", collision_point

    if abs(normal.x) >= abs(normal.y):
        return "vertical", collision_point
    return "horizontal", collision_point


def _ray_aabb_time(
    pos: pygame.Vector2,
    vel: pygame.Vector2,
    rect: pygame.Rect
):
    """
    Ray (pos, vel) vs AABB(rect) — devuelve (t_entry, t_exit, normal) o None.
    t_entry/t_exit en unidades relativas a vel (i.e., t en [0,1] para segment).
    normal: vector que aproxima la normal de la cara de entrada.
    """
    px, py = float(pos.x), float(pos.y)
    vx, vy = float(vel.x), float(vel.y)

    left, right = float(rect.left), float(rect.right)
    top, bottom = float(rect.top), float(rect.bottom)

    # X axis
    if abs(vx) < EPS:
        if px < left or px > right:
            return None
        tx_entry = -math.inf
        tx_exit = math.inf
    else:
        tx1 = (left - px) / vx
        tx2 = (right - px) / vx
        tx_entry = min(tx1, tx2)
        tx_exit = max(tx1, tx2)

    # Y axis
    if abs(vy) < EPS:
        if py < top or py > bottom:
            return None
        ty_entry = -math.inf
        ty_exit = math.inf
    else:
        ty1 = (top - py) / vy
        ty2 = (bottom - py) / vy
        ty_entry = min(ty1, ty2)
        ty_exit = max(ty1, ty2)

    t_entry = max(tx_entry, ty_entry)
    t_exit = min(tx_exit, ty_exit)

    if t_entry > t_exit:
        return None
    if t_exit < 0:
        return None

    # decidir normal por qué eje produce t_entry
    if abs(vx) < EPS:
        tx_entry = -math.inf
    else:
        tx1 = (left - px) / vx
        tx2 = (right - px) / vx
        tx_entry = min(tx1, tx2)

    if abs(vy) < EPS:
        ty_entry = -math.inf
    else:
        ty1 = (top - py) / vy
        ty2 = (bottom - py) / vy
        ty_entry = min(ty1, ty2)

    if tx_entry > ty_entry:
        if vx > 0:
            normal = pygame.Vector2(-1, 0)
        else:
            normal = pygame.Vector2(1, 0)
    elif ty_entry > tx_entry:
        if vy > 0:
            normal = pygame.Vector2(0, -1)
        else:
            normal = pygame.Vector2(0, 1)
    else:
        contact_point = pos + vel * t_entry
        cx = (left + right) / 2.0
        cy = (top + bottom) / 2.0
        n = pygame.Vector2(contact_point.x - cx, contact_point.y - cy)
        if n.length_squared() == 0:
            normal = pygame.Vector2(-math.copysign(1, vx), -math.copysign(1, vy))
        else:
            normal = n.normalize()

    return float(t_entry), float(t_exit), normal