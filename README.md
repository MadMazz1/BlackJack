# MazZ's BlackJack Table
This is a Black Jack Card game I re-created out of boredom, upon coming across a deck of cards API.
<br />
<br />
API = "https://deckofcardsapi.com/"

Another way to do this manually:

    for suit in ("Hearts", "Diamonds", "Clubs", "Spades"):
        for val in range(2, 15):
            deck.append((val, suit))

    Then Define face cards with a function similar to below: p_face_cards()


Using the API allowed me to play around with JSON objects, and required much more functionality.


# TODO: 
- #1) Track Player + Dealer Cards [DONE]
- #2) Track Player + Dealer Score [DONE]
- #3) Betting System [DONE]
- #4) Player Hit/Stay functionality [DONE]
- #6) Double-Down
- #7) Keep counts and let player know when deck is "Hot" or "Cold"

