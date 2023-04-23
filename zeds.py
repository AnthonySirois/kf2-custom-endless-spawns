from dataclasses import dataclass

@dataclass
class Zed:
    aliases: list
    name: str
    
    
class KF2_ZEDS:
    _zeds: dict

    def _add_default_zeds(self):
        default_zeds = [
            # small zeds
            Zed(["Clot"], "Clot_Alpha"),
            Zed(["Rioter"], "Clot_AlphaKing"),
            Zed(["AlphaClot"], "Clot_Alpha_Versus"),
            Zed(["Cyst"], "Clot_Cyst"),
            Zed(["Slasher"], "Clot_Slasher"),
            Zed(["AlphaSlasher"], "Clot_Slasher_Versus"),

            Zed(["Crawler"], "Crawler"),
            Zed(["EliteCrawler"], "CrawlerKing"),
            Zed(["AlphaCrawler"], "Crawler_Versus"),
            Zed(["Stalker"], "Stalker"),
            Zed(["AlphaStalker"], "Stalker_Versus"),
            Zed(["Gorefast"], "Gorefast"),
            Zed(["AlphaGorefast"], "Gorefast_Versus"),

            # medium zeds
            Zed(["Gorefiend"], "GorefastDualBlade"),
            Zed(["Bloat"], "Bloat"),
            Zed(["AlphaBloat"], "Bloat_Versus"),
            Zed(["Siren"], "Siren"),
            Zed(["AlphaSiren"], "Siren_Versus"),
            Zed(["Husk"], "Husk"),
            Zed(["AlphaHusk"], "Husk_Versus"),
            Zed(["Quarterpound", "FPMini", "MiniFP", "FleshpoundMini", "MiniFleshpound"], "FleshpoundMini"),
            
            # large zeds
            Zed(["Scrake"], "Scrake"),
            Zed(["AlphaScrake"], "Scrake_Versus"),
            Zed(["Fleshpound"], "Fleshpound"),
            Zed(["AlphaFleshpound"], "Fleshpound_Versus"),
                        
            # bosses
            Zed(["Patriarch"], "Patriarch"),
            Zed(["AlphaPatriarch"], "Patriarch_Versus"),
            Zed(["Hans"], "Hans"),
            Zed(["KingFP", "FleshpoundKing", "KingFleshpound"], "FleshpoundKing"),
            Zed(["Abomination", "KingBloat", "BloatKing"], "BloatKing"),
            ]
        
        prefix = 'KFGameContent.KFPawn_Zed'
        for zed in default_zeds:
            self._zeds.update(dict.fromkeys(zed.aliases, prefix + zed.name))


    def zed_alias_to_name(self, name : str) -> str:
        return self._zeds[name]


    def __init__(self):
        self._zeds = {}
        self._add_default_zeds()


    