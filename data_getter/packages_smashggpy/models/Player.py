from os import stat


class Player(object):

    def __init__(self, id, name, country, city, pronouns):
        self.id = id
        self.name = name
        self.country = country
        self.city = city
        self.pronouns = pronouns

    def __eq__(self, other):
        if other is None:
            return False
        if type(other) != type(self):
            return False
        return hash(other) == hash(self)

    def __hash__(self):
        return hash((self.id, self.name, self.country, self.city, self.pronouns))

    @staticmethod
    def parse(data):
        datalist = []
        assert (data is not None), 'Player.parse must not have a none data parameter'

        if data['player']['user'] is None:
            country_name = None
            city_name = None
            pronouns = None
        else:
            if data['player']['user']['location'] is None or data['player']['user']['location']['country'] is None:
                country_name = None
            else:
                country_name = data['player']['user']['location']['country'].title()

            if data['player']['user']['location'] is None or data['player']['user']['location']['city'] is None:
                city_name = None
            else:
                city_name = data['player']['user']['location']['city'].title()

            if data['player']['user']['genderPronoun'] is None:
                pronouns = None
            else:
                pronouns = data['player']['user']['genderPronoun'].lower()
            
        return Player(
                data['player']['id'],
                data['player']['gamerTag'],
                country_name,
                city_name,
                pronouns
                )
