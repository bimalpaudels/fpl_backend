from api_call import get_player_stats_by_gw, split_players_by_importance
from datetime import datetime


if __name__ == '__main__':
    player_ids = split_players_by_importance(importance=1)
    try:
        start_time = datetime.now()
        get_player_stats_by_gw(player_ids, split=50)
        end_time = datetime.now()
        print("Time taken: ", end_time - start_time)
    except Exception as e:
        print(e)
