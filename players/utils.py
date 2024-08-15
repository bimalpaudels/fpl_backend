def player_position(key: int):
    positions = {
        1: "GK",
        2: "DEF",
        3: "MID",
        4: "FWD"
    }
    return positions.get(key)


def get_team(key: int):
    teams = {
        1: "ARS",
        2: "AVL",
        3: "BOU",
        4: "BRE",
        5: "BHA",
        6: "CHE",
        7: "CRY",
        8: "EVE",
        9: "FUL",
        10: "IPS",
        11: "LEI",
        12: "LIV",
        13: "MCI",
        14: "MUN",
        15: "NEW",
        16: "NFO",
        17: "SOU",
        18: "TOT",
        19: "WHU",
        20: "WOL",
    }
    return teams.get(key)
