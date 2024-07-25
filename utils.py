def filter_required_attributes(players_data):
    """
    Filters out only the attributes that are used in the local system at the moment
    :param players_data: List of dictionaries of players from external api
    :return: List of dictionaries of players with filtered attributes only
    """
    filtered_players = [
        {
            'player_id': player["id"],
            'first_name': player['first_name'],
            'second_name': player['second_name'],
            'now_cost': player['now_cost'],

        }
        for player in players_data
    ]
    return filtered_players


HISTORY_DATA = [
    {
        "element": 183,
        "round": 1,
        "goals": 1,
        "assists": 0,
        "total_points": 10
    },
    {
        "element": 183,
        "round": 2,
        "goals": 0,
        "assists": 1,
        "total_points": 5
    },
    {
        "element": 183,
        "round": 3,
        "goals": 0,
        "assists": 0,
        "total_points": 2
    },
    {
        "element": 182,
        "round": 4,
        "goals": 2,
        "assists": 0,
        "total_points": 13
    },
    {
        "element": 182,
        "round": 5,
        "goals": 3,
        "assists": 0,
        "total_points": 20
    },
]


def filtered_players_details(history_data):
    filtered_players = [
        {"player_id": data.get('element'),
         "game_week": data.get('round'),
         "goals": data.get('goals'),
         "assists": data.get('assists'),
         "total_points": data.get('total_points')
         }
        for data in history_data
    ]
    return filtered_players


def player_history_mock_data(player_id):

    historical_data = [
        {
            "element": player_id,
            "round": 1,
            "goals": 1,
            "assists": 0,
            "total_points": 10
        },
        {
            "element": player_id,
            "round": 2,
            "goals": 0,
            "assists": 1,
            "total_points": 5
        },
        {
            "element": player_id,
            "round": 3,
            "goals": 0,
            "assists": 0,
            "total_points": 2
        },
        {
            "element": player_id,
            "round": 4,
            "goals": 2,
            "assists": 0,
            "total_points": 13
        },
        {
            "element": player_id,
            "round": 5,
            "goals": 3,
            "assists": 0,
            "total_points": 20
        },
        {
            "element": player_id,
            "round": 6,
            "goals": 1,
            "assists": 1,
            "total_points": 10
        },
    ]
    return historical_data
