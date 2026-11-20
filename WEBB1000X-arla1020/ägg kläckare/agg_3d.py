import random
from ursina import *

app = Ursina(title="Äggkläckaren 3D", borderless=False)
window.size = (960, 600)
window.color = color.rgb(18, 22, 34)

# Spelstatus
mynt = 75
agg_niva = 1
lycka_niva = 1
samling = []
skak_tid = 0.0

AGG_TYPER = {
    1: {"namn": "Vanligt Ägg", "pris": 25, "farg": color.rgb(235, 225, 200), "skala": (1.3, 1.75, 1.3)},
    2: {"namn": "Skogsägg", "pris": 75, "farg": color.rgb(90, 205, 120), "skala": (1.4, 1.9, 1.4)},
    3: {"namn": "Kristallägg", "pris": 180, "farg": color.rgb(95, 195, 255), "skala": (1.5, 2.05, 1.5)},
    4: {"namn": "Drakägg", "pris": 400, "farg": color.rgb(240, 85, 85), "skala": (1.65, 2.25, 1.65)},
}

SAKER_POOL = [
    {"namn": "Träpinne", "raritet": "Vanlig", "varde": 15, "vikt": 50, "farg": color.brown, "form": "cube"},
    {"namn": "Skogsmus", "raritet": "Vanlig", "varde": 30, "vikt": 38, "farg": color.light_gray, "form": "sphere"},
    {"namn": "Glödande Svamp", "raritet": "Ovanlig", "varde": 70, "vikt": 24, "farg": color.lime, "form": "cylinder"},
    {"namn": "Silverfjäder", "raritet": "Sällsynt", "varde": 165, "vikt": 12, "farg": color.cyan, "form": "diamond"},
    {"namn": "Stjärndrake", "raritet": "Episk", "varde": 420, "vikt": 5, "farg": color.magenta, "form": "sphere"},
    {"namn": "Solgudens Gnista", "raritet": "Legendarisk", "varde": 1100, "vikt": 1, "farg": color.gold, "form": "diamond"},
]

# Golv och ljus för bättre 3D-djup
golv = Entity(
    model="cylinder",
    scale=(12, 0.25, 12),
    position=(0, -1.6, 0),
    color=color.rgb(34, 40, 58),
    texture="brick",
    texture_scale=(6, 6),
)

sol_ljus = DirectionalLight(y=8, z=-5, shadows=True)
sol_ljus.look_at((0, 0, 0))
AmbientLight(color=color.rgba(140, 150, 180, 120))

# Själva 3D-ägget
agg_3d = Entity(
    model="sphere",
    color=AGG_TYPER[1]["farg"],
    scale=AGG_TYPER[1]["skala"],
    position=(-1.2, -0.2, 0),
    specular=0.6,
)

# 3D-föremålet som visas när du kläcker
drop_3d = Entity(
    model="diamond",
    color=color.gold,
    scale=0.001,
    position=(1.6, 0.2, 0),
    specular=0.8,
)

# Kamera som går att vrida med högerklick
kamera_kontroll = EditorCamera(enabled=True, move_speed=0, zoom_speed=1.2)
kamera_kontroll.position = (0, 0.6, -8.5)
kamera_kontroll.rotation = (8, 0, 0)

# UI-texter
hud_topp = Text(
    text="",
    position=(-0.85, 0.45),
    scale=1.3,
    color=color.white,
)
drop_text = Text(
    text="Klicka på 'Kläck ägg'!",
    position=(0.18, 0.25),
    scale=1.2,
    color=color.light_gray,
)
status_text = Text(
    text="",
    position=(-0.85, -0.36),
    scale=1.15,
    color=color.gold,
)


def agg_kostnad():
    return agg_niva * 110


def lycka_kostnad():
    return lycka_niva * 90


def uppdatera_hud():
    agg = AGG_TYPER[agg_niva]
    agg_3d.color = agg["farg"]
    agg_3d.scale = agg["skala"]

    total_varde = sum(x["varde"] for x in samling)
    hud_topp.text = (
        f"Mynt: {mynt}   |   Ägg: {agg['namn']} (Lv.{agg_niva})   |   "
        f"Lycka: Lv.{lycka_niva}   |   Samling: {len(samling)} st ({total_varde} mynt)"
    )

    knapp_klack.text = f"Kläck ägg ({agg['pris']})"
    if agg_niva >= max(AGG_TYPER.keys()):
        knapp_agg.text = "Max äggnivå"
    else:
        knapp_agg.text = f"Uppgradera ägg ({agg_kostnad()})"

    knapp_lycka.text = f"Uppgradera lycka ({lycka_kostnad()})"
    knapp_salj.text = f"Sälj allt (+{total_varde})"


def klacka_agg():
    global mynt, skak_tid

    agg = AGG_TYPER[agg_niva]
    if mynt < agg["pris"]:
        status_text.text = f"Inte råd! {agg['namn']} kostar {agg['pris']} mynt."
        status_text.color = color.red
        return

    mynt -= agg["pris"]
    skak_tid = 0.45

    vikter = []
    for idx, sak in enumerate(SAKER_POOL):
        bonus = 1 + (lycka_niva - 1) * 0.28 * (idx * 0.45)
        vikter.append(sak["vikt"] * bonus)

    vald = random.choices(SAKER_POOL, weights=vikter, k=1)[0]
    varde = int(vald["varde"] * (1 + (agg_niva - 1) * 0.45))

    post = {"namn": vald["namn"], "raritet": vald["raritet"], "varde": varde}
    samling.append(post)

    # Uppdatera 3D-föremålet
    drop_3d.model = vald["form"]
    drop_3d.color = vald["farg"]
    drop_3d.scale = 0.2
    drop_3d.animate_scale(1.15, duration=0.25, curve=curve.out_back)

    drop_text.text = f"{vald['namn']}\n[{vald['raritet']}]\nVärde: {varde} mynt"
    drop_text.color = vald["farg"]
    status_text.text = f"Du kläckte {vald['namn']} för {varde} mynt!"
    status_text.color = color.lime
    uppdatera_hud()


def uppgradera_agg():
    global mynt, agg_niva
    if agg_niva >= max(AGG_TYPER.keys()):
        status_text.text = "Du har redan högsta äggnivån!"
        return
    kost = agg_kostnad()
    if mynt < kost:
        status_text.text = f"Behöver {kost} mynt för att uppgradera ägg."
        status_text.color = color.red
        return
    mynt -= kost
    agg_niva += 1
    status_text.text = f"Nytt 3D-ägg upplåst: {AGG_TYPER[agg_niva]['namn']}!"
    status_text.color = color.gold
    uppdatera_hud()


def uppgradera_lycka():
    global mynt, lycka_niva
    kost = lycka_kostnad()
    if mynt < kost:
        status_text.text = f"Behöver {kost} mynt för bättre lycka."
        status_text.color = color.red
        return
    mynt -= kost
    lycka_niva += 1
    status_text.text = f"Lycka nivå {lycka_niva}! Bättre chans på sällsynta saker."
    status_text.color = color.cyan
    uppdatera_hud()


def salj_allt():
    global mynt
    if not samling:
        status_text.text = "Din samling är tom."
        return
    summa = sum(x["varde"] for x in samling)
    antal = len(samling)
    mynt += summa
    samling.clear()
    status_text.text = f"Sålde {antal} saker för +{summa} mynt!"
    status_text.color = color.gold
    uppdatera_hud()


# Knappar i nedre delen av skärmen
knapp_klack = Button(text="Kläck ägg", position=(-0.62, -0.45), scale=(0.28, 0.075), color=color.azure, on_click=klacka_agg)
knapp_agg = Button(text="Uppgradera ägg", position=(-0.24, -0.45), scale=(0.34, 0.075), color=color.violet, on_click=uppgradera_agg)
knapp_lycka = Button(text="Uppgradera lycka", position=(0.18, -0.45), scale=(0.36, 0.075), color=color.cyan, on_click=uppgradera_lycka)
knapp_salj = Button(text="Sälj allt", position=(0.62, -0.45), scale=(0.28, 0.075), color=color.gold, on_click=salj_allt)


def update():
    global skak_tid

    # Snurra ägget och det kläckta föremålet i 3D
    agg_3d.rotation_y += 55 * time.dt
    drop_3d.rotation_y += 95 * time.dt
    drop_3d.rotation_x += 35 * time.dt

    if skak_tid > 0:
        skak_tid = max(0.0, skak_tid - time.dt)
        agg_3d.x = -1.2 + random.uniform(-0.12, 0.12)
        agg_3d.rotation_z = random.uniform(-14, 14)
    else:
        agg_3d.x = -1.2
        agg_3d.rotation_z = 0


uppdatera_hud()
app.run()