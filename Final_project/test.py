import pytest

from final_project import won
from final_project import (
    CROSS as X, ZERO as O, FREE_SPACE as _
)


@pytest.mark.parametrize(
    "state,expected",
    [
        pytest.param(
            [
                [_, _, _],
                [_, _, _],
                [_, _, _]
            ],
            False,
        ),
        pytest.param(
            [
                [X, X, X],
                [_, _, _],
                [O, O, _]
            ],
            True,
        ),
        pytest.param(
            [
                [X, X, _],
                [O, X, X],
                [O, O, O]
            ],
            True,
        ),
        pytest.param(
            [
                [X, X, O],
                [O, O, X],
                [O, X, _]
            ],
            True,
        ),
        pytest.param(
            [
                [X, O, O],
                [O, X, X],
                [O, X, X]
            ],
            True,
        ),
        pytest.param(
            [
                [X, O, X],
                [O, X, X],
                [O, X, O]
            ],
            False,
        ),
        pytest.param(
            [
                [X, O, O],
                [X, X, _],
                [O, _, _]
            ],
            False,
        ),
        pytest.param(
            [
                [O, _, _],
                [O, X, X],
                [O, X, X]
            ],
            True,
        ),
        pytest.param(
            [
                [X, O, O],
                [X, O, _],
                [O, X, X]
            ],
            True,
        ),
        pytest.param(
            [
                [X, O, O],
                [_, O, X],
                [X, X, X]
            ],
            True,
        ),
    ],
)
def test_won_is_correct(state: list[list[str]], expected: bool):
    result = won(state)
    assert result == expected
