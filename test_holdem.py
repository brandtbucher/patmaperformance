import pytest

import bm_holdem


def test_holdem() -> None:
    _, results = bm_holdem.holdem(bm_holdem.POSSIBLE_HANDS)
    assert results == {
        "Royal Flush": 4,
        "Straight Flush": 36,
        "Four Of A Kind": 624,
        "Full House": 3_744,
        "Flush": 5_108,
        "Straight": 10_200,
        "Three Of A Kind": 54_912,
        "Two Pair": 123_552,
        "One Pair": 1_098_240,
        "High Card": 1_302_540,
    }
