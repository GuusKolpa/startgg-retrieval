import data_getter.packages_smashggpy.queries.Tournament_Queries as queries
from data_getter.packages_smashggpy.models.Event import Event


from data_getter.packages_smashggpy.util.Logger import Logger
from data_getter.packages_smashggpy.common.Common import flatten, validate_data, unix_to_datetime
from data_getter.packages_smashggpy.util.NetworkInterface import NetworkInterface as NI
from data_getter.packages_smashggpy.models.Player import Player
from data_getter.packages_smashggpy.common.Exceptions import \
    DataPullException, NoTournamentDataException, NoEventDataException, \
    NoPhaseDataException, NoPhaseGroupDataException, DataMalformedException
from datetime import datetime


class Tournament(object):

    def __init__(self, id, name, slug, start_time, end_time, timezone, is_online, country_code, city, owner_id, owner_tag):
        self.id = id
        self.name = name
        self.slug = slug
        self.start_time = start_time
        self.end_time = end_time
        self.timezone = timezone
        self.is_online = is_online
        self.country_code = country_code
        self.city = city
        self.owner_id = owner_id
        self.owner_tag = owner_tag

    def __eq__(self, other):
        if other is None:
            return False

        if type(self) != type(other):
            return False

        return hash(self) == hash(other)

    def __hash__(self) -> int:
        return super().__hash__()

    @staticmethod
    def validate_data(input: dict, slug: str = None):
        if 'data' in input:
            raise DataMalformedException(input)
        if 'tournament' not in input or input['tournament'] is None:
            raise NoTournamentDataException(slug)

    @staticmethod
    def get(slug: str):
        assert (slug is not None), "Tournament.get must have a slug parameter"
        data = NI.query(queries.get_tournament_by_slug, {'slug': slug})
        validate_data(data)

        try:
            tournament_data = data['data']['tournament']
            if tournament_data is None:
                raise NoTournamentDataException(slug)

            return Tournament.parse(tournament_data)
        except AttributeError as e:
            raise NoTournamentDataException(slug)


    @staticmethod
    def parse(data):
        assert (data is not None), 'Tournament.parse must have a data parameter'
        if 'data' in data and 'tournament' in data['data']:
            raise DataMalformedException(data,
                                         'data is malformed for Tournament.parse. '
                                         'Please give only what is contained in the '
                                         '"tournament" property')

        assert ('id' in data), 'Tournament.parse must have id in data parameter'
        assert ('name' in data), 'Tournament.parse must have name in data parameter'
        assert ('slug' in data), 'Tournament.parse must have slug in data parameter'
        assert ('startAt' in data), 'Tournament.parse must have startAt in data parameter'
        assert ('endAt' in data), 'Tournament.parse must have endAt in data parameter'
        assert ('timezone' in data), 'Tournament.parse must have timezone in data parameter'
        assert ('isOnline' in data), 'Tournament.parse must have isOnline in data parameter'
        assert ('countryCode' in data), 'Tournament.parse must have countryCode in data parameter'
        assert ('city' in data), 'Tournament.parse must have city in data parameter'
        assert ('owner' in data), 'Tournament.parse must have owner in data parameter'



        return Tournament(
            data['id'],
            data['name'],
            data['slug'],
            unix_to_datetime(data['startAt']),
            unix_to_datetime(data['endAt']),
            data['timezone'],
            data['isOnline'],
            data['countryCode'],
            data['city'],
            data['owner']['id'],
            data['owner']['player']['gamerTag']
        )

    def get_events(self):
        assert (self.id is not None), "tournament id cannot be None if calling get_events"
        data = NI.query(queries.get_tournament_events, {'id': self.id})
        validate_data(data)

        tournament_data = data['data']['tournament']
        if tournament_data is None:
            raise NoTournamentDataException(self.slug)

        base_data = tournament_data['events']
        if base_data is None:
            raise NoEventDataException(self.slug)

        return [i for i in [Event.parse(event_data) for event_data in base_data] if i is not None]  # Filter out empty events. Empty events are those without a valid videogame.

    def get_tournament_players(self):
        assert (self.id is not None), 'tournament id cannot be None if calling get_phase_groups'
        Logger.debug('Getting Players for Tournament: {0}:{1}'.format(self.id, self.name))
        data = NI.paginated_query(queries.get_tournament_players, {'id': self.id})
        # validate_data(data)
        return [i for i in [Player.parse(player_data) for player_data in data] if i is not None]

# from data_getter.packages_smashggpy.models.Event import Event
