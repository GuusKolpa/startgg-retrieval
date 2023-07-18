
from data_getter.packages_smashggpy.models.Tournament import Tournament
from data_getter.packages_smashggpy.util import Initializer
from data_getter.packages_smashggpy.util.Logger import Logger
from data_getter.packages_smashggpy.util.QueryQueueDaemon import QueryQueueDaemon
from data_getter.packages_smashggpy.inserts.InsertFunc import insert_records
from data_getter.packages_smashggpy.reads.ReadTournaments import get_existing_tournament_urls
import os
import tracemalloc

tracemalloc.start()

# arguments = sys.argv[0:1]
existing_tournaments = get_existing_tournament_urls()
tournament_slugs = []

# tournament_slugs = ['mission-complete-5']
with open("tournament_slug_list.txt", "r") as f:
    for line in f:
        tournament_slugs.append(str(line.strip()))

overwrite_mode = False

if __name__ == '__main__':
    assert os.getenv('startgg_api_key') is not None and os.getenv('SGG_PY_APPPWD') is not None
    SGG_API_KEY = os.getenv('startgg_api_key')
    Initializer.initialize(SGG_API_KEY, 'info')

    for slug in tournament_slugs:
        tournament_list = []
        event_list = []
        phase_groups_list = []
        set_list = []
        entrant_list = []
        player_list = []
        entrant_player_list = []
        tournament_url = 'tournament/' + slug
        if not overwrite_mode and tournament_url in existing_tournaments:
            Logger.error('Tournament already exists in database: {}'.format(slug))
            continue

        Logger.info('Retrieving Tournament info for tournament: {}'.format(slug))
        current_tourn = Tournament.get(slug)
        tournament_list.append(current_tourn)
        current_events = current_tourn.get_events()
        event_list.extend(current_events)
        current_players = current_tourn.get_tournament_players()
        player_list.extend(current_players)

        for event in event_list:
            Logger.info('Retrieving Event info for event: {} - {}'.format(event.name, slug))
            current_phas_groups = event.get_phase_groups()
            phase_groups_list.extend(current_phas_groups)

        for event in event_list:
            Logger.info('Retrieving players for event: {} - {}'.format(event.name, slug))
            current_entrants, current_player_links = event.get_entrants_with_player_links()
            entrant_player_list.extend(current_player_links)
            entrant_list.extend(current_entrants)

        for phase in phase_groups_list:
            Logger.info('Retrieving sets for phase: {} - {}'.format(phase.name, slug))
            current_sets = phase.get_sets()
            set_list.extend(current_sets)

        valid_tourn_ids = insert_records(tournament_list, 'sgg.TOURNAMENT', overwrite_mode=overwrite_mode)
        valid_event_ids = insert_records(event_list, TABLE_NAME='sgg.EVENT', overwrite_mode=overwrite_mode)
        valid_event_ids = insert_records(player_list, TABLE_NAME='sgg.PLAYER', overwrite_mode=overwrite_mode)
        valid_phase_ids = insert_records(phase_groups_list, TABLE_NAME='sgg.PHASE', overwrite_mode=overwrite_mode)
        valid_entrant_ids = insert_records(entrant_list, 'sgg.ENTRANT', overwrite_mode=overwrite_mode)
        valid_entrant_playerds = insert_records(entrant_player_list, 'sgg.ENTRANTPLAYER', overwrite_mode=overwrite_mode)
        valid_set_ids = insert_records(set_list, 'sgg.GGSET', overwrite_mode=overwrite_mode)

        del tournament_list, event_list, phase_groups_list, set_list, entrant_list, player_list, entrant_player_list

QueryQueueDaemon.kill_daemon()
