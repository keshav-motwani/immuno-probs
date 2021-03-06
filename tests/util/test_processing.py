# Create IGoR models and calculate the generation probability of V(D)J and
# CDR3 sequences. Copyright (C) 2019 Wout van Helvoirt

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


"""Test file for testing immuno_probs.util.processing file."""


import pytest

from immuno_probs.util.processing import multiprocess_array


def sum_integers_plus_value(args):
    """Sums list of integers and add given integer to the sum."""
    ary, kwargs = args
    return sum(ary) + kwargs['plus']


@pytest.mark.parametrize(
    'ary, func, num_workers, plus, expected',
    [
        (
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
            sum_integers_plus_value,
            1,
            10,
            [55]
        ),
        (
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
            sum_integers_plus_value,
            2,
            5,
            [15, 40]
        ),
        (
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
            sum_integers_plus_value,
            4,
            -4,
            [-1, 8, 9, 13]
        )
    ]
)
def test_multiprocess_array(ary, func, num_workers, plus, expected):
    """Test if fasta file can be aligned by MUSCLE commandline tool.

    Parameters
    ----------
    ary : list
        List 'like' object to be split for multiple workers.
    func : Object
        A function object that the workers should apply.
    num_workers : int
        The number of workers/threads to spawn.
    **kwargs
        The remaining arguments to be given to the input function.
    expected : numpy.ndarray
        The expected output numpy.ndarray or list with values.

    Raises
    -------
    AssertionError
        If the performed test failed.

    """
    result = multiprocess_array(ary=ary, func=func, num_workers=num_workers,
                                plus=plus)
    assert result == expected
