import math
import random
import pygame


def skapa_gard_bakgrund(bredd: int, hojd: int) -> pygame.Surface:
    """Skapar en solig utomhusgård med himmel, sol, gräs, grusplan och skrot i fjärran."""
    yta = pygame.Surface((bredd, hojd))
    horisont_y = int(hojd * 0.42)

    # Gradvis himmel (ljusblå mot horisonten, djupare blå högre upp)
    for y in range(horisont_y):
        t = y / max(1, horisont_y)
        r = int(112 + t * 88)
        g = int(182 + t * 52)
        b = int(242 + t * 8)
        pygame.draw.line(yta, (r, g, b), (0, y), (bredd, y))

    # Strålande sol uppe till vänster
    sol_x, sol_y = 95, 72
    for radie, alfa in [(88, 22), (62, 42), (42, 85), (28, 255)]:
        sol_lager = pygame.Surface((radie * 2 + 8, radie * 2 + 8), pygame.SRCALPHA)
        pygame.draw.circle(sol_lager, (255, 232, 120, alfa), (radie + 4, radie + 4), radie)
        yta.blit(sol_lager, (sol_x - radie - 4, sol_y - radie - 4))

    # Mjuka moln
    for mx, my, skala in [(250, 58, 1.0), (490, 44, 0.8), (610, 74, 0.9)]:
        moln = pygame.Surface((130, 50), pygame.SRCALPHA)
        for dx, dy, rad in [(28, 28, 16), (48, 20, 22), (72, 22, 18), (92, 29, 14)]:
            pygame.draw.circle(moln, (255, 255, 255, 195), (dx, dy), rad)
        moln_skalad = pygame.transform.smoothscale(moln, (int(130 * skala), int(50 * skala)))
        yta.blit(moln_skalad, (mx, my))

    # Avlägsna skrotkullar & berg vid horisonten
    pygame.draw.polygon(
        yta,
        (108, 128, 112),
        [(0, horisont_y), (120, horisont_y - 34), (250, horisont_y - 12), (390, horisont_y - 28),
         (540, horisont_y - 10), (bredd, horisont_y - 24), (bredd, horisont_y), (0, horisont_y)],
    )

    # Små skrothögar i bakgrunden längs horisonten
    rng_bak = random.Random(101)
    for bx in range(30, bredd - 30, 58):
        bh = rng_bak.randint(10, 22)
        bw = rng_bak.randint(24, 46)
        pygame.draw.polygon(
            yta,
            rng_bak.choice([(118, 96, 78), (96, 102, 108), (132, 104, 72)]),
            [(bx, horisont_y + 4), (bx + bw // 3, horisont_y - bh), (bx + (2 * bw) // 3, horisont_y - bh // 2), (bx + bw, horisont_y + 4)],
        )

    # Gräsmatta och grusgård
    pygame.draw.rect(yta, (92, 152, 74), (0, horisont_y, bredd, hojd - horisont_y))

    # Grusplan i mitten där man arbetar och bygger maskiner
    grus_rect = pygame.Rect(22, horisont_y + 24, bredd - 44, hojd - horisont_y - 42)
    pygame.draw.ellipse(yta, (176, 158, 126), grus_rect)
    pygame.draw.ellipse(yta, (148, 130, 100), grus_rect, width=3)

    # Grässtrån och småstenar för liv i gården
    rng = random.Random(77)
    for _ in range(95):
        gx = rng.randint(10, bredd - 10)
        gy = rng.randint(horisont_y + 6, hojd - 8)
        if grus_rect.collidepoint(gx, gy):
            pygame.draw.circle(yta, (132, 116, 88), (gx, gy), rng.randint(1, 3))
        else:
            pygame.draw.line(yta, (68, 124, 54), (gx, gy), (gx + rng.randint(-3, 3), gy - rng.randint(4, 9)), 2)

    # Enkelt gårdstaket längs kanten
    staket_y = horisont_y + 10
    pygame.draw.line(yta, (138, 104, 68), (0, staket_y + 5), (bredd, staket_y + 5), 3)
    pygame.draw.line(yta, (138, 104, 68), (0, staket_y + 13), (bredd, staket_y + 13), 3)
    for sx in range(18, bredd, 46):
        pygame.draw.rect(yta, (152, 116, 76), (sx, staket_y - 4, 7, 24), border_radius=2)

    return yta


def skapa_skrothog_textur(storlek: int = 205) -> pygame.Surface:
    """Skapar en detaljrik textur av en skrothög med balkar, kugghjul och rör."""
    yta = pygame.Surface((storlek, storlek), pygame.SRCALPHA)
    rng = random.Random(42)

    pygame.draw.ellipse(yta, (45, 42, 34, 125), (16, storlek - 44, storlek - 32, 32))

    farger = [
        (146, 88, 54),
        (112, 120, 132),
        (182, 114, 48),
        (86, 94, 108),
        (202, 162, 56),
    ]

    for _ in range(18):
        farg = rng.choice(farger)
        w = rng.randint(34, 82)
        h = rng.randint(14, 32)
        x = rng.randint(26, storlek - w - 26)
        y = rng.randint(50, storlek - h - 24)
        rect = pygame.Rect(x, y, w, h)
        pygame.draw.rect(yta, farg, rect, border_radius=4)
        pygame.draw.rect(yta, (32, 34, 40), rect, width=2, border_radius=4)

    for cx, cy, radie in [(70, 124, 21), (136, 112, 25), (104, 84, 17)]:
        pygame.draw.circle(yta, (128, 136, 148), (cx, cy), radie)
        pygame.draw.circle(yta, (48, 52, 60), (cx, cy), radie // 2)
        for i in range(8):
            vinkel = i * (math.pi / 4)
            tx = cx + math.cos(vinkel) * (radie + 4)
            ty = cy + math.sin(vinkel) * (radie + 4)
            pygame.draw.circle(yta, (148, 156, 168), (int(tx), int(ty)), 5)

    return yta


def skapa_robot_textur(storlek: int = 58) -> pygame.Surface:
    """Skapar en sorteringsrobot för automationen."""
    yta = pygame.Surface((storlek, storlek), pygame.SRCALPHA)
    pygame.draw.ellipse(yta, (35, 34, 28, 110), (10, storlek - 13, storlek - 20, 9))
    pygame.draw.rect(yta, (46, 52, 60), (11, storlek - 19, storlek - 22, 9), border_radius=4)
    pygame.draw.rect(yta, (62, 142, 192), (13, 16, storlek - 26, storlek - 31), border_radius=7)
    pygame.draw.rect(yta, (24, 38, 52), (13, 16, storlek - 26, storlek - 31), width=2, border_radius=7)
    pygame.draw.rect(yta, (125, 248, 215), (19, 23, storlek - 38, 9), border_radius=4)
    pygame.draw.line(yta, (215, 222, 230), (storlek // 2, 16), (storlek // 2, 6), 2)
    pygame.draw.circle(yta, (255, 188, 55), (storlek // 2, 5), 4)
    return yta


def skapa_transportband_textur(bredd: int = 96, hojd: int = 42) -> pygame.Surface:
    """Skapar ett litet transportband som fraktar skrot."""
    yta = pygame.Surface((bredd, hojd), pygame.SRCALPHA)
    pygame.draw.ellipse(yta, (35, 34, 28, 100), (6, hojd - 10, bredd - 12, 9))
    pygame.draw.rect(yta, (68, 74, 84), (4, 8, bredd - 8, hojd - 16), border_radius=12)
    pygame.draw.rect(yta, (34, 38, 44), (4, 8, bredd - 8, hojd - 16), width=2, border_radius=12)
    for rx in range(14, bredd - 10, 18):
        pygame.draw.circle(yta, (150, 158, 170), (rx, hojd // 2), 4)
    return yta


def skapa_ugn_textur(storlek: int = 86, aktiv: bool = True) -> pygame.Surface:
    """Skapar en smältugn som glöder när den är aktiv."""
    yta = pygame.Surface((storlek, storlek), pygame.SRCALPHA)
    pygame.draw.ellipse(yta, (35, 34, 28, 110), (12, storlek - 14, storlek - 24, 10))
    pygame.draw.rect(yta, (78, 84, 94), (storlek - 26, 5, 13, 26), border_radius=3)
    pygame.draw.rect(yta, (98, 104, 116), (11, 24, storlek - 22, storlek - 34), border_radius=7)
    pygame.draw.rect(yta, (30, 34, 40), (11, 24, storlek - 22, storlek - 34), width=2, border_radius=7)
    glod_farg = (255, 132, 30) if aktiv else (66, 58, 54)
    pygame.draw.rect(yta, (38, 40, 46), (22, 39, storlek - 44, 28), border_radius=5)
    pygame.draw.rect(yta, glod_farg, (26, 43, storlek - 52, 20), border_radius=4)
    return yta


def skapa_kross_textur(storlek: int = 84) -> pygame.Surface:
    """Skapar en skrotpress/kross som komprimerar metall."""
    yta = pygame.Surface((storlek, storlek), pygame.SRCALPHA)
    pygame.draw.ellipse(yta, (35, 34, 28, 110), (10, storlek - 14, storlek - 20, 10))
    # Pelare
    pygame.draw.rect(yta, (84, 92, 104), (14, 14, 12, storlek - 24), border_radius=3)
    pygame.draw.rect(yta, (84, 92, 104), (storlek - 26, 14, 12, storlek - 24), border_radius=3)
    # Toppbalk
    pygame.draw.rect(yta, (198, 142, 42), (10, 10, storlek - 20, 16), border_radius=4)
    # Presshuvud
    pygame.draw.rect(yta, (124, 132, 144), (26, 30, storlek - 52, 18), border_radius=4)
    # Skrotbit under pressen
    pygame.draw.rect(yta, (165, 92, 56), (28, storlek - 24, storlek - 56, 10), border_radius=3)
    return yta