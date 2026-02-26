# (c) Copyright Riverlane 2020-2025.
from collections.abc import Sequence

import numpy as np
from deltakit_core.deprecation import deprecated
from deltakit_explorer.plotting import correlation_matrix
from deltakit_explorer.types._types import QubitCoordinateToDetectorMapping


@deprecated(
    reason="This function has been superseded by explorer plotting utilities.",
    replaced_by="deltakit_explorer.plotting.correlation_matrix",
)
def plot_correlation_matrix(
    matrix: list[list[float]],
    major_minor_mapping: dict[tuple[float, ...], list[int]],
    labels: Sequence[str] = (),
):
    """Plot a given correlation matrix as a heatmap.

    Parameters
    ----------
    matrix : List[List[float]]
        A correlation matrix generated from Pij data.
    major_minor_mapping : Dict[Tuple[int, ...], List[int]]
        The accompanying coordinate mapping for a correlation matrix.
    labels : Sequence[str]
        Optional list of labels to assign to the qubits in-order. If unspecified,
        will use the qubit's coordinates instead.
        By default, ().

    Returns
    -------
    matplotlib.plt
        The plt object containing the drawn heatmap.
    """
    return correlation_matrix(
        matrix=np.asarray(matrix),
        qubit_to_detector_mapping=QubitCoordinateToDetectorMapping(major_minor_mapping),
        labels=labels,
    )
