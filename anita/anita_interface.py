import copy

default_trait_weight_dict = {'O_weight': 1, 'C_weight': 1, 'E_weight': 1, 'A_weight': 1, 'N_weight': 1}

class Anita_Persona:
    def __init__(self, _avatar_name, _AT, _trait_weight_dict = default_trait_weight_dict):
        self.avatar_name = _avatar_name
        self.trait_weight_dict = _trait_weight_dict
        self.AT = _AT

        self.O_final = self.AT.O_score * _trait_weight_dict['O_weight']
        self.C_final = self.AT.C_score * _trait_weight_dict['C_weight']
        self.E_final = self.AT.E_score * _trait_weight_dict['E_weight']
        self.A_final = self.AT.A_score * _trait_weight_dict['A_weight']
        self.N_final = self.AT.N_score * _trait_weight_dict['N_weight']

        self.anita_reward = sum([self.O_final, self.C_final, self.E_final, self.A_final, self.N_final])


class Anita_Trait:
    def __init__(self, _TI, _n_features, _n_actions):
        self.TI = copy.deepcopy(_TI)
        self.n_features = _n_features
        self.n_actions = _n_actions
        self.O_score = 0
        self.C_score = 0 + self.if_more_hold() * 1/1
        self.E_score = 0
        self.A_score = 0
        self.N_score = 0

    def if_more_hold(self):
        hold_amount = 0
        for i in self.TI.trade_log:
            if i['trade_unit'] == 0:
                hold_amount += 1
        if hold_amount >= self.n_features / self.n_actions:
            return 1
        else:
            return -1


def in_ai():
    print('now in anita_interface')