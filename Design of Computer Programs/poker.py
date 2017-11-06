# straight(ranks): returns True if the hand is a straight.
# flush(hand):     returns True if the hand is a flush.
# kind(n, ranks):  returns the first rank that the hand has
#                  exactly n of. For A hand with 4 sevens
#                  this function would return 7.
# two_pair(ranks): if there is a two pair, this function
#                  returns their corresponding ranks as a
#                  tuple. For example, a hand with 2 twos
#                  and 2 fours would cause this function
#                  to return (4, 2).
# card_ranks(hand) returns an ORDERED tuple of the ranks
#                  in a hand (where the order goes from
#                  highest to lowest rank).

import random # this will be a useful library for shuffling

# This builds a deck of 52 cards. If you are unfamiliar
# with this notation, check out Andy's supplemental video
# on list comprehensions (you can find the link in the
# Instructor Comments box below).

mydeck = [r+s for r in '23456789TJQKA' for s in 'SHDC']

def deal(numhands, n=5, deck=mydeck):
    # shuffle the deck and deal out numhands n-card hands.
    random.shuffle(deck)
    return [deck[n*i:n*(i+1)] for i in range(numhands)]

def poker(hands):
    "return the best hand: pocker([hand, ...]) => [hand, ...]"
    return allmax(hands, key=hand_rank)

def allmax(iterable, key=None):
    "Return a list of all items equal to the max of the iterable."
    max_hand = max(iterable, key=key)
    key = key or (lambda x: x)
    return [hand for hand in iterable if key(hand) == key(max_hand)]

# lesson version
def allmax_(iterable, key=None):
    "Return a list of all items equal to the max of the iterable."
    result, maxval = [], None
    key = key or (lambda x: x)
    for x in iterable:
        xval = key(x)
        if not result or xval > maxval:
            result, maxval = [x], xval
        elif xval == maxval:
            result.append(x)
    return result

# flush: same suits
# straight: consecutive
def hand_rank_(hand):
    "Return a value indicating the ranking of a hand."
    ranks = card_ranks(hand)
    if straight(ranks) and flush(hand):            # straight flush
        return (8, max(ranks))
    elif kind(4, ranks):                           # 4 of a kind
        return (7, kind(4, ranks), kind(1, ranks))
    elif kind(3, ranks) and kind(2, ranks):        # full house
        return (6, kind(3, ranks), kind(2, ranks))
    elif flush(hand):                              # flush
        return (5, ranks)
    elif straight(ranks):                          # straight
        return (4, max(ranks))
    elif kind(3, ranks):                           # 3 of a kind
        return (3, kind(3, ranks), ranks)
    elif two_pair(ranks):                          # 2 pair
        return (2, two_pair(ranks), ranks)
    elif kind(2, ranks):                           # kind
        return (1, kind(2, ranks), ranks)
    else:                                          # high card
        return (0, ranks)

'''DRY: don't repeat yourself'''
# refactored version
def hand_rank(hand):
    "Return a value indicating how high the hand ranks"
    # counts is the count of each rank; ranks lists corresponding ranks
    # E.g. '7 T 7 9 7' => counts = (3, 1, 1); ranks = (7, 10, 9)
    groups = group(['--23456789TJQKA'.index(r) for r,s in hand])
    counts, ranks = unzip(groups)
    if ranks == (14, 5, 4, 3, 2):
        ranks = (5, 4, 3, 2, 1)
    straight = len(ranks) == 5 and max(ranks) - min(ranks) == 4
    flush = len(set([s for r,s in hand])) == 1
    return (9 if (5,) == counts else
            8 if straight and flush else
            7 if (4, 1) == counts else
            6 if (3, 2) == counts else
            5 if flush else
            4 if straight else
            3 if (3, 1, 1) == counts else
            2 if (2, 2, 1) == counts else
            1 if (2, 1, 1, 1) == counts else
            0), ranks
    # can be replaced by more elegant expression
    # return max(count_rankings[counts], 4*straight + 5*flush), ranks
count_rankings = {(5,):10, (4, 1):7, (3, 2):6, (3, 1, 1):3, (2, 2, 1):2,
                    (2, 1, 1, 1):1, (1, 1, 1, 1, 1):0}

def group(items):
    "Return a list of [(count, x)...], highest count first, then highest x first."
    groups = [(items.count(x), x) for x in set(items)]
    return sorted(groups, reverse=True)

def unzip(pairs): return zip(*pairs)


def card_ranks(hand):
    "Return a list of the ranks, sorted with higher first."
    ranks = ['--23456789TJQKA'.index(r) for r,s in hand]
    ranks.sort(reverse=True)
    return [5, 4, 3, 2, 1] if (ranks == [14, 5, 4, 3, 2]) else ranks

def straight(ranks):
    "Return True if the ordered ranks form a 5-card straight."
    return (max(ranks) - min(ranks) == 4) and len(set(ranks)) == 5

# my version
def straight_(ranks):
    "Return True if the ordered ranks form a 5-card straight."
    rank_last = ranks[0]
    for rank in ranks[1:]:
        if rank != rank_last - 1:
            return False
        rank_last = rank

    return True

def flush(hand):
    "Return True if all the cards have the same suit."
    suits = [s for r, s in hand]
    return len(set(suits)) == 1

# my version
def flush_(hand):
    "Return True if all the cards have the same suit."
    suit = hand[0][1]
    for r, s in hand[1:]:
        if s != suit:
            return False
    return True

def kind(n, ranks):
    """Return the first rank that this hand has exactly n of.
    Return None if there is no n-of-a-kind in the hand."""
    for r in ranks:
        if ranks.count(r) == n:
            return r
    return None


# my version
def kind_(n, ranks):
    """Return the first rank that this hand has exactly n of.
    Return None if there is no n-of-a-kind in the hand."""
    counts = [(rank, ranks.count(rank)) for rank in set(ranks)]
    counts.sort(key=lambda count: count[0], reverse=True)
    for rank, count in counts:
        if count == n:
            return rank

    return None

def two_pair(ranks):
    """If there are two pair, return the two ranks as a
    tuple: (highest, lowest); otherwise return None."""
    pair = kind(2, ranks)
    lowpair = kind(2, list(reversed(ranks)))
    if pair and lowpair != pair:
        return (pair, lowpair)
    else:
        return None

# my version
def two_pair_(ranks):
    """If there are two pair, return the two ranks as a
    tuple: (highest, lowest); otherwise return None."""
    highest = None
    lowest = None
    for r in ranks:
        if ranks.count(r) == 2:
            if not highest:
                highest = r
            elif highest != r:
                lowest = r
    if highest and lowest:
        return highest, lowest
    return None

def test():
    "test cases for the functions in the poker program"
    # suits: diamonds, clubs, hearts, spades
    sf = "6C 7C 8C 9C TC".split() # straight flush
    fk = "9D 9H 9S 9C 7D".split() # four of a kind
    fh = "TD TC TH 7C 7D".split() # full house
    tp = "5S 5D 9H 9C 6S".split() # Two pairs
    al = "AC 2D 4H 3D 5S".split() # Ace-Low Straight
    assert straight(card_ranks(al)) == True

    fkranks = card_ranks(fk)
    tpranks = card_ranks(tp)
    assert kind(4, fkranks) == 9
    assert kind(3, fkranks) == None
    assert kind(2, fkranks) == None
    assert kind(1, fkranks) == 7
    assert straight([9, 8, 7, 6, 5]) == True
    assert straight([9, 8, 8, 6, 5]) == False
    assert flush(sf) == True
    assert flush(fk) == False
    assert card_ranks(sf) == [10, 9, 8, 7, 6]
    assert card_ranks(fk) == [9, 9, 9, 9, 7]
    assert card_ranks(fh) == [10, 10, 10, 7, 7]
    assert poker([sf, fk, fh]) == [sf]
    assert poker([fk, fh]) == [fk]
    assert poker([fh, fh]) == [fh,fh]
    assert poker([sf]) == [sf]
    assert poker([sf] + 99*[fh]) == [sf]
    assert hand_rank(sf) == (8, (10,9,8,7,6))#(8, 10)
    assert hand_rank(fk) == (7, (9,7))
    assert hand_rank(fh) == (6, (10,7))


    return "tests pass"

print test()

hand_names = list(reversed(["Straight Flush", "4 of a kind", "Full house", "Flush",
                "Straight", "3 of a kind", "2 pair", "Pair", "High card"]))
def hand_percentage(n=700*1000):
    "Sample n random hands and print a table of percentage for each type of hand."
    counts = [0] * 9
    for i in range(n/10):
        for hand in deal(10):
            ranking = hand_rank(hand)[0] # obtain the rank of this hand
            counts[ranking] += 1

    for i in reversed(range(9)):
        print "%14s: %6.3f %%" % (hand_names[i], 100.*counts[i]/n)
print hand_percentage()

# shuffle algorithm
def shuffle(deck):
    "Knuth's Algorithm P."
    N = len(deck)
    for i in range(N-1):
        swap(deck, i, random.randrange(i, N))
    return deck

def swap(deck, i, j):
    "Swap elements i and j of a collection."
    print 'swap', i, j
    deck[i], deck[j] = deck[j], deck[i]
deck = [1, 2, 3, 4]
print deck, '\n', shuffle(deck)
