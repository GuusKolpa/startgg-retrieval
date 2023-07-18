from data_getter.packages_smashggpy.models.Entrant import Entrant
import data_getter.packages_smashggpy.queries.Event_Queries as queries
from data_getter.packages_smashggpy.util.Logger import Logger
from data_getter.packages_smashggpy.common.Common import flatten, validate_data
from data_getter.packages_smashggpy.common.ValidGames import VALID_GAMES
from data_getter.packages_smashggpy.models.PhaseGroup import PhaseGroup
from data_getter.packages_smashggpy.models.EntrantPlayerLink import EntrantPlayer
from data_getter.packages_smashggpy.util.NetworkInterface import NetworkInterface as NI
from data_getter.packages_smashggpy.util.ThreadFactory import ThreadFactory
from data_getter.packages_smashggpy.common.Exceptions import \
    DataPullException, NoEventDataException, NoPhaseGroupDataException, NoPhaseDataException, DataMalformedException


class Event(object):

    def __init__(self, id, tournament_id, name, videogame_id, is_online, num_entrants, event_type):
        self.id = id
        self.tournament_id = tournament_id
        self.name = name
        self.videogame_id = videogame_id
        self.is_online = is_online
        self.num_entrants = num_entrants
        self.event_type = event_type

    def __eq__(self, other):
        if other is None:
            return False
        if type(other) != type(self):
            return False
        return hash(other) == hash(self)

    def __hash__(self):
        return hash((self.id, self.tournament_id, self.name, self.videogame_id, self.is_online, self.num_entrants))

    def __str__(self):
        return 'Event ({0}): {1}'

    @staticmethod
    def validate_data(input: dict, id: int=0):
        if 'data' in input:
            raise DataMalformedException(input)
        if 'event' not in input or input['event'] is None:
            raise NoEventDataException(id)

    @staticmethod
    def parse(data):
        assert (data is not None), 'Event.parse cannot have None for data parameter'
        if 'data' in data and 'event' in data['data']:
            raise DataMalformedException(data,
                                         'data is malformed for Event.parse. '
                                         'Please give only what is contained in the '
                                         '"event" property')

        assert ('id' in data), 'Event.parse must have id property on data parameter'
        assert ('tournament' in data), 'Event.parse must have tournament property on data parameter'
        assert ('name' in data), 'Event.parse must have name property on data parameter'
        assert ('videogame' in data), 'Event.parse must have videogame property on data parameter'
        assert ('numEntrants' in data), 'Event.parse must have numEntrants property on data parameter'
        assert ('isOnline' in data), 'Event.parse must have isOnline property on data parameter'
        
        if (data['videogame']['id'] in VALID_GAMES): # 'Event.parse must have videogame property on data parameter'
            if data['teamRosterSize'] is None:
                event_type = 'SINGLES'
            elif data['teamRosterSize']['minPlayers'] > 2:
                event_type = 'CREWS'
            elif data['teamRosterSize']['minPlayers'] == 2:
                event_type = 'DOUBLES'
            else:
                event_type = 'UNKNOWN'
            return Event(
                data['id'],
                data['tournament']['id'],
                data['name'],
                data['videogame']['id'],
                data['isOnline'],
                data['numEntrants'],
                event_type
            )


    def get_phase_groups(self):
        assert (self.id is not None), 'event id cannot be None if calling get_phase_groups'
        Logger.debug('Getting Phase Groups for Event: {0}:{1}'.format(self.id, self.name))
        data = NI.query(queries.get_event_phase_groups, {'id': self.id})
        validate_data(data)

        try:
            event_data = data['data']['event']
            if event_data is None:
                raise NoEventDataException(self.id)

            phase_groups_data = event_data['phaseGroups']
            if phase_groups_data is None:
                Logger.error(NoPhaseGroupDataException(self.id))
                return []

            return [PhaseGroup.parse(phase_group_data) for phase_group_data in phase_groups_data]
        except AttributeError as e:
            Logger.error("No phase group data pulled back for event {}".format(self.id))

    def get_entrants(self):
        assert (self.id is not None), 'event id cannot be None if calling get_phase_groups'
        Logger.debug('Getting Entrants for Event: {0}:{1}'.format(self.id, self.name))
        data = NI.paginated_query(queries.get_event_entrants, {'id': self.id})
        entrants = flatten([Entrant.parse(entrant_data) for entrant_data in data])
        return entrants

    def get_entrants_with_player_links(self):
        assert (self.id is not None), 'event id cannot be None if calling get_phase_groups'
        Logger.debug('Getting Entrants for Event: {0}:{1}'.format(self.id, self.name))
        data = NI.paginated_query(queries.get_event_entrants, {'id': self.id})
        entrants = [i for i in [Entrant.parse(entrant_data) for entrant_data in data] if i is not None]
        player_links = flatten([EntrantPlayer.parse(entrant_data) for entrant_data in data])
        return entrants, player_links



    # @staticmethod
    # def get(tournament_slug: str, event_slug: str):
    #     assert (tournament_slug is not None), 'Event.get cannot have None for tournament_slug parameter'
    #     assert (event_slug is not None), 'Event.get cannot have None for event_slug parameter'
    #     slug = "tournament/{0}/event/{1}".format(tournament_slug, event_slug)
    #     data = NI.query(queries.get_event_by_slugs, {"slug": slug})
    #     validate_data(data)

    #     try:
    #         event_data = data['data']['event']
    #         if event_data is None:
    #             raise NoEventDataException('{}:{}'.format(tournament_slug, event_slug))

    #         return Event.parse(event_data)
    #     except AttributeError as e:
    #         raise NoEventDataException('{}:{}'.format(tournament_slug, event_slug))

    # @staticmethod
    # def get_by_id(id: int):
    #     assert (id is not None), "Event.get_by_id cannot have None for id parameter"
    #     data = NI.query(queries.get_event_by_id, {'id': id})
    #     validate_data(data)

    #     try:
    #         event_data = data['data']['event']
    #         if event_data is None:
    #             raise NoEventDataException(id)

    #         return Event.parse(event_data)
    #     except AttributeError as e:
    #         raise NoEventDataException(id)

    # def get_phases(self):
    #     assert (self.id is not None), 'event id cannot be None if calling get_phases'
    #     Logger.info('Getting Phases for Event: {0}:{1}'.format(self.id, self.name))
    #     data = NI.query(queries.get_event_phases, {'id': self.id})
    #     validate_data(data)

    #     try:
    #         event_data = data['data']['event']
    #         if event_data is None:
    #             raise NoEventDataException(self.identifier)

    #         phases_data = event_data['phases']
    #         if phases_data is None:
    #             raise NoPhaseDataException(self.identifier)

    #         return [Phase.parse(phase_data) for phase_data in phases_data]
    #     except AttributeError as e:
    #         raise Exception("No phase data pulled back for event {} {}".format(self.id, self.name))

    # def get_attendees(self):
    #     assert (self.id is not None), 'event id cannot be None if calling get_attendees'
    #     Logger.info('Getting Attendees for Event: {0}:{1}'.format(self.id, self.name))
    #     phase_groups = self.get_phase_groups()
    #     attendees = flatten([phase_group.get_attendees() for phase_group in phase_groups])
    #     return attendees

    # def get_entrants(self):
    #     assert (self.id is not None), 'event id cannot be None if calling get_entrants'
    #     Logger.info('Getting Entrants for Event: {0}:{1}'.format(self.id, self.name))
    #     phase_groups = self.get_phase_groups()
    #     entrants = flatten([phase_group.get_entrants() for phase_group in phase_groups])
    #     return entrants

    # def get_sets(self):
    #     assert (self.id is not None), 'event id cannot be None if calling get_sets'
    #     Logger.info('Getting Sets for Event: {0}:{1}'.format(self.id, self.name))
    #     phase_groups = self.get_phase_groups()
    #     sets = flatten([phase_group.get_sets() for phase_group in phase_groups])
    #     return sets

    # def get_incomplete_sets(self):
    #     assert (self.id is not None), 'event id cannot be None if calling get_incomplete_sets'
    #     Logger.info('Getting Incomplete Sets for Event: {0}:{1}'.format(self.id, self.name))
    #     sets = self.get_sets()
    #     incomplete_sets = []
    #     for ggset in sets:
    #         if ggset.get_is_completed() is False:
    #             incomplete_sets.append(ggset)
    #     return incomplete_sets

    # def get_completed_sets(self):
    #     assert (self.id is not None), 'event id cannot be None if calling get_completed_sets'
    #     Logger.info('Getting Completed Sets for Event: {0}:{1}'.format(self.id, self.name))
    #     sets = self.get_sets()
    #     complete_sets = []
    #     for ggset in sets:
    #         if ggset.get_is_completed() is True:
    #             complete_sets.append(ggset)
    #     return complete_sets

