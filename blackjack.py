import requests
import json

'''-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-Mazz's BLACKJACK Table-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
This is a Blackjack Card game I re-created out of boredom, upon coming across a deck of cards API.
API = "https://deckofcardsapi.com/"

Another way to do this manually:

    for suit in ("Hearts", "Diamonds", "Clubs", "Spades"):
        for val in range(2, 15):
            deck.append((val, suit))
    
    Then Define face cards with a function similar to below: p_face_cards()
        

Using the API allowed me to play around with JSON objects, and required much more functionality. 

I will try my best to clean up the code in a future update. I realize some things are a bit messy.
'''


# TODO: #1) Track Player + Dealer Cards [DONE]
#       #2) Track Player + Dealer Score [DONE]
#       #3) Betting System [DONE]
#       #4) Player Hit/Stay functionality [DONE]
#       #6) Double-Down
#       #7) Keep counts and let player know when deck is "Hot" or "Cold"


# Gets 1 deck of cards using 'deckofcards' API.
def get_deck(count):
    api_req = requests.get(f'https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count={count}')
    deck = json.loads(api_req.text)

    success = deck['success']
    deck_id = deck['deck_id']
    remaining = deck['remaining']
    shuffled = deck['shuffled']

    return deck_id, remaining


# DECK ID && Remaining Card count
DECK_ID, REMAINING = get_deck(1)


# Handles Player Face Card Values
def p_face_cards(card: list):
    if card[0] == str:
        card[0] = int(card[0])

    elif card[0] == 'Jack'.upper():
        card[0] = 10

    elif card[0] == 'Queen'.upper():
        card[0] = 10

    elif card[0] == 'King'.upper():
        card[0] = 10

    elif card[0] == 'Ace'.upper():
        while True:
            choice = input("[1] Ace = 1\n"
                           "[2] Ace = 11\n"
                           "Choice: ")
            if choice == str(int(1)):
                card[0] = 1
                break
            elif choice == str(int(2)):
                card[0] = 11
                break
            else:
                print("That is not an option...")

    value = card[0]
    suit = card[1]

    return value, suit


# Handles Dealer face card values.
def d_face_cards(card: list):
    if card[0] == str:
        card[0] = int(card[0])

    elif card[0] == 'Jack'.upper():
        card[0] = 10

    elif card[0] == 'Queen'.upper():
        card[0] = 10

    elif card[0] == 'King'.upper():
        card[0] = 10

    elif card[0] == 'Ace'.upper():
        card[0] = 11

    value = card[0]
    suit = card[1]

    return value, suit


# Draws cards from the deck
def draw_cards(count, deckID):
    draw_req = requests.get(f'https://deckofcardsapi.com/api/deck/{deckID}/draw/?count={count}')
    j_draw = json.loads(draw_req.text)
    # debug = json.dumps(j_draw, indent=4)

    code = j_draw['cards'][0]['code']
    card_val = j_draw['cards'][0]['value']
    suit = j_draw['cards'][0]['suit']
    img = j_draw['cards'][0]['image']

    cards = f"{card_val} of {suit}\n"

    return card_val, suit, img, code


# Dealer Cards
def dealer_cards(deckID):
    points = 0
    card1 = draw_cards(1, deckID)
    card2 = draw_cards(1, deckID)

    print(f"-=-=-=-=-=-=-=-=-=-Dealer Cards-=-=-=-=-=-=-=-=-=-=-\n"
          f"Face-Down: Hidden\n"
          f"Face-Up: {list(card2)[0]} of {list(card2)[1]}\n")

    val1, suit1 = d_face_cards(list(card1))
    val2, suit2 = d_face_cards(list(card2))

    points += int(val1) + int(val2)

    return card1, card2, points


# Player Cards
def player_cards(deckID, d_card: list):
    deckID = deckID
    player_score = 0
    card1 = draw_cards(1, deckID)
    card2 = draw_cards(1, deckID)
    print('-=-=-=-=-=-=-=-=-=-Player Cards-=-=-=-=-=-=-=-=-=-=-')
    print(f"Face-Down: {list(card1)[0]} of {list(card1)[1]}\n"
          f"Face-Up: {list(card2)[0]} of {list(card2)[1]}\n")

    val1, suit1 = p_face_cards(list(card1))
    val2, suit2 = p_face_cards(list(card2))

    player_score += int(val1) + int(val2)
    print(f"Player Score: {player_score}")

    while player_score <= 21:
        choice = input("Hit or Stay?: ")
        if choice == 'hit'.lower():
            p_card3 = draw_cards(1, deckID)
            value, suit = p_face_cards(list(p_card3))

            player_score += int(value)
            print(f"+1 Card Dealt: {value} of {suit}\nPlayer Score: {player_score}\n")

        elif choice == 'stay'.lower():
            break

        else:
            print("That is not an option...")

    return card1, card2, player_score


# Get's remaining card count.
def get_remaining(deckID):
    updated = requests.get(f'https://deckofcardsapi.com/api/deck/{deckID}')
    j_remaining = json.loads(updated.text)

    remaining = j_remaining['remaining']

    return remaining


def main(deckID):
    bank = 1000  # Start with $1000.00
    user_input = str()
    welcome = "Welcome to BlackJack!\n To start >> Enter command: 'play'."
    while user_input != 'quit'.lower():
        print(welcome)
        user_input = input("> ")

        if user_input == 'play'.lower():
            while True:
                bet = input("Bet: $")
                if bet.isdigit():
                    if bank <= 0:
                        print("You don't have enough money to play!")
                        break

                    elif int(bet) > bank:
                        print("You don't have enough to bet that much!")
                        break

                    else:
                        remaining_cards = get_remaining(deckID)
                        if remaining_cards <= 0:
                            print("There are no more cards left in the deck!")
                            break

                        bank -= int(bet)

                        d_card1, d_card2, d_count = dealer_cards(DECK_ID)
                        p_card1, p_card2, p_count = player_cards(deckID, list(d_card2)[0])
                        player_score = p_count
                        print(f"Player Final: {player_score}\n")
                        if player_score == 21:
                            print(f"Player hit BLACKJACK!!!")

                        dealer_score = d_count
                        print(f"-=-=-=-=-=-=-=-=-=-Dealer Cards-=-=-=-=-=-=-=-=-=-=-\n"
                              f"Face-Down: {list(d_card1)[0]} of {list(d_card1)[1]}\n"
                              f"Face-Up: {list(d_card2)[0]} of {list(d_card2)[1]}")

                        if dealer_score == 21:
                            print(f"Dealer hit BLACKJACK!!!")

                        print(f"\nDealer Score: {dealer_score}\n")

                        if player_score <= 21:
                            if dealer_score <= 14:
                                d_card3 = draw_cards(1, deckID)
                                dvalue, dsuit = d_face_cards(list(d_card3))

                                dealer_score += int(dvalue)
                                print(f"+1 Card Dealt: {dvalue} of {dsuit}\nDealer Score: {dealer_score}\n")
                            if dealer_score <= 21:
                                if player_score > dealer_score:
                                    bank += int(bet) * 2
                                    print(f"YOU WIN!!!")
                                    print(f"Bank: ${bank}")
                                    break
                                elif player_score == dealer_score:
                                    bank += bet
                                    print(f"Wash...")
                                    print(f"Bank: ${bank}")
                                    break
                                elif player_score < dealer_score:
                                    print(f"Dealer WINS!")
                                    print(f"Bank: ${bank}")
                                    break
                            else:
                                bank += int(bet) * 2
                                print(f"Dealer busted! YOU WIN!!!\n"
                                      f"Bank: ${bank}")
                        else:
                            print(f"You busted! Dealer wins!!!")
                            print(f"Bank: ${bank}")
                            break

                else:
                    print(f"You must enter a bet amount...")


if __name__ == "__main__":
    main(DECK_ID)
