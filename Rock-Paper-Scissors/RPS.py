import random

"""
Here I'm trying to get 60+% of winning plays in Rock Paper Scissor game.
As my code will face different bots which use different strategics, I define here 5 different ways to generate 
moves (you can as suggest/use more like Markov chains, random algorithms etc I couldn't perform them well enough to reach
the goal, but maybe you'll be more lucky). 
I leave some comments, hope you will find it useful.
AK.
"""

#MAIN FUNCTIONS, RECIEVE OPPONENT MOVE AND RETURNS ONE
def player(prev_move, opponent_history=[], my_history=[], strategies_history=[], scoring_for_strategy=[],
           pairs=[]):
    if prev_move == "":
        opponent_history.clear()
        my_history.clear()
        scoring_for_strategy.clear()
        strategies_history.clear()
        pairs.clear()
        for _ in range(5):
            strategies_history.append([])
            scoring_for_strategy.append(0)
        pairs.append({'RRR': 0, 'RRP': 0, 'RRS': 0,
                      'RPR': 0, 'RPP': 0, 'RPS': 0,
                      'RSR': 0, 'RSP': 0, 'RSS': 0,
                      'PRR': 0, 'PRP': 0, 'PRS': 0,
                      'PPR': 0, 'PPP': 0, 'PPS': 0,
                      'PSR': 0, 'PSP': 0, 'PSS': 0,
                      'SRR': 0, 'SRP': 0, 'SRS': 0,
                      'SPR': 0, 'SPP': 0, 'SPS': 0,
                      'SSR': 0, 'SSP': 0, 'SSS': 0})
    actions = ['R', 'P', 'S']
    strategies_number = 5
    opponent_history.append(prev_move)
    rounds = len(opponent_history)
    my_play, pairs, strategies_history = \
        manage_strategies(actions, opponent_history, my_history, pairs, rounds, strategies_history,
                          strategies_number, scoring_for_strategy)
    my_history.append(my_play)
    return (my_play)

#FUNCTION THAT PERFORMS DIFFERENT LOGICS AND CHOOSE THE OPTIMUM ONE
def manage_strategies(actions, opponent_history, my_history, pairs, rounds, strategies_history, strategies_number, scoring_for_strategy):
    if rounds <= 3:
        start = False
        my_play = random_agent(actions)
    else:
        start = True

    if rounds >= 3:
        reward = get_reward(my_history[-1], opponent_history[-1])
        # APPLYING LOGIC 5
        greedy_play, pairs = greedy(pairs, my_history[-2]+opponent_history[-2],opponent_history[-1],my_history[-1],reward,actions)
        # APPLYING LOGIC 3
        foresee_v1_play = foresee_v1(opponent_history[-1])
        # APPLYING LOGIC 4
        foresee_v2_play = foresee_v2(my_history[-1])
        # APPLYING LOGIC 1
        random_agent_play = random_agent(actions)
        # APPLYING LOGIC 2
        semi_random_agent_play = semi_random_agent(opponent_history[-1])
        # PUTTING TOGETHER ALL
        my_play_candidates = [random_agent_play, semi_random_agent_play, foresee_v1_play, foresee_v2_play, greedy_play]
        for i in range(strategies_number):
            strategies_history[i].append(my_play_candidates[i])
        if start:
            scoring_for_strategy = Update_scoring_for_strategy(strategies_history, opponent_history[-1], scoring_for_strategy,
                                                       strategies_number)
            best_strategy = scoring_for_strategy.index(max(scoring_for_strategy))
            my_play = my_play_candidates[best_strategy]

    return my_play, pairs, strategies_history


def Update_scoring_for_strategy(strategies_history, prev_opponent_play, scoring_for_strategy, strategies_number):
    for i in range(strategies_number):
        scoring_for_strategy[i] += get_reward(strategies_history[i][-1], prev_opponent_play)
    return scoring_for_strategy


# LOGIC 1: GIVE ABSOLUTELY RANDOM MOVE
def random_agent(actions):
    shuffled_actions = actions
    random.shuffle(shuffled_actions)
    my_play = random.choice(shuffled_actions)
    return my_play


# LOGIC 2: GIVE SEMI RANDOM MOVE, EXCLUDING PREVIOUS MOVE
def semi_random_agent(prev_move):
    if (prev_move == 'R'):
        my_play = random.choice(['P', 'S'])
    elif (prev_move == 'P'):
        my_play = random.choice(['R', 'S'])
    else:
        my_play = random.choice(['R', 'P'])
    return my_play


# LOGIC 3: GIVE A MOVE BASED ON PREVIOUS MOVE MADE BY COMPUTER, OPPONENT
def foresee_v1(prev_move):
    if (prev_move == 'R'):
        my_play = 'S'
    elif (prev_move == 'P'):
        my_play = 'R'
    else:
        my_play = 'P'
    return my_play


# LOGIC 4: GIVE A MOVE BASED ON MY PREVIOUS MOVE
def foresee_v2(my_prev_move):
    if (my_prev_move == 'R'):
        my_play = 'S'
    elif (my_prev_move == 'P'):
        my_play = 'R'
    else:
        my_play = 'P'
    return my_play


# LOGIC 5: GIVE A MOVE BY COMBINATION OF PREVIOUS RESULT
# E.G. my previous move is S and opponent move is R so based on the score it chooses the maximum between SRR, SRP and SRS to decide the next move
def greedy(pairs, prev_state, opponent_prev_move, my_prev_move, reward, actions):
    pairs[0][prev_state + my_prev_move] += reward - 1
    available_actions = [pairs[0][my_prev_move + opponent_prev_move + i] for i in ['R', 'P', 'S']]
    best_action = available_actions.index(max(available_actions))
    my_play = actions[best_action]
    return my_play, pairs


# EVALUATION FUNCTION THAT APPLIES THE RULES OF THE GAME TO FIND THE WINNER, VALUES ARE 1 FOR A WIN, -1 FOR A LOSS, AND 0 FOR A TIE.
def get_reward(play1, play2):
    if (play1 == 'R'):
        if (play2 == 'S'):
            res = 1
        elif (play2 == 'P'):
            res = -1
        else:
            res = 0
    if (play1 == 'P'):
        if (play2 == 'R'):
            res = 1
        elif (play2 == 'S'):
            res = -1
        else:
            res = 0
    if (play1 == 'S'):
        if (play2 == 'P'):
            res = 1
        elif (play2 == 'R'):
            res = -1
        else:
            res = 0
    return res
