def filter_required_attributes(players_data):
    """
    Filters out only the attributes that are used in the local system at the moment
    :param players_data: List of dictionaries of players from external api
    :return: List of dictionaries of players with filtered attributes only
    """
    filtered_players = [
        rename_keys(player) for player in players_data
    ]
    return filtered_players


def rename_keys(player):
    player['player_id'] = player.pop('id')
    player['expected_goals_involvement'] = player.pop('expected_goal_involvements')
    player['expected_goals_involvements_per_90'] = player.pop('expected_goal_involvements_per_90')
    columns_to_remove = ["chance_of_playing_next_round", "chance_of_playing_this_round", "code", "cost_change_event",
                         "cost_change_event_fall", "cost_change_start", "cost_change_start_fall", "dreamteam_count",
                         "element_type", "ep_next", "ep_this", "event_points", "in_dreamteam", "news", "news_added",
                         "photo", "special", "squad_number", "status", "team", "team_code", "transfers_in", "transfers_in_event",
                         "transfers_out", "transfers_out_event", "value_form", "value_season", "web_name", "influence_rank",
                         "influence_rank_type", "creativity_rank", "creativity_rank_type", "threat_rank", "threat_rank_type",
                         "ict_index_rank", "ict_index_rank_type", "corners_and_indirect_freekicks_order",
                         "corners_and_indirect_freekicks_text", "direct_freekicks_order", "direct_freekicks_text",
                         "penalties_order", "penalties_text", "now_cost_rank", "now_cost_rank_type", "form_rank", "form_rank_type",
                         "points_per_game_rank", "points_per_game_rank_type", "selected_rank", "selected_rank_type", "starts_per_90",
                         "clean_sheets_per_90"]
    for column in columns_to_remove:
        if column in player:
            player.pop(column)
    return player


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
