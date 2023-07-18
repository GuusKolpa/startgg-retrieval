tournament_overwrite_schema = """
DELETE FROM sgg.[Tournament]
WHERE [TournamentId] = ?;
"""


event_overwrite_schema = """
DELETE FROM sgg.[Event]
WHERE [EventId] = ?;
"""


phase_overwrite_schema = """
DELETE FROM sgg.[Phase]
WHERE [PhaseId] = ?;
"""

set_overwrite_schema = """
DELETE FROM sgg.[GGSet]
WHERE [GGSetId] = ?;
"""

entrant_overwrite_schema = """
DELETE FROM sgg.[Entrant]
WHERE [EntrantId] = ?;
"""

entrant_player_overwrite_schema = """
DELETE FROM sgg.[EntrantPlayer]
WHERE [EntrantPlayerId] = ?;
"""

player_overwrite_schema = """
DELETE FROM sgg.[Player]
WHERE [PlayerId] = ?;
"""