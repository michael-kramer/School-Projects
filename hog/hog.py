"""The Game of Hog."""

from dice import four_sided, six_sided, make_test_dice
from ucb import main, trace, log_current_line, interact

GOAL_SCORE = 100 # The goal of Hog is to score 100 points.

######################
# Phase 1: Simulator #
######################

def roll_dice(num_rolls, dice=six_sided):
    """Roll DICE for NUM_ROLLS times. Return either the sum of the outcomes,
    or 1 if a 1 is rolled (Pig out). This calls DICE exactly NUM_ROLLS times.

    num_rolls:  The number of dice rolls that will be made;lu at least 1.
    dice:       A zero-argument function that returns an integer outcome.
    """
    # These assert statements ensure that num_rolls is a positive integer.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls > 0, 'Must roll at least once.'
    "*** YOUR CODE HERE ***"
    score = 0
    no_one = 2
    b = no_one
    seen_one = 5
    while num_rolls > 0:
        a = dice()
        score = score + a
        num_rolls -= 1
        if a == 1:
            b = seen_one
    if b == seen_one:
        return 1 
    else:
        return score

def take_turn(num_rolls, opponent_score, dice=six_sided):
    """Simulate a turn rolling NUM_ROLLS dice, which may be 0 (Free bacon).

    num_rolls:       The number of dice rolls that will be made.
    opponent_score:  The total score of the opponent.
    dice:            A function of no args that returns an integer outcome.
    """
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls >= 0, 'Cannot roll a negative number of dice.'
    assert num_rolls <= 10, 'Cannot roll more than 10 dice.'
    assert opponent_score < 100, 'The game should be over.'
    "*** YOUR CODE HERE ***"
    if num_rolls == 0:
        a = opponent_score // 10
        b = opponent_score - (a * 10)
        if a == 0: 
            return 1 + b
        else:
            return 1 + max(a,b)
    elif num_rolls > 0:
        return roll_dice(num_rolls, dice)


def select_dice(score, opponent_score):
    """Select six-sided dice unless the sum of SCORE and OPPONENT_SCORE is a
    multiple of 7, in which case select four-sided dice (Hog wild).
    """
    "*** YOUR CODE HERE ***"
    if (score + opponent_score) % 7 == 0:
        return four_sided
    else:
        return six_sided

def is_prime(n):
    """Return True if a non-negative number N is prime, otherwise return
    False. 1 is not a prime number!
    """
    assert type(n) == int, 'n must be an integer.'
    assert n >= 0, 'n must be non-negative.'
    if n == 0:
        return False
    if n == 1:
        return False
    k = 2
    while k < n:
        if n % k == 0:
            return False
        k += 1
    return True


def other(who):
    """Return the other player, for a player WHO numbered 0 or 1.

    >>> other(0)
    1
    >>> other(1)
    0
    """
    return 1 - who

def play(strategy0, strategy1, score0=0, score1=0, goal=GOAL_SCORE):
    """Simulate a game and return the final scores of both players, with
    Player 0's score first, and Player 1's score second.

    A strategy is a function that takes two total scores as arguments
    (the current player's score, and the opponent's score), and returns a
    number of dice that the current player will roll this turn.

    strategy0:  The strategy function for Player 0, who plays first
    strategy1:  The strategy function for Player 1, who plays second
    score0   :  The starting score for Player 0
    score1   :  The starting score for Player 1
    """
    who = 0  # Which player is about to take a turn, 0 (first) or 1 (second)
    "*** YOUR CODE HERE ***"
    while score0 < goal and score1 < goal:
        if who == 0:
            num_rolls = strategy0(score0,score1)
            dice = select_dice(score0, score1)
            total = take_turn(num_rolls,score1,dice)
            score0 = score0 + total
            is_prime(score0 + score1)
            if is_prime(score0 + score1) == True:
                if score0 > score1:
                    score0 += total
                if score0 < score1:
                    score1 += total
        if who == 1:
            num_rolls = strategy1(score1,score0)
            dice = select_dice(score0, score1)
            total = take_turn(num_rolls,score0,dice)
            score1 += total
            is_prime(score0 + score1)
            if is_prime(score0 + score1) == True:
                if score0 > score1:
                    score0 += total
                if score0 < score1:
                    score1 += total
        who = other(who)       
    return score0, score1  # You may want to change this line.

#######################
# Phase 2: Strategies #
#######################

def always_roll(n):
    """Return a strategy that always rolls N dice.

    A strategy is a function that takes two total scores as arguments
    (the current player's score, and the opponent's score), and returns a
    number of dice that the current player will roll this turn.

    >>> strategy = always_roll(5)
    >>> strategy(0, 0)
    5
    >>> strategy(99, 99)
    5
    """
    def strategy(score, opponent_score):
        return n
    return strategy

# Experiments

def make_averaged(fn, num_samples=1000):
    """Return a function that returns the average_value of FN when called.

    To implement this function, you will have to use *args syntax, a new Python
    feature introduced in this project.  See the project description.

    >>> dice = make_test_dice(3, 1, 5, 6)
    >>> averaged_dice = make_averaged(dice, 1000)
    >>> averaged_dice()
    3.75
    >>> make_averaged(roll_dice, 1000)(2, dice)
    6.0

    In this last example, two different turn scenarios are averaged.
    - In the first, the player rolls a 3 then a 1, receiving a score of 1.
    - In the other, the player rolls a 5 and 6, scoring 11.
    Thus, the average value is 6.0.
    """
    "*** YOUR CODE HERE ***"
    def make_average_return(*args):
        total = 0
        counter = num_samples
        while counter > 0:
            counter -= 1
            total = total + fn(*args) 
        average = total / num_samples
        return average
    return make_average_return

        

def max_scoring_num_rolls(dice=six_sided):
    """Return the number of dice (1 to 10) that gives the highest average turn
    score by calling roll_dice with the provided DICE.  Assume that dice always
    return positive outcomes.

    >>> dice = make_test_dice(3)
    >>> max_scoring_num_rolls(dice)
    10
    """
    "*** YOUR CODE HERE ***"
    average_return = make_averaged(roll_dice)
    n = 1
    highest = 0
    count = 0
    while n <= 10:
        new_average = average_return(n, dice)
        if new_average > highest:
            highest = new_average
            count = n
        n += 1
    return count

def winner(strategy0, strategy1):
    """Return 0 if strategy0 wins against strategy1, and 1 otherwise."""
    score0, score1 = play(strategy0, strategy1)
    if score0 > score1:
        return 0
    else:
        return 1

def average_win_rate(strategy, baseline=always_roll(5)):
    """Return the average win rate (0 to 1) of STRATEGY against BASELINE."""
    win_rate_as_player_0 = 1 - make_averaged(winner)(strategy, baseline)
    win_rate_as_player_1 = make_averaged(winner)(baseline, strategy)
    return (win_rate_as_player_0 + win_rate_as_player_1) / 2 # Average results

def run_experiments():
    """Run a series of strategy experiments and report results."""
    if True: # Change to False when done finding max_scoring_num_rolls
        six_sided_max = max_scoring_num_rolls(six_sided)
        print('Max scoring num rolls for six-sided dice:', six_sided_max)
        four_sided_max = max_scoring_num_rolls(four_sided)
        print('Max scoring num rolls for four-sided dice:', four_sided_max)

    if False: # Change to True to test always_roll(8)
        print('always_roll(8) win rate:', average_win_rate(always_roll(8)))

    if False: # Change to True to test bacon_strategy
        print('bacon_strategy win rate:', average_win_rate(bacon_strategy))

    if False: # Change to True to test prime_strategy
        print('prime_strategy win rate:', average_win_rate(prime_strategy))

    if False: # Change to True to test final_strategy
        print('final_strategy win rate:', average_win_rate(final_strategy))

    "*** You may add additional experiments as you wish ***"

# Strategies

def bacon_strategy(score, opponent_score, margin=8, num_rolls=5):
    """This strategy rolls 0 dice if that gives at least MARGIN points,
    and rolls NUM_ROLLS otherwise.
    """
    "*** YOUR CODE HERE ***"
    a = opponent_score // 10
    b = opponent_score - (a * 10)
    score_when_zero = 1 + max(a,b)
    if margin <= score_when_zero:
        return 0
    else:
        return num_rolls

def prime_strategy(score, opponent_score, margin=8, num_rolls=5):
    """This strategy rolls 0 dice when it results in a beneficial boost and
    rolls NUM_ROLLS if rolling 0 dice gives the opponent a boost. It also
    rolls 0 dice if that gives at least MARGIN points and rolls NUM_ROLLS
    otherwise.
    """
    "*** YOUR CODE HERE ***"
    
    bacon_gives = 1 + max([int(raw_digit) for raw_digit in str(opponent_score)])
    score_with_bacon = score + bacon_gives
    
    if is_prime(score_with_bacon + opponent_score) and score_with_bacon != opponent_score: # Hogtimus prime rule will give someone a boost if I roll 0
        if score_with_bacon > opponent_score:
            return 0
        else: 
            return num_rolls
    if bacon_gives >= margin:
        return 0
    return num_rolls



def final_strategy(score, opponent_score):
    """Write a brief description of your final strategy.

    *** YOUR DESCRIPTION HERE ***
    """
    "*** YOUR CODE HERE ***"
    needed = GOAL_SCORE - score
    
    bacon_gives = 1 + max([int(raw_digit) for raw_digit in str(opponent_score)]) # exactly how many points I'll get should I roll no dice and let Free bacon be invoked
    bacon_bonus = 0 
    if is_prime(score + bacon_gives + opponent_score) and score + bacon_gives != opponent_score: # Hogtimus prime rule will give someone a boost if I roll 0
        if score + bacon_gives > opponent_score: # I would get the boost
            bacon_gives *= 2
            if ((score + 2 * bacon_gives) + opponent_score) % 7 == 0: # this would then put my opponent in a 4-sided-dice position because of Hog wild
                bacon_bonus = 4
        else: # Opponent would get the boost
            bacon_gives = 0 # it won't help my score at all, because it'll help my opponent as much as me
            if ((score + bacon_gives) + (opponent_score + bacon_gives)) % 7 == 0: # this would then put my opponent in a 4-sided-dice position
                bacon_bonus = 4
    else:
        if ((score + bacon_gives) + opponent_score) % 7 == 0:
            bacon_bonus = 4

    if bacon_gives >= needed: 
        return 0

    dice_sides = 6
    if (score + opponent_score) % 7 == 0: 
        dice_sides = 4
    
    def average_result(num_rolls, dice_sides):
        chance_of_1 = 1 - ((dice_sides - 1) / dice_sides) ** num_rolls
        return 1 * chance_of_1 + (num_rolls * (1 + dice_sides / 2)) * (1 - chance_of_1)
    
    max_average = bacon_gives + bacon_bonus
    max_average_num_rolls = 0
    for this_num_rolls in range(1, 11):
        this_average = average_result(this_num_rolls, dice_sides)
        if this_average > needed + 4:
            return this_num_rolls
        if this_average > max_average:
            max_average = this_average
            max_average_num_rolls = this_num_rolls
    return max_average_num_rolls


##########################
# Command Line Interface #
##########################

# Note: Functions in this section do not need to be changed.  They use features
#       of Python not yet covered in the course.


@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions.

    This function uses Python syntax/techniques not yet covered in this course.
    """
    import argparse
    parser = argparse.ArgumentParser(description="Play Hog")
    parser.add_argument('--run_experiments', '-r', action='store_true',
                        help='Runs strategy experiments')
    args = parser.parse_args()

    if args.run_experiments:
        run_experiments()
