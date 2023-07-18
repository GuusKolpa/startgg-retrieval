from os import stat


class EntrantPlayer(object):

    def __init__(self, event_id, player_id):
        self.id = int(str(event_id)+str(player_id))
        self.event_id = event_id
        self.player_id = player_id

    def __eq__(self, other):
        if other is None:
            return False
        if type(other) != type(self):
            return False
        return hash(other) == hash(self)

    def __hash__(self):
        return hash((self.event_id, self.player_id,))

    @staticmethod
    def parse(data):
        datalist = []
        assert (data is not None), 'EntrantPlayer.parse must not have a none data parameter'
        assert ('id' in data), 'EntrantPlayer.parse must have a event property in data parameter'
        assert ('participants' in data), 'EntrantPlayer.parse must have a participants property in data parameter'

        for i in range(len(data['participants'])):
            datalist.append(EntrantPlayer(
                data['id'],
                data['participants'][i]['player']['id'],
                )
            )

        return datalist