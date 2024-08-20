from players.schemas import PlayerCompleteSchema, PlayersDetailSchema
from players.utils import calculate_hash


def validated_required_attributes(players_data):
    """
    Filters out only the attributes that are used in the local system at the moment
    :param players_data: List of dictionaries of players from external api
    :return: List of dictionaries of players with filtered attributes only
    """
    filtered_players = [
        PlayerCompleteSchema(**player).model_dump() for player in players_data
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


def filtered_players_details(history_data, redis):
    filtered_players = []
    for player_data in history_data:
        validated_player_data = PlayersDetailSchema(**player_data).model_dump()
        player_id = validated_player_data["player_id"]
        game_week = validated_player_data["game_week"]
        detail_hash = calculate_hash(validated_player_data)
        # Use player_id and game_week for combined field key for hashmap.
        player_detail_key = "player_detail"
        player_detail_field = f"{player_id}:{game_week}"

        cached_hash = redis.hget(player_detail_key, player_detail_field)
        if cached_hash is not None:
            cached_hash = cached_hash.decode("utf-8")

        if cached_hash == detail_hash:
            print("Skipping this..")
            continue
        filtered_players.append(validated_player_data)
        redis.hset(player_detail_key, player_detail_field, detail_hash)
    # filtered_players = [
    #     PlayersDetailSchema(**player).model_dump() for player in history_data
    # ]
    return filtered_players


def rename_gw_attributes(gw_data):
    gw_data['player_id'] = gw_data.pop('element')
    gw_data['game_week'] = gw_data.pop('round')

    return gw_data


def player_history_mock_data(player_id):

    historical_data = [
        {
            "element": player_id,
            "round": 1,
            "goals_scored": 1,
            "assists": 0,
            "total_points": 10,
            "minutes": 90,
            "clean_sheets": 1,
            "goals_conceded": 0,
            "own_goals": 0,
            "penalties_saved": 0,
            "penalties_missed": 0,
            "yellow_cards": 1,
            "red_cards": 0,
            "saves": 0,
            "bonus": 2,
            "bps": 22,
            "influence": 36.6,
            "creativity": 15.3,
            "threat": 54.0,
            "ict_index": 10.6,
            "value": 120,
            "selected": 283747,
            "transfers_in": 0,
            "transfers_out": 0
        },
        {
            "element": player_id,
            "round": 2,
            "goals_scored": 1,
            "assists": 1,
            "total_points": 16,
            "minutes": 70,
            "clean_sheets": 0,
            "goals_conceded": 1,
            "own_goals": 0,
            "penalties_saved": 0,
            "penalties_missed": 0,
            "yellow_cards": 1,
            "red_cards": 0,
            "saves": 0,
            "bonus": 3,
            "bps": 22,
            "influence": 36.6,
            "creativity": 15.3,
            "threat": 54.0,
            "ict_index": 12.6,
            "value": 119,
            "selected": 123747,
            "transfers_in": 6000,
            "transfers_out": 0
        },
        {
            "element": player_id,
            "round": 3,
            "goals_scored": 1,
            "assists": 1,
            "total_points": 16,
            "minutes": 70,
            "clean_sheets": 0,
            "goals_conceded": 1,
            "own_goals": 0,
            "penalties_saved": 0,
            "penalties_missed": 0,
            "yellow_cards": 1,
            "red_cards": 0,
            "saves": 0,
            "bonus": 3,
            "bps": 22,
            "influence": 36.6,
            "creativity": 15.3,
            "threat": 54.0,
            "ict_index": 12.6,
            "value": 119,
            "selected": 123747,
            "transfers_in": 6000,
            "transfers_out": 0
        },

    ]
    return historical_data
