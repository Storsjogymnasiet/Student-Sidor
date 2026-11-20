import array
import math
import random
import sys
import pygame

# --- INITIERING & LJUDSYNTES ---
pygame.mixer.pre_init(frequency=22050, size=-16, channels=1, buffer=512)
pygame.init()

WIDTH, HEIGHT = 920, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hydraulic Press Tycoon: Deluxe + Sound")
clock = pygame.time.Clock()


def make_sound(samples):
    """Skapar ett Pygame Sound-objekt från en lista med flyttal mellan -1.0 och 1.0."""
    sr = 22050
    buf = array.array("h")
    for s in samples:
        clamped = max(-1.0, min(1.0, s))
        buf.append(int(clamped * 32767))
    return pygame.mixer.Sound(buffer=buf.tobytes())


def generate_sfx():
    sr = 22050

    # 1. Tungt hydrauliskt dunk + svagt luftpys
    press_samples = []
    n_press = int(sr * 0.16)
    for i in range(n_press):
        t = i / sr
        env = math.exp(-t * 24)
        # Fallande lågfrekvent ton (130 Hz -> 42 Hz) + lite brus som pys
        freq = 42 + 88 * math.exp(-t * 28)
        tone = math.sin(2 * math.pi * freq * t) * 0.75
        hiss = random.uniform(-1, 1) * 0.22 * math.exp(-t * 15)
        press_samples.append((tone + hiss) * env)

    # 2. Kritisk värmeträff (skarpare punch + sprak)
    crit_samples = []
    n_crit = int(sr * 0.22)
    for i in range(n_crit):
        t = i / sr
        env = math.exp(-t * 16)
        freq = 65 + 190 * math.exp(-t * 22)
        punch = math.sin(2 * math.pi * freq * t) * 0.65
        crackle = random.uniform(-1, 1) * 0.45 * math.exp(-t * 10)
        crit_samples.append((punch + crackle) * env)

    # 3. Krasch när objekt går sönder
    smash_samples = []
    n_smash = int(sr * 0.32)
    for i in range(n_smash):
        t = i / sr
        env = math.exp(-t * 10)
        noise = random.uniform(-1, 1) * 0.7
        thud = math.sin(2 * math.pi * 55 * t) * 0.45 * math.exp(-t * 14)
        smash_samples.append((noise + thud) * env)

    # 4. Köp-ljud (två korta toner uppåt)
    buy_samples = []
    n_buy = int(sr * 0.18)
    for i in range(n_buy):
        t = i / sr
        env = math.exp(-t * 18)
        freq = 587.33 if t < 0.08 else 880.0  # D5 -> A5
        tone = math.sin(2 * math.pi * freq * t) * 0.45
        buy_samples.append(tone * env)

    return {
        "press": make_sound(press_samples),
        "crit": make_sound(crit_samples),
        "smash": make_sound(smash_samples),
        "buy": make_sound(buy_samples),
    }


sound_enabled = pygame.mixer.get_init() is not None
sfx = generate_sfx() if sound_enabled else {}
muted = False


def play_sfx(name):
    if sound_enabled and not muted and name in sfx:
        sfx[name].play()


# --- FÄRGPALETT ---
BG_DARK = (18, 20, 26)
PANEL_BG = (28, 32, 42)
CARD_BG = (38, 43, 56)
CARD_HOVER = (48, 55, 72)
STEEL_DARK = (55, 62, 75)
STEEL_MID = (100, 110, 130)
STEEL_LIGHT = (170, 180, 200)
GOLD = (245, 185, 45)
ORANGE = (240, 110, 30)
RED_GLOW = (255, 60, 40)
GREEN = (50, 190, 100)
CYAN = (60, 210, 240)
WHITE = (245, 245, 250)
GRAY_TEXT = (160, 170, 185)

font_xl = pygame.font.SysFont("segoeui", 32, bold=True)
font_lg = pygame.font.SysFont("segoeui", 22, bold=True)
font_md = pygame.font.SysFont("segoeui", 16, bold=True)
font_sm = pygame.font.SysFont("segoeui", 13)

# --- SPELVARIABLER ---
money = 0
shake_timer = 0.0
shake_intensity = 0

press_power = 12
auto_speed = 0.0
auto_efficiency = 0.5
crit_chance = 0.0
heat_level = 0
scrap_mult = 1.0
material_tier = 1

auto_timer = 0.0
press_y_offset = 0.0
gauge_angle = 0.0

upgrades = [
    {
        "id": "power",
        "name": "Hydraulik-tryck",
        "desc": "Ökar manuell presskraft",
        "level": 1,
        "cost": 15,
        "cost_mult": 1.55,
        "color": ORANGE,
    },
    {
        "id": "auto",
        "name": "Autopress-motor",
        "desc": "+0.5 auto-tryck / sek",
        "level": 0,
        "cost": 40,
        "cost_mult": 1.65,
        "color": CYAN,
    },
    {
        "id": "scrap",
        "name": "Skrot-sortering",
        "desc": "+25% mer pengar per sak",
        "level": 1,
        "cost": 65,
        "cost_mult": 1.75,
        "color": GOLD,
    },
    {
        "id": "heat",
        "name": "Värmeslingor",
        "desc": "+6% chans för 2.5x Kritisk Hätta",
        "level": 0,
        "cost": 100,
        "cost_mult": 1.80,
        "color": RED_GLOW,
    },
    {
        "id": "auto_eff",
        "name": "Dubbelkolv (Auto)",
        "desc": "Autopress gör mer skada",
        "level": 1,
        "cost": 150,
        "cost_mult": 1.85,
        "color": (130, 140, 255),
    },
    {
        "id": "tier",
        "name": "Leverantörsavtal",
        "desc": "Låser upp dyrare objekt",
        "level": 1,
        "cost": 250,
        "cost_mult": 2.60,
        "color": GREEN,
    },
]

ITEMS = [
    ("Läskburk", 25, 6, (210, 45, 45), (230, 230, 230), 48, 75, "can"),
    ("Gammal Brödrost", 70, 18, (180, 185, 195), (40, 40, 45), 85, 65, "box"),
    ("Ek-kub", 160, 45, (150, 95, 45), (110, 65, 25), 80, 80, "wood"),
    ("Bowlingklot", 380, 115, (35, 55, 175), (15, 20, 40), 90, 90, "bowling"),
    ("Kassaskåp", 950, 310, (75, 85, 95), (210, 175, 55), 110, 110, "safe"),
    ("Guld-tacka", 2400, 850, (245, 190, 40), (255, 235, 130), 120, 65, "gold"),
    ("Diamantkristall", 6000, 2300, (70, 220, 245), (200, 250, 255), 95, 95, "diamond"),
    ("Nukleär Kärna", 16000, 6500, (50, 230, 90), (20, 40, 25), 105, 105, "nuclear"),
]

current_item = None
item_hp = 0
particles = []
floating_texts = []
upgrade_rects = []


# --- HJÄLPFUNKTIONER ---
def draw_metallic_rect(surface, rect, base_color, border_radius=0):
    pygame.draw.rect(surface, base_color, rect, border_radius=border_radius)
    highlight = tuple(min(255, c + 35) for c in base_color)
    shadow = tuple(max(0, c - 35) for c in base_color)
    if rect.width > 12:
        hl_rect = pygame.Rect(rect.x + 3, rect.y + 2, max(2, rect.width // 6), rect.height - 4)
        pygame.draw.rect(surface, highlight, hl_rect, border_radius=border_radius)
        sh_rect = pygame.Rect(rect.right - max(3, rect.width // 6) - 2, rect.y + 2, max(2, rect.width // 6), rect.height - 4)
        pygame.draw.rect(surface, shadow, sh_rect, border_radius=border_radius)


def spawn_item():
    global current_item, item_hp
    max_idx = min(len(ITEMS) - 1, material_tier)
    min_idx = max(0, max_idx - 2)
    idx = random.randint(min_idx, max_idx)
    current_item = ITEMS[idx]
    item_hp = current_item[1]


def add_floating_text(x, y, text, color, is_crit=False):
    floating_texts.append({
        "x": x + random.randint(-25, 25),
        "y": y,
        "text": text,
        "color": color,
        "life": 1.0,
        "vy": -65 if is_crit else -45,
        "font": font_lg if is_crit else font_md,
    })


def press_action(base_damage, is_auto=False):
    global money, item_hp, press_y_offset, shake_timer, shake_intensity, gauge_angle

    is_crit = random.random() < crit_chance
    damage = int(base_damage * (2.5 if is_crit else 1.0))
    damage = max(1, damage)

    item_hp -= damage
    press_y_offset = 40 if not is_auto else 22
    gauge_angle = min(140, 30 + (damage / 5))

    if not is_auto or is_crit:
        shake_timer = 0.12 if is_crit else 0.06
        shake_intensity = 6 if is_crit else 3

    if is_crit:
        play_sfx("crit")
    elif not is_auto:
        play_sfx("press")

    dmg_str = f"-{damage}!" if is_crit else f"-{damage}"
    dmg_col = RED_GLOW if is_crit else (CYAN if is_auto else WHITE)
    add_floating_text(245, 380, dmg_str, dmg_col, is_crit)

    p_count = 14 if is_crit else (4 if is_auto else 7)
    for _ in range(p_count):
        p_col = random.choice([RED_GLOW, ORANGE, GOLD]) if is_crit else random.choice([GOLD, WHITE, ORANGE])
        particles.append({
            "x": 245 + random.randint(-45, 45),
            "y": 445,
            "vx": random.uniform(-4.5, 4.5),
            "vy": random.uniform(-5.5, -1.5),
            "life": random.randint(18, 35),
            "color": p_col,
            "size": random.randint(2, 5),
        })

    if item_hp <= 0:
        play_sfx("smash")
        reward = int(current_item[2] * scrap_mult)
        money += reward
        add_floating_text(245, 330, f"+{reward} kr", GREEN, True)
        shake_timer = 0.18
        shake_intensity = 7

        for _ in range(28):
            particles.append({
                "x": 245 + random.randint(-40, 40),
                "y": 440,
                "vx": random.uniform(-7, 7),
                "vy": random.uniform(-8, -2),
                "life": random.randint(25, 50),
                "color": random.choice([current_item[3], current_item[4], GOLD]),
                "size": random.randint(3, 6),
            })
        spawn_item()


def buy_upgrade(upg):
    global money, press_power, auto_speed, scrap_mult, crit_chance, heat_level, auto_efficiency, material_tier

    if money < upg["cost"]:
        return
    if upg["id"] == "heat" and crit_chance >= 0.72:
        return
    if upg["id"] == "tier" and material_tier >= len(ITEMS) - 1:
        return

    money -= upg["cost"]
    upg["level"] += 1
    upg["cost"] = int(upg["cost"] * upg["cost_mult"])
    play_sfx("buy")

    if upg["id"] == "power":
        press_power = int(press_power * 1.35) + 6
    elif upg["id"] == "auto":
        auto_speed += 0.5
    elif upg["id"] == "scrap":
        scrap_mult += 0.25
    elif upg["id"] == "heat":
        crit_chance = min(0.75, crit_chance + 0.06)
        heat_level += 1
    elif upg["id"] == "auto_eff":
        auto_efficiency += 0.25
    elif upg["id"] == "tier":
        material_tier += 1
        spawn_item()


def draw_item(surface, rect, item_data):
    _, _, _, c1, c2, _, _, itype = item_data
    pygame.draw.rect(surface, c1, rect, border_radius=6)

    if itype == "can":
        pygame.draw.rect(surface, c2, (rect.x, rect.y, rect.width, 6), border_radius=2)
        pygame.draw.rect(surface, c2, (rect.x, rect.bottom - 6, rect.width, 6), border_radius=2)
        pygame.draw.line(surface, c2, (rect.x + 4, rect.centery), (rect.right - 4, rect.centery), 4)
    elif itype == "wood":
        pygame.draw.rect(surface, c2, rect, 3, border_radius=4)
        pygame.draw.line(surface, c2, (rect.x + 8, rect.y + 8), (rect.right - 8, rect.bottom - 8), 2)
    elif itype == "bowling":
        for dx, dy in [(-10, -8), (10, -8), (0, 6)]:
            if rect.height > 25:
                pygame.draw.circle(surface, c2, (rect.centerx + dx, rect.centery + dy), 5)
    elif itype == "safe":
        pygame.draw.rect(surface, c2, rect, 4, border_radius=4)
        if rect.height > 30:
            pygame.draw.circle(surface, c2, rect.center, min(14, rect.height // 3), 3)
    elif itype in ("gold", "diamond", "nuclear"):
        inner = rect.inflate(-rect.width // 3, -rect.height // 3)
        pygame.draw.rect(surface, c2, inner, border_radius=4)

    pygame.draw.rect(surface, (20, 20, 25), rect, 2, border_radius=6)


def draw_gauge(surface, center, radius, angle_deg):
    pygame.draw.circle(surface, (230, 230, 220), center, radius)
    pygame.draw.circle(surface, STEEL_DARK, center, radius, 4)
    pygame.draw.arc(
        surface,
        RED_GLOW,
        (center[0] - radius + 5, center[1] - radius + 5, (radius - 5) * 2, (radius - 5) * 2),
        0,
        1.2,
        4,
    )
    rad = math.radians(180 - angle_deg)
    end_x = center[0] + int((radius - 8) * math.cos(rad))
    end_y = center[1] - int((radius - 8) * math.sin(rad))
    pygame.draw.line(surface, RED_GLOW, center, (end_x, end_y), 3)
    pygame.draw.circle(surface, STEEL_DARK, center, 4)


spawn_item()

# --- HUVUDLOOP ---
running = True
while running:
    dt = clock.tick(60) / 1000.0
    mx, my = pygame.mouse.get_pos()

    press_zone = pygame.Rect(25, 25, 440, 600)
    mute_btn = pygame.Rect(795, 38, 80, 32)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                press_action(press_power, is_auto=False)
            elif event.key == pygame.K_m:
                muted = not muted

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if mute_btn.collidepoint(mx, my):
                muted = not muted
            elif press_zone.collidepoint(mx, my):
                press_action(press_power, is_auto=False)
            else:
                for idx, rect in enumerate(upgrade_rects):
                    if rect.collidepoint(mx, my):
                        buy_upgrade(upgrades[idx])

    if auto_speed > 0:
        auto_timer += dt
        interval = 1.0 / auto_speed
        if auto_timer >= interval:
            auto_timer -= interval
            press_action(int(press_power * auto_efficiency), is_auto=True)

    if press_y_offset > 0:
        press_y_offset = max(0.0, press_y_offset - 220 * dt)
    if gauge_angle > 15:
        gauge_angle = max(15.0, gauge_angle - 120 * dt)
    if shake_timer > 0:
        shake_timer = max(0.0, shake_timer - dt)

    for p in particles[:]:
        p["x"] += p["vx"]
        p["y"] += p["vy"]
        p["vy"] += 0.35
        p["life"] -= 1
        if p["life"] <= 0:
            particles.remove(p)

    for ft in floating_texts[:]:
        ft["y"] += ft["vy"] * dt
        ft["life"] -= dt
        if ft["life"] <= 0:
            floating_texts.remove(ft)

    canvas = pygame.Surface((WIDTH, HEIGHT))
    canvas.fill(BG_DARK)

    # --- VÄNSTER PANEL ---
    pygame.draw.rect(canvas, PANEL_BG, press_zone, border_radius=14)
    pygame.draw.rect(canvas, STEEL_DARK, press_zone, 2, border_radius=14)

    stripe_y = 515
    pygame.draw.rect(canvas, (35, 35, 40), (45, stripe_y, 400, 22))
    for sx in range(50, 430, 30):
        pygame.draw.polygon(
            canvas,
            GOLD,
            [(sx, stripe_y + 22), (sx + 15, stripe_y + 22), (sx + 25, stripe_y), (sx + 10, stripe_y)],
        )

    draw_metallic_rect(canvas, pygame.Rect(65, 70, 28, 445), STEEL_MID)
    draw_metallic_rect(canvas, pygame.Rect(397, 70, 28, 445), STEEL_MID)
    draw_metallic_rect(canvas, pygame.Rect(55, 55, 380, 35), STEEL_DARK, border_radius=6)
    draw_metallic_rect(canvas, pygame.Rect(95, 475, 300, 40), STEEL_DARK, border_radius=4)
    draw_metallic_rect(canvas, pygame.Rect(115, 462, 260, 14), STEEL_LIGHT, border_radius=3)

    draw_gauge(canvas, (355, 130), 26, gauge_angle)

    hp_ratio = max(0.14, item_hp / current_item[1])
    cur_h = int(current_item[6] * hp_ratio)
    cur_w = int(current_item[5] * (1.85 - hp_ratio * 0.85))
    item_rect = pygame.Rect(245 - cur_w // 2, 462 - cur_h, cur_w, cur_h)
    draw_item(canvas, item_rect, current_item)

    piston_y = min(462 - cur_h, (462 - cur_h) - 18 + press_y_offset)
    draw_metallic_rect(canvas, pygame.Rect(185, 90, 120, 110), STEEL_DARK, border_radius=6)
    rod_h = max(10, int(piston_y - 200))
    draw_metallic_rect(canvas, pygame.Rect(220, 200, 50, rod_h), STEEL_LIGHT)

    head_rect = pygame.Rect(150, int(piston_y - 26), 190, 26)
    draw_metallic_rect(canvas, head_rect, ORANGE, border_radius=4)
    if heat_level > 0:
        glow_h = min(10, 3 + heat_level)
        pygame.draw.rect(canvas, RED_GLOW, (head_rect.x + 6, head_rect.bottom - glow_h, head_rect.width - 12, glow_h), border_radius=2)

    for p in particles:
        pygame.draw.circle(canvas, p["color"], (int(p["x"]), int(p["y"])), p["size"])

    for ft in floating_texts:
        txt_s = ft["font"].render(ft["text"], True, ft["color"])
        canvas.blit(txt_s, (ft["x"] - txt_s.get_width() // 2, int(ft["y"])))

    name_s = font_lg.render(current_item[0], True, WHITE)
    canvas.blit(name_s, (245 - name_s.get_width() // 2, 545))

    bar_bg = pygame.Rect(115, 580, 260, 18)
    pygame.draw.rect(canvas, (15, 18, 22), bar_bg, border_radius=9)
    fill_w = int(260 * max(0, item_hp / current_item[1]))
    if fill_w > 0:
        pygame.draw.rect(canvas, GREEN if hp_ratio > 0.3 else RED_GLOW, (115, 580, fill_w, 18), border_radius=9)
    hp_s = font_sm.render(f"{max(0, item_hp)} / {current_item[1]} HP", True, WHITE)
    canvas.blit(hp_s, (245 - hp_s.get_width() // 2, 580))

    # --- HÖGER PANEL ---
    shop_panel = pygame.Rect(485, 25, 410, 600)
    pygame.draw.rect(canvas, PANEL_BG, shop_panel, border_radius=14)
    pygame.draw.rect(canvas, STEEL_DARK, shop_panel, 2, border_radius=14)

    money_s = font_xl.render(f"{money:,} kr".replace(",", " "), True, GOLD)
    canvas.blit(money_s, (505, 38))

    # Ljudknapp (M)
    pygame.draw.rect(canvas, STEEL_DARK if muted else STEEL_MID, mute_btn, border_radius=6)
    mute_lbl = font_sm.render("Ljud: AV" if muted else "Ljud: PÅ", True, WHITE)
    canvas.blit(mute_lbl, (mute_btn.centerx - mute_lbl.get_width() // 2, mute_btn.centery - mute_lbl.get_height() // 2))

    auto_dmg = int(press_power * auto_efficiency) if auto_speed > 0 else 0
    stats_line1 = font_sm.render(f"Kraft: {press_power} ton   |   Auto: {auto_speed:.1f}/s ({auto_dmg} skada)", True, GRAY_TEXT)
    stats_line2 = font_sm.render(f"Värde: {int(scrap_mult * 100)}%   |   Kritisk Hätta: {int(crit_chance * 100)}%  (M = Mute)", True, GRAY_TEXT)
    canvas.blit(stats_line1, (505, 82))
    canvas.blit(stats_line2, (505, 102))

    pygame.draw.line(canvas, STEEL_DARK, (505, 128), (875, 128), 2)

    upgrade_rects = []
    start_y = 140
    card_h = 72
    gap = 8

    for i, upg in enumerate(upgrades):
        rect = pygame.Rect(500, start_y + i * (card_h + gap), 380, card_h)
        upgrade_rects.append(rect)

        is_maxed = (upg["id"] == "heat" and crit_chance >= 0.72) or (upg["id"] == "tier" and material_tier >= len(ITEMS) - 1)
        can_afford = money >= upg["cost"] and not is_maxed
        is_hovered = rect.collidepoint(mx, my)

        bg = CARD_HOVER if (is_hovered and can_afford) else CARD_BG
        pygame.draw.rect(canvas, bg, rect, border_radius=10)
        border_col = upg["color"] if can_afford else STEEL_DARK
        pygame.draw.rect(canvas, border_col, rect, 2, border_radius=10)

        pygame.draw.rect(canvas, upg["color"], (rect.x + 6, rect.y + 10, 6, rect.height - 20), border_radius=3)

        title_s = font_md.render(f"{upg['name']}  (Nivå {upg['level']})", True, WHITE)
        desc_s = font_sm.render(upg["desc"], True, GRAY_TEXT)
        canvas.blit(title_s, (rect.x + 22, rect.y + 12))
        canvas.blit(desc_s, (rect.x + 22, rect.y + 38))

        btn_rect = pygame.Rect(rect.right - 115, rect.y + 16, 102, 40)
        btn_col = GREEN if can_afford else (50, 55, 65)
        pygame.draw.rect(canvas, btn_col, btn_rect, border_radius=6)

        cost_label = "MAX" if is_maxed else f"{upg['cost']:,} kr".replace(",", " ")
        cost_s = font_md.render(cost_label, True, WHITE if can_afford else GRAY_TEXT)
        canvas.blit(cost_s, (btn_rect.centerx - cost_s.get_width() // 2, btn_rect.centery - cost_s.get_height() // 2))

    ox = random.randint(-shake_intensity, shake_intensity) if shake_timer > 0 else 0
    oy = random.randint(-shake_intensity, shake_intensity) if shake_timer > 0 else 0
    screen.blit(canvas, (ox, oy))

    pygame.display.flip()

pygame.quit()
sys.exit()