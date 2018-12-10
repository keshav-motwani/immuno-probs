# ImmunoProbs Python package uses simplified manner for calculating the
# generation probability of V(D)J and CDR3 sequences.
# Copyright (C) 2018 Wout van Helvoirt

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


"""Test file for testing immuno_probs.cdr3.anchor_locator file."""


import pandas
import pytest

from immuno_probs.alignment.muscle_aligner import MuscleAligner
from immuno_probs.cdr3.anchor_locator import AnchorLocator


def create_alignment():
    """Create an alignment to use for testing."""
    filename = 'tests/test_data/IGH_mus_musculus/ref_genomes/genomicJs.fasta'
    aligner = MuscleAligner(infile=filename)
    return aligner.get_muscle_alignment()


@pytest.mark.parametrize('gene, motif, expected', [
    ('J', 'TTT', pandas.DataFrame(
        [['IGHJ1*02', 44, 'F', 'TTT']],
        columns=['gene', 'anchor_index', 'function', 'motif'])
    ),
    pytest.param('J', 'TGG', pandas.DataFrame(
        [['IGHJ3*01', 14, 'F', 'TGG'],
         ['IGHJ3*02', 14, 'P', 'TGG'],
         ['IGHJ1*02', 19, 'F', 'TGG'],
         ['IGHJ1*03', 19, 'F', 'TGG'],
         ['IGHJ1*01', 19, 'F', 'TGG']],
        columns=['gene', 'anchor_index', 'function', 'motif'])),
    pytest.param('X', None, None, marks=pytest.mark.xfail)
])
def test_anchor_locator(gene, motif, expected):
    """Test if correct indices of conserved motif regions are returned.

    Parameters
    ----------
    gene : string
        A gene identifier, either V or J, specifying the alignment's origin.
    motif : string
        A custom motif string to use for the search.
    expected : pandas.DataFrame
        The expected output pandas.Dataframe with correct columns and values.

    Raises
    -------
    AssertionError
        If the performed test failed.

    """
    locator = AnchorLocator(alignment=create_alignment(), gene=gene)
    if motif is not None:
        result = locator.get_indices_motifs(motif).head()
    else:
        result = locator.get_indices_motifs().head()
    assert (result == expected).all().all()
