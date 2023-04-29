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
            Zed(["AlphaClot", "ClotVersus"], "Clot_Alpha_Versus"),
            Zed(["Cyst"], "Clot_Cyst"),
            Zed(["Slasher"], "Clot_Slasher"),
            Zed(["AlphaSlasher", "SlasherVersus"], "Clot_Slasher_Versus"),

            Zed(["Crawler"], "Crawler"),
            Zed(["EliteCrawler", "WhiteCrawler"], "CrawlerKing"),
            Zed(["AlphaCrawler", "CrawlerVersus"], "Crawler_Versus"),
            Zed(["Stalker"], "Stalker"),
            Zed(["AlphaStalker", "StalkerVersus"], "Stalker_Versus"),
            Zed(["Gorefast"], "Gorefast"),
            Zed(["AlphaGorefast", "GorefastVersus"], "Gorefast_Versus"),

            # medium zeds
            Zed(["Gorefiend"], "GorefastDualBlade"),
            Zed(["Bloat"], "Bloat"),
            Zed(["AlphaBloat", "BloatVersus"], "Bloat_Versus"),
            Zed(["Siren"], "Siren"),
            Zed(["AlphaSiren", "SirenVersus"], "Siren_Versus"),
            Zed(["Husk"], "Husk"),
            Zed(["AlphaHusk", "HuskVersus"], "Husk_Versus"),
            Zed(["Quarterpound", "FPMini", "MiniFP", "FleshpoundMini", "MiniFleshpound"], "FleshpoundMini"),
            
            # large zeds
            Zed(["Scrake"], "Scrake"),
            Zed(["AlphaScrake", "ScrakeVersus"], "Scrake_Versus"),
            Zed(["Fleshpound"], "Fleshpound"),
            Zed(["AlphaFleshpound", "FleshpoundVersus"], "Fleshpound_Versus"),
                        
            # bosses
            Zed(["Patriarch"], "Patriarch"),
            Zed(["AlphaPatriarch", "PatriarchVersus"], "Patriarch_Versus"),
            Zed(["Hans"], "Hans"),
            Zed(["KingFP", "FleshpoundKing", "KingFleshpound"], "FleshpoundKing"),
            Zed(["Abomination", "KingBloat", "BloatKing"], "BloatKing"),
            ]
        
        prefix = 'KFGameContent.KFPawn_Zed'
        for zed in default_zeds:
            self._zeds.update(dict.fromkeys(zed.aliases, prefix + zed.name))


    def _add_zed_variants_mod_zeds(self):
        modded_zeds = [
            # small zeds
            Zed(["MagmaClot"], "magmaclot"),
            Zed(["Prowler"], "prowler"),
            Zed(["GreenClot", "HoneyBiscuit"], "honeybiscuit"),
            Zed(["DemonicClot"], "demonicclot"),
            Zed(["RedStalker"], "redstalker"),
            Zed(["DarkCreep"], "darkcreep"),
            Zed(["MrPelvis"], "mrpelvis"),

            # medium zeds
            Zed(["GreenBloat"], "greenbloat"),
            Zed(["RedHusk"], "redhusk"),
            Zed(["BlueHusk"], "bluehusk"),
            Zed(["WhiteHusk"], "shocktroop"),
            Zed(["FireworksHusk", "Sparky"], "sparky"),
            Zed(["HellfireHusk"], "hellfire"),
            Zed(["DoomRevenant", "Revenant"], "revenant"),

            # large zeds
            Zed(["RedScrake"], "redscrake"),
            Zed(["BlueScrake"], "bluescrake"),
            Zed(["WerewolfScrake", "Otis", "BossScrake"], "otis"),
            Zed(["RedFleshpound"], "redfleshpound"),
            Zed(["DoomBaron", "BaronOfHell", "Baron"], "baronhell"),
            Zed(["DoomMancubus", "Mancubus"], "mancubus"),
        ]

        prefix = 'zedcustom.'
        for zed in modded_zeds:
            self._zeds.update(dict.fromkeys(zed.aliases, prefix + zed.name))


    def zed_alias_to_name(self, name : str) -> str:
        return self._zeds[name]


    def __init__(self, include_custom: bool):
        self._zeds = {}
        self._add_default_zeds()

        if include_custom:
            self._add_zed_variants_mod_zeds()


    