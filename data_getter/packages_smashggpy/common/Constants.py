import os
import data_getter.packages_smashggpy.inserts.Schema as InsertSchema
import data_getter.packages_smashggpy.overwrites.Schema as OverwriteSchema

SERVER = 'DESKTOP-EQR6D6L\SQLEXPRESS'
DATABASE = 'smashgg_archive'
UID = 'sgg_py_app'
PWD = os.getenv('SGG_PY_APPPWD')

TABLE_DICTIONARY = {
    "sgg.TOURNAMENT": {"OW": OverwriteSchema.tournament_overwrite_schema, "INS": InsertSchema.tournament_insert_schema},
    "sgg.EVENT": {"OW": OverwriteSchema.event_overwrite_schema, "INS": InsertSchema.event_insert_schema},
    "sgg.PHASE": {"OW": OverwriteSchema.phase_overwrite_schema, "INS": InsertSchema.phase_insert_schema},
    "sgg.GGSET": {"OW": OverwriteSchema.set_overwrite_schema, "INS": InsertSchema.set_insert_schema},
    "sgg.ENTRANT": {"OW": OverwriteSchema.entrant_overwrite_schema, "INS": InsertSchema.entrant_insert_schema},
    "sgg.ENTRANTPLAYER": {
        "OW": OverwriteSchema.entrant_player_overwrite_schema, "INS": InsertSchema.entrant_player_insert_schema
        },
    "sgg.PLAYER": {"OW": OverwriteSchema.player_overwrite_schema, "INS": InsertSchema.player_insert_schema}
    }
