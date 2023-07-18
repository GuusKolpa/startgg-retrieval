from os import stat
from data_getter.packages_smashggpy.models.EntrantPlayerLink import EntrantPlayer


class Entrant(object):

    def __init__(self, id, event_id, name, placement, is_team):
        self.id = id
        self.event_id = event_id
        self.name = name
        self.placement = placement
        self.is_team = is_team

    def __eq__(self, other):
        if other is None:
            return False
        if type(other) != type(self):
            return False
        return hash(other) == hash(self)

    def __hash__(self):
        return hash((self.id, self.player_id, self.event_id, self.placement))

    @staticmethod
    def parse(data):
        assert (data is not None), 'Entrant.parse must not have a none data parameter'
        assert ('event' in data), 'Entrant.parse must have a event property in data parameter'
        assert ('name' in data), 'Entrant.parse must have a name property in data parameter'
        assert ('standing' in data), 'Entrant.parse must have a standing property in data parameter'
        assert ('participants' in data), 'Entrant.parse must have a participants property in data parameter'

        if data['standing'] is None:  ## Players who do not have results are not taken into account
            standing = None
        else:
            standing = str(data['standing']['placement'])

        if data['team'] is None:
            is_team = False
        else:
            is_team = True


        return Entrant(
                data['id'],
                data['event']['id'],
                data['name'],
                standing,
                is_team
                )
