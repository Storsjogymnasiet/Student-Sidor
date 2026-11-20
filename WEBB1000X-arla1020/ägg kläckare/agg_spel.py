import random
import pygame

pygame.init()

BREDD, HOJD = 800, 520
skarm = pygame.display.set_mode((BREDD, HOJD))
pygame.display.set_caption("Äggkläckaren – 2D Spel")
klocka = pygame.time.Clock()

# Färger
BAKGRUND = (24, 27, 38)
KORT_BG = (38, 43, 60)
TEXT_VIT = (240, 242, 248)
TEXT_GRÅ = (165, 175, 195)
GRÖN = (64, 185, 130)
GULD = (245, 195, 65)
LILA = (175, 95, 235)
BLÅ = (80, 165, 245)
RÖD = (225, 85, 95)

RARITET_FÄRG = {
    "Vanlig": (190, 198, 210),
    "Ovanlig": (85, 205, 120),
    "Sällsynt": (85, 165, 250),
    "Episk": (185, 100, 245),
    "Legendarisk": (250, 195, 55),
}

# Typsnitt
font_stor = pygame.font.SysFont("arial", 28, bold=True)
font_medel = pygame.font.SysFont("arial", 20, bold=True)
font_liten = pygame.font.SysFont("arial", 16)

# Speldata
mynt = 60
agg_niva = 1
lycka_niva = 1
samling = []  # lista av dicts: {"namn", "raritet", "varde"}
senaste_drop = None
meddelande = "Klicka på 'Kläck ägg' för att börja!"
meddelande_farg = TEXT_GRÅ

# Animation för ägget
skak_tid = 0.0

AGG_TYPER = {
    1: {"namn": "Vanligt Ägg", "pris": 25, "farg": (235, 225, 200)},
    2: {"namn": "Skogsägg", "pris": 75, "farg": (110, 195, 125)},
    3: {"namn": "Kristallägg", "pris": 180, "farg": (115, 200, 255)},
    4: {"namn": "Drakägg", "pris": 400, "farg": (235, 95, 85)},
}

SAKER_POOL = [
    {"namn": "Träpinne", "raritet": "Vanlig", "varde": 15, "vikt": 50},
    {"namn": "Skogsmus", "raritet": "Vanlig", "varde": 30, "vikt": 38},
    {"namn": "Glödande Svamp", "raritet": "Ovanlig", "varde": 70, "vikt": 24},
    {"namn": "Silverfjäder", "raritet": "Sällsynt", "varde": 165, "vikt": 12},
    {"namn": "Stjärndrake", "raritet": "Episk", "varde": 420, "vikt": 5},
    {"namn": "Solgudens Gnista", "raritet": "Legendarisk", "varde": 1100, "vikt": 1},
]


class Knapp:
    def __init__(self, rect, text, farg, aktiv=True):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.farg = farg
        self.aktiv = aktiv

    def rita(self, yta, mus_pos):
        hover = self.aktiv and self.rect.collidepoint(mus_pos)
        if not self.aktiv:
            bg = (65, 70, 85)
        elif hover:
            bg = tuple(min(255, c + 25) for c in self.farg)
        else:
            bg = self.farg

        pygame.draw.rect(yta, bg, self.rect, border_radius=10)
        pygame.draw.rect(yta, (255, 255, 255), self.rect, width=2, border_radius=10)

        txt = font_medel.render(self.text, True, TEXT_VIT if self.aktiv else TEXT_GRÅ)
        yta.blit(txt, txt.get_rect(center=self.rect.center))

    def klickad(self, event):
        return (
            self.aktiv
            and event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and self.rect.collidepoint(event.pos)
        )


def agg_kostnad():
    return agg_niva * 110


def lycka_kostnad():
    return lycka_niva * 90


def klacka_agg():
    global mynt, senaste_drop, meddelande, meddelande_farg, skak_tid

    agg = AGG_TYPER[agg_niva]
    if mynt < agg["pris"]:
        meddelande = f"Inte råd! {agg['namn']} kostar {agg['pris']} mynt."
        meddelande_farg = RÖD
        return

    mynt -= agg["pris"]
    skak_tid = 0.35

    vikter = []
    for idx, sak in enumerate(SAKER_POOL):
        bonus = 1 + (lycka_niva - 1) * 0.28 * (idx * 0.45)
        vikter.append(sak["vikt"] * bonus)

    vald = random.choices(SAKER_POOL, weights=vikter, k=1)[0]
    varde = int(vald["varde"] * (1 + (agg_niva - 1) * 0.45))

    drop = {"namn": vald["namn"], "raritet": vald["raritet"], "varde": varde}
    samling.append(drop)
    senaste_drop = drop

    meddelande = f"Du fick {drop['namn']} ({drop['raritet']}) – värde {drop['varde']} mynt!"
    meddelande_farg = RARITET_FÄRG.get(drop["raritet"], TEXT_VIT)


def uppgradera_agg():
    global mynt, agg_niva, meddelande, meddelande_farg
    if agg_niva >= max(AGG_TYPER.keys()):
        return
    kost = agg_kostnad()
    if mynt < kost:
        meddelande = f"Behöver {kost} mynt för att uppgradera ägg."
        meddelande_farg = RÖD
        return
    mynt -= kost
    agg_niva += 1
    meddelande = f"Nytt ägg upplåst: {AGG_TYPER[agg_niva]['namn']}!"
    meddelande_farg = GULD


def uppgradera_lycka():
    global mynt, lycka_niva, meddelande, meddelande_farg
    kost = lycka_kostnad()
    if mynt < kost:
        meddelande = f"Behöver {kost} mynt för bättre lycka."
        meddelande_farg = RÖD
        return
    mynt -= kost
    lycka_niva += 1
    meddelande = f"Lycka nivå {lycka_niva}! Högre chans på sällsynta saker."
    meddelande_farg = BLÅ


def salj_allt():
    global mynt, meddelande, meddelande_farg
    if not samling:
        return
    summa = sum(item["varde"] for item in samling)
    antal = len(samling)
    mynt += summa
    samling.clear()
    meddelande = f"Sålde {antal} saker för +{summa} mynt!"
    meddelande_farg = GRÖN


def rita_agg(yta, x, y, farg, skak_offset_x):
    cx = x + skak_offset_x
    # Själva ägget (oval form med två cirklar/ellipse)
    agg_rect = pygame.Rect(cx - 65, y - 85, 130, 170)
    pygame.draw.ellipse(yta, farg, agg_rect)
    pygame.draw.ellipse(yta, (255, 255, 255), agg_rect, width=3)

    # Liten glansdetalj
    glans = pygame.Rect(cx - 35, y - 55, 22, 42)
    pygame.draw.ellipse(yta, (255, 255, 255), glans)


# Knappar
knapp_klack = Knapp((70, 355, 240, 52), "Kläck ägg", GRÖN)
knapp_agg_upp = Knapp((70, 420, 240, 46), "Uppgradera ägg", LILA)
knapp_lycka_upp = Knapp((325, 420, 215, 46), "Uppgradera lycka", BLÅ)
knapp_salj = Knapp((555, 355, 200, 52), "Sälj allt", GULD)

kor = True
while kor:
    dt = klocka.tick(60) / 1000.0
    mus_pos = pygame.mouse.get_pos()

    if skak_tid > 0:
        skak_tid = max(0.0, skak_tid - dt)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            kor = False
        if knapp_klack.klickad(event):
            klacka_agg()
        elif knapp_agg_upp.klickad(event):
            uppgradera_agg()
        elif knapp_lycka_upp.klickad(event):
            uppgradera_lycka()
        elif knapp_salj.klickad(event):
            salj_allt()

    skarm.fill(BAKGRUND)

    # Topprad med status
    agg_info = AGG_TYPER[agg_niva]
    status_text = font_stor.render(
        f"Mynt: {mynt}   |   Ägg: {agg_info['namn']} (Lv.{agg_niva})   |   Lycka: Lv.{lycka_niva}",
        True,
        TEXT_VIT,
    )
    skarm.blit(status_text, (40, 22))

    # Vänster kort: Ägg & drop
    pygame.draw.rect(skarm, KORT_BG, (40, 75, 480, 255), border_radius=14)
    skak_x = random.randint(-7, 7) if skak_tid > 0 else 0
    rita_agg(skarm, 150, 205, agg_info["farg"], skak_x)

    pris_lbl = font_medel.render(f"Pris: {agg_info['pris']} mynt", True, GULD)
    skarm.blit(pris_lbl, (95, 298))

    if senaste_drop:
        r_farg = RARITET_FÄRG.get(senaste_drop["raritet"], TEXT_VIT)
        d_namn = font_stor.render(senaste_drop["namn"], True, r_farg)
        d_rar = font_medel.render(f"Raritet: {senaste_drop['raritet']}", True, r_farg)
        d_val = font_medel.render(f"Värde: {senaste_drop['varde']} mynt", True, TEXT_VIT)
        skarm.blit(d_namn, (250, 130))
        skarm.blit(d_rar, (250, 170))
        skarm.blit(d_val, (250, 202))
    else:
        ingen = font_medel.render("Inget kläckt ännu", True, TEXT_GRÅ)
        skarm.blit(ingen, (250, 175))

    # Höger kort: Ryggsäck / samling
    pygame.draw.rect(skarm, KORT_BG, (540, 75, 220, 255), border_radius=14)
    s_rubrik = font_medel.render(f"Samling ({len(samling)} st)", True, TEXT_VIT)
    skarm.blit(s_rubrik, (558, 92))

    total_varde = sum(item["varde"] for item in samling)
    s_summa = font_liten.render(f"Totalt värde: {total_varde} mynt", True, GULD)
    skarm.blit(s_summa, (558, 118))

    for i, item in enumerate(samling[-7:]):
        f = RARITET_FÄRG.get(item["raritet"], TEXT_VIT)
        rad = font_liten.render(f"• {item['namn']} ({item['varde']})", True, f)
        skarm.blit(rad, (558, 148 + i * 24))

    # Meddelanderad
    msg_surf = font_medel.render(meddelande, True, meddelande_farg)
    skarm.blit(msg_surf, (70, 476))

    # Uppdatera knapp-texter och aktivering
    knapp_klack.text = f"Kläck ägg ({agg_info['pris']})"
    knapp_klack.aktiv = mynt >= agg_info["pris"]

    if agg_niva >= max(AGG_TYPER.keys()):
        knapp_agg_upp.text = "Max äggnivå"
        knapp_agg_upp.aktiv = False
    else:
        k_agg = agg_kostnad()
        knapp_agg_upp.text = f"Uppgradera ägg ({k_agg})"
        knapp_agg_upp.aktiv = mynt >= k_agg

    k_lycka = lycka_kostnad()
    knapp_lycka_upp.text = f"Uppgradera lycka ({k_lycka})"
    knapp_lycka_upp.aktiv = mynt >= k_lycka

    knapp_salj.text = f"Sälj allt (+{total_varde})"
    knapp_salj.aktiv = len(samling) > 0

    for knapp in (knapp_klack, knapp_agg_upp, knapp_lycka_upp, knapp_salj):
        knapp.rita(skarm, mus_pos)

    pygame.display.flip()

pygame.quit()