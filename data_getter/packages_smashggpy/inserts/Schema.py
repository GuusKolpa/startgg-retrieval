tournament_insert_schema = """
INSERT INTO sgg.[Tournament](
     [TournamentId]
    ,[Name]
    ,[URL]
    ,[StartDate]
    ,[EndDate]
    ,[Timezone]
    ,[IsOnline]
    ,[CountryCode]
    ,[City]
    ,[OwnerId]
    ,[OwnerTag]) 
    VALUES (?,?,?,?,?,?,?,?,?,?,?);
"""

event_insert_schema = """
INSERT INTO sgg.[Event](
     [EventId]
    ,[TournamentId]
    ,[Name]
    ,[VideogameId]
    ,[IsOnline]
    ,[Entrants]
    ,[EventType])
    VALUES (?,?,?,?,?,?,?);
"""

phase_insert_schema = """
INSERT INTO sgg.[Phase](
     [PhaseId]
    ,[EventId]
    ,[SubId]
    ,[Name]
    ,[BracketType])
    VALUES (?,?,?,?,?);
"""

set_insert_schema = """
INSERT INTO sgg.[GGSet](
     [GGSetId]
    ,[PhaseId]
    ,[Entrant1Id]
    ,[Entrant2Id]
    ,[Entrant1Score]
    ,[Entrant2Score]
    ,[RoundText]
    ,[CompletionTime])
    VALUES (?,?,?,?,?,?,?,?);
"""
entrant_insert_schema = """
INSERT INTO sgg.[Entrant](
     [EntrantId]
    ,[EventId]
    ,[Name]
    ,[Placement]
    ,[IsTeam])
    VALUES (?,?,?,?,?)
"""

entrant_player_insert_schema = """
INSERT INTO sgg.[EntrantPlayer](
     [EntrantPlayerId]
    ,[EntrantId]
    ,[PlayerId])
    VALUES (?,?,?)
"""

player_insert_schema = """
INSERT INTO sgg.[Player](
     [PlayerId]
    ,[Name]
    ,[Country]
    ,[City]
    ,[Pronouns])
    VALUES (?,?,?,?,?)
"""