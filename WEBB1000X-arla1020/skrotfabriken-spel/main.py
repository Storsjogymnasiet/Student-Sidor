from dataclasses import dataclass
import math
import random
import sys
import pygame

from textures import (
    skapa_gard_bakgrund,
    skapa_kross_textur,
    skapa_robot_textur,
    skapa_skrothog_textur,
    skapa_transportband_textur,
    skapa_ugn_textur,
)

BREDD, HOJD = 1120, 700
FPS = 60


@dataclass
class FlytandeText:
    text: str
    x: float
    y: float
    farg: tuple[int, int, int]
    livstid: float = 1.0


@dataclass
class Knapp:
    rect: pygame.Rect
    titel: str
    undertext: str
    kostnad: int
    farg: tuple[int, int, int]


class SkrotfabrikSpel:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("Skrotfabriken — Solig skrotgård & automation")
        self.skarm = pygame.display.set_mode((BREDD, HOJD))
        self.klocka = pygame.time.Clock()

        self.font_stor = pygame.font.SysFont("segoeui", 25, bold=True)
        self.font_medel = pygame.font.SysFont("segoeui", 16, bold=True)
        self.font_liten = pygame.font.SysFont("segoeui", 13)

        # Bakgrund & texturer
        self.gard_yta = skapa_gard_bakgrund(740, HOJD - 78)
        self.skrot_yta = skapa_skrothog_textur(205)
        self.robot_yta = skapa_robot_textur(56)
        self.band_yta = skapa_transportband_textur(96, 42)
        self.ugn_yta = skapa_ugn_textur(84, aktiv=True)
        self.kross_yta = skapa_kross_textur(82)

        # Ekonomi: börjar långsamt och manuellt (1 kr per grävning)
        self.pengar: float = 0.0
        self.totalt_intjanat: float = 0.0

        # Manuella uppgraderingar
        self.verktyg_niva: int = 1
        self.verktyg_pris: int = 25
        self.manuell_bas: int = 1

        self.detektor_niva: int = 0
        self.detektor_pris: int = 85
        self.bonus_per_detektor: int = 2

        # Automation (4 olika maskiner i stigande pris & effekt)
        self.band_antal: int = 0
        self.band_pris: int = 160
        self.band_per_sek: float = 1.5

        self.robotar: int = 0
        self.robot_pris: int = 420
        self.robot_per_sek: float = 5.0

        self.krossar: int = 0
        self.kross_pris: int = 1100
        self.kross_per_sek: float = 16.0

        self.ugnar: int = 0
        self.ugn_pris: int = 2800
        self.ugn_per_sek: float = 45.0

        # Visuella effekter
        self.skrot_rect = pygame.Rect(265, 335, 205, 205)
        self.skrot_studs: float = 0.0
        self.tid: float = 0.0
        self.flytande_texter: list[FlytandeText] = []

        self.grav_knapp_rect = pygame.Rect(210, 562, 315, 48)
        self.uppgraderings_knappar: list[Knapp] = []
        self.uppdatera_knappar()

    @property
    def manuell_intakt(self) -> int:
        return self.manuell_bas + (self.detektor_niva * self.bonus_per_detektor)

    @property
    def inkomst_per_sek(self) -> float:
        return (
            (self.band_antal * self.band_per_sek)
            + (self.robotar * self.robot_per_sek)
            + (self.krossar * self.kross_per_sek)
            + (self.ugnar * self.ugn_per_sek)
        )

    def uppdatera_knappar(self) -> None:
        x0 = 760
        bredd = 338
        hojd = 82
        start_y = 94
        avstand = 94

        self.uppgraderings_knappar = [
            Knapp(
                rect=pygame.Rect(x0, start_y + 0 * avstand, bredd, hojd),
                titel=f"[1] Bättre spade & klo (Niv. {self.verktyg_niva})",
                undertext="+1 manuell intäkt per klick",
                kostnad=self.verktyg_pris,
                farg=(58, 122, 190),
            ),
            Knapp(
                rect=pygame.Rect(x0, start_y + 1 * avstand, bredd, hojd),
                titel=f"[2] Metalldetektor (Niv. {self.detektor_niva})",
                undertext=f"+{self.bonus_per_detektor} bonus/klick (hittar finare skrot)",
                kostnad=self.detektor_pris,
                farg=(176, 118, 44),
            ),
            Knapp(
                rect=pygame.Rect(x0, start_y + 2 * avstand, bredd, hojd),
                titel=f"[3] Transportband ({self.band_antal} st)",
                undertext=f"Auto: +{self.band_per_sek:.1f} kr/s per band",
                kostnad=self.band_pris,
                farg=(88, 118, 152),
            ),
            Knapp(
                rect=pygame.Rect(x0, start_y + 3 * avstand, bredd, hojd),
                titel=f"[4] Sorteringsrobot ({self.robotar} st)",
                undertext=f"Auto: +{self.robot_per_sek:.0f} kr/s per robot",
                kostnad=self.robot_pris,
                farg=(44, 152, 120),
            ),
            Knapp(
                rect=pygame.Rect(x0, start_y + 4 * avstand, bredd, hojd),
                titel=f"[5] Skrotpress ({self.krossar} st)",
                undertext=f"Auto: +{self.kross_per_sek:.0f} kr/s per press",
                kostnad=self.kross_pris,
                farg=(172, 132, 36),
            ),
            Knapp(
                rect=pygame.Rect(x0, start_y + 5 * avstand, bredd, hojd),
                titel=f"[6] Smältugn ({self.ugnar} st)",
                undertext=f"Auto: +{self.ugn_per_sek:.0f} kr/s per ugn",
                kostnad=self.ugn_pris,
                farg=(192, 74, 52),
            ),
        ]

    def lagg_till_pengar(self, mangd: float, x: float, y: float, farg=(255, 232, 115)) -> None:
        self.pengar += mangd
        self.totalt_intjanat += mangd
        visad = f"+{mangd:.1f} kr" if mangd % 1 else f"+{int(mangd)} kr"
        self.flytande_texter.append(FlytandeText(text=visad, x=x, y=y, farg=farg))

    def grav_manuellt(self) -> None:
        varde = self.manuell_intakt
        self.skrot_studs = 1.0
        ox = self.skrot_rect.centerx + random.randint(-36, 36)
        oy = self.skrot_rect.top + random.randint(10, 38)
        self.lagg_till_pengar(varde, ox, oy, farg=(255, 236, 120))

    def kop_uppgradering(self, index: int) -> None:
        if index == 0 and self.pengar >= self.verktyg_pris:
            self.pengar -= self.verktyg_pris
            self.verktyg_niva += 1
            self.manuell_bas += 1
            self.verktyg_pris = int(self.verktyg_pris * 1.85) + 10
        elif index == 1 and self.pengar >= self.detektor_pris:
            self.pengar -= self.detektor_pris
            self.detektor_niva += 1
            self.detektor_pris = int(self.detektor_pris * 1.95) + 25
        elif index == 2 and self.pengar >= self.band_pris:
            self.pengar -= self.band_pris
            self.band_antal += 1
            self.band_pris = int(self.band_pris * 1.8) + 45
        elif index == 3 and self.pengar >= self.robot_pris:
            self.pengar -= self.robot_pris
            self.robotar += 1
            self.robot_pris = int(self.robot_pris * 1.85) + 120
        elif index == 4 and self.pengar >= self.kross_pris:
            self.pengar -= self.kross_pris
            self.krossar += 1
            self.kross_pris = int(self.kross_pris * 1.9) + 300
        elif index == 5 and self.pengar >= self.ugn_pris:
            self.pengar -= self.ugn_pris
            self.ugnar += 1
            self.ugn_pris = int(self.ugn_pris * 1.95) + 750
        self.uppdatera_knappar()

    def uppdatera(self, dt: float) -> None:
        self.tid += dt
        if self.skrot_studs > 0:
            self.skrot_studs = max(0.0, self.skrot_studs - dt * 5.0)

        if self.inkomst_per_sek > 0:
            intjanat = self.inkomst_per_sek * dt
            self.pengar += intjanat
            self.totalt_intjanat += intjanat

            if random.random() < dt * 1.1:
                rx = random.randint(80, 640)
                ry = random.randint(315, 520)
                self.flytande_texter.append(
                    FlytandeText(
                        text=f"+{self.inkomst_per_sek:.1f} kr/s",
                        x=rx,
                        y=ry,
                        farg=(255, 245, 175),
                        livstid=0.95,
                    )
                )

        for ft in self.flytande_texter:
            ft.y -= 34 * dt
            ft.livstid -= dt
        self.flytande_texter = [ft for ft in self.flytande_texter if ft.livstid > 0]

    def rita_topplist(self) -> None:
        pygame.draw.rect(self.skarm, (24, 29, 36), (0, 0, BREDD, 78))
        pygame.draw.line(self.skarm, (68, 78, 92), (0, 78), (BREDD, 78), 2)

        pengar_text = self.font_stor.render(f"Pengar: {self.pengar:,.1f} kr", True, (145, 248, 165))
        auto_text = self.font_medel.render(f"Automation: +{self.inkomst_per_sek:.1f} kr/s", True, (130, 226, 248))
        klick_text = self.font_liten.render(
            f"Manuellt: +{self.manuell_intakt} kr/klick  |  Klicka på skrothögen eller tryck MELLANSLAG",
            True,
            (205, 214, 226),
        )

        self.skarm.blit(pengar_text, (24, 12))
        self.skarm.blit(auto_text, (24, 46))
        self.skarm.blit(klick_text, (395, 31))

    def rita_gard(self) -> None:
        self.skarm.blit(self.gard_yta, (0, 78))

        # Statusskylt i soliga gården
        if self.inkomst_per_sek == 0:
            fas = "FAS 1: Solig skrotgård — gräv själv och spara till första maskinerna"
        else:
            fas = "FAS 2: Maskinerna jobbar på gården!"
        skylt = pygame.Rect(20, 92, 540, 32)
        pygame.draw.rect(self.skarm, (28, 34, 40, 210), skylt, border_radius=8)
        pygame.draw.rect(self.skarm, (220, 210, 175), skylt, width=1, border_radius=8)
        self.skarm.blit(self.font_liten.render(fas, True, (248, 245, 232)), (32, 100))

        # Transportband längs vänstra gårdsplanen
        for i in range(min(self.band_antal, 3)):
            self.skarm.blit(self.band_yta, (42 + i * 104, 465))

        # Skrotpressar mot högra gårdsplanen
        for i in range(min(self.krossar, 2)):
            studs_y = int(math.sin(self.tid * 5 + i) * 4)
            self.skarm.blit(self.kross_yta, (545 + i * 92, 435 + studs_y))

        # Smältugnar längre bak i gården
        for i in range(min(self.ugnar, 3)):
            self.skarm.blit(self.ugn_yta, (525 + i * 68, 328))

        # Sorteringsrobotar som patrullerar på gården
        for i in range(min(self.robotar, 5)):
            hastighet = 1.0 + i * 0.14
            fas_rorelse = i * 1.2
            rx = 230 + math.sin(self.tid * hastighet + fas_rorelse) * 195
            ry = 515 + (i % 2) * 24
            self.skarm.blit(self.robot_yta, (int(rx), int(ry)))

        # Huvudskrothögen med studs vid klick
        skala = 1.0 + 0.06 * self.skrot_studs
        ny_storlek = int(205 * skala)
        skalad_skrot = pygame.transform.smoothscale(self.skrot_yta, (ny_storlek, ny_storlek))
        skrot_pos = skalad_skrot.get_rect(center=self.skrot_rect.center)
        self.skarm.blit(skalad_skrot, skrot_pos)

        # Manuell knapp under skrothögen
        mus_pos = pygame.mouse.get_pos()
        hovrar = self.grav_knapp_rect.collidepoint(mus_pos)
        knapp_farg = (88, 168, 98) if hovrar else (66, 138, 78)
        pygame.draw.rect(self.skarm, knapp_farg, self.grav_knapp_rect, border_radius=10)
        pygame.draw.rect(self.skarm, (235, 250, 235), self.grav_knapp_rect, width=2, border_radius=10)
        grav_label = self.font_medel.render(f"GRÄV I SKROT (+{self.manuell_intakt} kr)", True, (255, 255, 255))
        self.skarm.blit(grav_label, grav_label.get_rect(center=self.grav_knapp_rect.center))

    def rita_hogerspalt(self) -> None:
        pygame.draw.rect(self.skarm, (28, 32, 39), (740, 78, BREDD - 740, HOJD - 78))
        pygame.draw.line(self.skarm, (68, 78, 92), (740, 78), (740, HOJD), 2)

        rubrik = self.font_medel.render("UPPGRADERINGAR & MASKINER (1–6)", True, (242, 245, 250))
        self.skarm.blit(rubrik, (760, 74))

        mus_pos = pygame.mouse.get_pos()
        for knapp in self.uppgraderings_knappar:
            rad_att_kopa = self.pengar >= knapp.kostnad
            hovrar = knapp.rect.collidepoint(mus_pos)

            if not rad_att_kopa:
                farg = (44, 48, 56)
            elif hovrar:
                farg = tuple(min(255, c + 24) for c in knapp.farg)
            else:
                farg = knapp.farg

            pygame.draw.rect(self.skarm, farg, knapp.rect, border_radius=9)
            kant_farg = (232, 238, 246) if rad_att_kopa else (78, 86, 98)
            pygame.draw.rect(self.skarm, kant_farg, knapp.rect, width=2, border_radius=9)

            titel_surf = self.font_medel.render(knapp.titel, True, (255, 255, 255) if rad_att_kopa else (148, 155, 168))
            under_surf = self.font_liten.render(knapp.undertext, True, (236, 242, 248) if rad_att_kopa else (124, 132, 146))
            pris_surf = self.font_medel.render(f"{knapp.kostnad} kr", True, (255, 226, 110) if rad_att_kopa else (155, 112, 112))

            self.skarm.blit(titel_surf, (knapp.rect.x + 12, knapp.rect.y + 11))
            self.skarm.blit(under_surf, (knapp.rect.x + 12, knapp.rect.y + 42))
            self.skarm.blit(pris_surf, (knapp.rect.right - pris_surf.get_width() - 12, knapp.rect.y + 13))

        tips = self.font_liten.render("Börja med spade [1] → band [3] → robotar [4] → pressar & ugnar [5–6]", True, (158, 168, 184))
        self.skarm.blit(tips, (760, 668))

    def rita_flytande_texter(self) -> None:
        for ft in self.flytande_texter:
            alfa = max(0, min(255, int(ft.livstid * 255)))
            skugga = self.font_medel.render(ft.text, True, (20, 24, 28))
            skugga.set_alpha(alfa)
            self.skarm.blit(skugga, (int(ft.x) + 1, int(ft.y) + 1))

            surf = self.font_medel.render(ft.text, True, ft.farg)
            surf.set_alpha(alfa)
            self.skarm.blit(surf, (int(ft.x), int(ft.y)))

    def kor(self) -> None:
        while True:
            dt = self.klocka.tick(FPS) / 1000.0

            for handelse in pygame.event.get():
                if handelse.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif handelse.type == pygame.KEYDOWN:
                    if handelse.key == pygame.K_SPACE:
                        self.grav_manuellt()
                    elif handelse.key == pygame.K_1:
                        self.kop_uppgradering(0)
                    elif handelse.key == pygame.K_2:
                        self.kop_uppgradering(1)
                    elif handelse.key == pygame.K_3:
                        self.kop_uppgradering(2)
                    elif handelse.key == pygame.K_4:
                        self.kop_uppgradering(3)
                    elif handelse.key == pygame.K_5:
                        self.kop_uppgradering(4)
                    elif handelse.key == pygame.K_6:
                        self.kop_uppgradering(5)

                elif handelse.type == pygame.MOUSEBUTTONDOWN and handelse.button == 1:
                    pos = handelse.pos
                    if self.skrot_rect.collidepoint(pos) or self.grav_knapp_rect.collidepoint(pos):
                        self.grav_manuellt()
                    else:
                        for i, knapp in enumerate(self.uppgraderings_knappar):
                            if knapp.rect.collidepoint(pos):
                                self.kop_uppgradering(i)
                                break

            self.uppdatera(dt)
            self.rita_topplist()
            self.rita_gard()
            self.rita_hogerspalt()
            self.rita_flytande_texter()
            pygame.display.flip()


if __name__ == "__main__":
    SkrotfabrikSpel().kor()