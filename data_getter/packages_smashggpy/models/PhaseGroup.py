import data_getter.packages_smashggpy.queries.Phase_Group_Queries as queries
from data_getter.packages_smashggpy.common.Common import flatten, validate_data, unix_to_datetime
from data_getter.packages_smashggpy.util.Logger import Logger
from data_getter.packages_smashggpy.util.NetworkInterface import NetworkInterface as NI
from data_getter.packages_smashggpy.common.Exceptions import DataMalformedException, NoPhaseGroupDataException
from data_getter.packages_smashggpy.models.GGSet import GGSet

class PhaseGroup(object):

    def __init__(self, id, event_id, phase_sub_id, name, bracket_type):
        self.id = id
        self.event_id = event_id
        self.phase_sub_id = phase_sub_id
        self.name = name
        self.bracket_type = bracket_type

    def __eq__(self, other):
        if other is None:
            return False
        if type(other) != type(self):
            return False
        return hash(other) == hash(self)

    def __hash__(self):
        return hash((self, self.id, self.event_id, self.phase_sub_id, self.name, self.bracket_type))

    @staticmethod
    def validate_data(input, id: int=0):
        if 'data' in input:
            raise DataMalformedException(input,
                                         'data is malformed for PhaseGroup.parse. '
                                         'Please give only what is contained in the '
                                         '"phaseGroup" property')
        if 'phaseGroup' not in input and 'phaseGroups' not in input:
            raise NoPhaseGroupDataException(id)
        elif 'phaseGroup' in input and input['phaseGroup'] is None:
            raise NoPhaseGroupDataException(id)
        elif 'phaseGroups' in input and input['phaseGroups'] is None:
            raise NoPhaseGroupDataException(id)

    @staticmethod
    def get(id: int):
        assert (id is not None), "PhaseGroup.get cannot have None for id parameter"
        data = NI.query(queries.phase_group_by_id, {'id': id})
        validate_data(data)
        PhaseGroup.validate_data(data['data'])

        base_data = data['data']['phaseGroup']
        return PhaseGroup.parse(base_data)

    @staticmethod
    def parse(data):
        assert (data is not None), "PhaseGroup.parse cannot have None for data parameter"
        if 'data' in data:
            raise DataMalformedException(data,
                                         'data is malformed for PhaseGroup.parse. '
                                         'Please give only what is contained in the '
                                         '"phaseGroup" property')

        assert ('id' in data), 'PhaseGroup.parse must have a id property in data parameter'
        assert ('displayIdentifier' in data), \
            'PhaseGroup.parse cannot must have a displayIdentifier property in data parameter'
        assert (data['displayIdentifier'] is not None), \
            'displayIdentifier can not be empty'
        assert ('phase' in data), 'PhaseGroup.parse cannot must have a phase property in data parameter'
        assert ('bracketType' in data), 'PhaseGroup.parse cannot must have a phase property in data parameter'

        return PhaseGroup(
            data['id'],
            data['phase']['event']['id'],
            data['displayIdentifier'],
            data['phase']['name'],
            data['bracketType']
        )

    def get_sets(self):
        assert (self.id is not None), 'phase group id cannot be None when calling get_sets'
        Logger.debug('Getting Sets for phase group: {0}:{1}'.format(self.id, self.name+" "+self.phase_sub_id))
        data = NI.paginated_query(queries.phase_group_sets, {'id': self.id})
        sets = [i for i in [GGSet.parse(set_data) for set_data in data] if i is not None]
        return sets