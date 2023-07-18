from data_getter.packages_smashggpy.common.Common import flatten, validate_data, unix_to_datetime
import re

from data_getter.packages_smashggpy.util.Logger import Logger

DISPLAY_SCORE_REGEX = re.compile('^([\S\s]*) ([0-9]{1,3}) - ([\S\s]*) ([0-9]{1,3})$')

class GGSet(object):

    def __init__(self, id, phase_group_id, player1_id, player2_id, score1,
                 score2, round_text, completed_at):
        self.id = id
        self.phase_group_id = phase_group_id
        self.player1_id = player1_id
        self.player2_id = player2_id
        self.score1 = score1
        self.score2 = score2
        self.round_text = round_text
        self.completed_at = completed_at

    def __eq__(self, other):
        if other is None:
            return False
        if type(other) != type(self):
            return False
        return hash(other) == hash(self)

    def __hash__(self):
        return hash((self.id, self.phase_group_id, self.player1_id, self.player2_id, self.score1,
                     self.score2, self.round_text, self.completed_at))

    def __str__(self):
        return 'Set ({0}) :: {1} :: {2} {3} - {4} {5}' \
            .format(self.id, self.round_text, self.player1_id, self.score1, self.score2, self.player2_id)

    @staticmethod
    def parse(data):
        
        assert (data is not None), 'GGSet.parse cannot have a none data parameter'
        assert ('id' in data), 'GGSet.parse must have an id property in data parameter'
        assert ('phaseGroup' in data), 'GGset.parse must have a phaseGroups property in data parameter'
        if data['state'] != 3: ## Only returning full sets
                    Logger.debug('Set with id \'{}\' not completed. No data saved.'.format(data['id']))
                    return None
        display_score_parsed = GGSet.parse_display_score(data)
        """
        assert ('p1_tag' in data), 'GGSet.parse must resolve p1_tag property in display score'
        assert ('p2_tag' in data), 'GGSet.parse must resolve p2_tag property in display score'
        assert ('p1_score' in data), 'GGSet.parse must resolve p1_score property in display score'
        assert ('p2_score' in data), 'GGSet.parse must resolve p2_score property in display score'
        """
        

        return GGSet(
            data['id'],
            data['phaseGroup']['id'],
            data['slots'][0]['entrant']['id'],
            data['slots'][1]['entrant']['id'],
            display_score_parsed['p1_score'],
            display_score_parsed['p2_score'],
            data['fullRoundText'],
            unix_to_datetime(data['completedAt'])
        )


    @staticmethod
    def parse_display_score(inp_data):
        ret = {
            'p1_tag': None,
            'p1_score': None,
            'p2_tag': None,
            'p2_score': None
        }

        if inp_data['displayScore'] is not None and inp_data['displayScore'] != '':
            matches = DISPLAY_SCORE_REGEX.match(inp_data['displayScore'])
            if matches is not None:
                ret['p1_tag'] = matches.group(1)
                ret['p1_score'] = matches.group(2)
                ret['p2_tag'] = matches.group(3)
                ret['p2_score'] = matches.group(4)
            elif inp_data['displayScore'] == 'DQ':
                if inp_data['slots'][0]['standing']['placement'] == 1:
                    ret['p1_score'] = 0
                    ret['p2_score'] = -1
                else:
                    ret['p1_score'] = -1
                    ret['p2_score'] = 0
            else:
                if inp_data['slots'][0]['standing']['placement'] == 1:
                    ret['p1_score'] = 1
                    ret['p2_score'] = 0
                else:
                    ret['p1_score'] = 0
                    ret['p2_score'] = 1
        return ret