import operator as op
from functools import reduce

def ncr(n, r):
    r = min(r, n-r)
    if r == 0: return 1
    numer = reduce(op.mul, range(n, n-r, -1))
    denom = reduce(op.mul, range(1, r+1))
    return numer//denom

def state_generator_2(cards, n_players):
    n_cards = len(cards)
    for i in range(len(cards)):
        first_cards = cards[i]
        for second_cards in cards[i+1:]:
            state = [first_cards, second_cards]
            if (n_players > 1):
                card_left = cards[:]
                card_left.remove(first_cards)
                card_left.remove(second_cards)
                st_gen_2 = state_generator_2(card_left, n_players-1)
                for state_for_less_pl in st_gen_2:
                    st = state[:]
                    st.extend(state_for_less_pl)
                    yield st
            else:
                yield state








class KripkeModel():

    def __init__(self, n_of_players, cards, open_cards):
        self.n_of_players = n_of_players
        self.n_of_cards = len(cards)
        self.n_of_cards_for_player = (self.n_of_cards - 1) // self.n_of_players
        self.n_of_open_cards = len(open_cards)

        n_without_open = self.n_of_cards - self.n_of_open_cards

        self.n_of_states = n_without_open
        cards_left = n_without_open - 1
        for i in range(1, self.n_of_players):
            variant_for_player = ncr(cards_left, self.n_of_cards_for_player)
            self.n_of_states *= variant_for_player
            cards_left -= self.n_of_cards_for_player

        cards_without_open = cards
        for card in open_cards:
            cards_without_open.remove(tuple(card))

        self.states = []

        for hiden_card in cards_without_open:
            card_for_players = cards_without_open[:]
            card_for_players.remove(hiden_card)
            state_gen = state_generator_2(card_for_players, n_of_players)
            for st in state_gen:
                s = [hiden_card]
                s.extend(st)
                self.states.append(s)

        l = len(self.states)
        print(l)


    def get_possible_cards(self, known_player, known_player_cards):
        positions = {0: set(), 1: set(), 2: set(), 3: set()} # 0 = hidden card
        probobilities = {0: {}, 1: {}, 2: {}, 3: {}} # 0 = hidden card
        known_card_n_1 = 1+(known_player-1)*2
        known_card_n_2 = 2+(known_player-1)*2

        known_tuple = [(known_player_cards[0][0], known_player_cards[0][1]), (known_player_cards[1][0], known_player_cards[1][1])]

        total_number_of_words = 0
        for st in self.states:
            if (st[known_card_n_1] == known_tuple[0]) or (st[known_card_n_1] == known_tuple[1]):
                if (st[known_card_n_2] == known_tuple[0]) or (st[known_card_n_2] == known_tuple[1]):
                    total_number_of_words += 1
                    for key in positions.keys():
                        if key != known_player:
                            if key == 0: # hidden
                                if st[0] in positions[0]:
                                    probobilities[0][st[0]] += 1
                                else:
                                    positions[0].add(st[0])
                                    probobilities[0][st[0]] = 1
                            else:
                                #add card 1
                                unknown_card_n_1 = 1 + (key - 1) * 2
                                if st[unknown_card_n_1] in positions[key]:
                                    c = st[unknown_card_n_1]
                                    probobilities[key][st[unknown_card_n_1]] += 1
                                else:
                                    positions[key].add(st[unknown_card_n_1])
                                    probobilities[key][st[unknown_card_n_1]] = 1

                                #add card 2
                                unknown_card_n_2 = 2 + (key - 1) * 2
                                if st[unknown_card_n_2] in positions[key]:
                                    probobilities[key][st[unknown_card_n_2]] += 1
                                else:
                                    positions[key].add(st[unknown_card_n_2])
                                    probobilities[key][st[unknown_card_n_2]] = 1
        return (positions, probobilities, total_number_of_words)


    def apply_single_card_anouncment(self, player_n, has, number, colour):
        card_n_1 = 1+(player_n-1)*2
        card_n_2 = 2+(player_n-1)*2
        if has:
            self.states = [st for st in self.states if ((st[card_n_1][0] == number) and (st[card_n_1][1] == colour)) or \
                           ((st[card_n_2][0] == number) and (st[card_n_2][1] == colour))]
        else:
            self.states = [st for st in self.states if not ((st[card_n_1][0] == number) and (st[card_n_1][1] == colour)) and \
                           not ((st[card_n_2][0] == number) and (st[card_n_2][1] == colour))]

    def apply_number_of_cards_anouncment(self, player_n, number, prop, value):
        n_prop = 0 if prop == "number" else 1
        card_n_1 = 1+(player_n-1)*2
        card_n_2 = 2+(player_n-1)*2
        good_st = []
        for st in self.states:
            number_for_st = 0
            if st[card_n_1][n_prop] == value:
                number_for_st += 1
            if st[card_n_2][n_prop] == value:
                number_for_st += 1
            if (number_for_st == number):
                good_st.append(st)
        self.states = good_st

if __name__ == "__main__":
    x = [1,2]
    y = [3,4]
    x.extend(y)
    print(x)