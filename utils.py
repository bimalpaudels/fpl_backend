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
