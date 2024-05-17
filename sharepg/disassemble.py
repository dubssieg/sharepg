from gfagraphs import Graph
from BubbleGun.Graph import Graph as BubbleGraph
from BubbleGun.find_bubbles import find_bubbles
from tharospytools.data_structures import Interval, IntPair


def extract_bubbles(
    graph: str,
    gfa_graph: Graph,
    node_result: dict[str, bool],
    reference: str,
) -> list[tuple]:
    """_summary_

    Parameters
    ----------
    graph : str
        _description_
    node_result : dict[str, bool]
        _description_
    """
    bubble_results: list[tuple] = list()
    # We compute bubbles in the graph thanks to BubbleGun
    find_bubbles(bg_graph := BubbleGraph(graph))
    # We iterate on the bubbles
    for i, val in enumerate(bg_graph.bubbles.values()):
        if any(included := [node_result[node_name] for node_name in val.list_bubble()]):
            interval: Interval = Interval([IntPair(x, y) for node_name in val.list_bubble(
            ) if reference in gfa_graph.segments[node_name]['PO'] for x, y, _ in gfa_graph.segments[node_name]['PO'][reference]])
            bubble_results.append(
                (
                    str(i),
                    ','.join(val.list_bubble()),
                    ','.join([
                        str(int(node_value))
                        for node_value in included
                    ]),
                    ','.join([str(intr) for intr in interval.intervals]),
                )
            )
    return bubble_results


def disassemble_graph(
    gfa_graph: Graph,
    path_a: set[str],
    path_b: set[str],
    reference: str,
    threshold: float = 1.,
) -> dict[str, bool]:
    """Iterates over all the nodes of the graph, and compares the paths traversing each of them.
    Returns a dict containing every node of the graph associated to a boolean exploring a criterion
    If the node has almost all paths of A (modulo threshold) and almost any of the paths of B (modulo 1-threshold).
    A threshold of 1 means that every path of A must go through the node and no path of B should,
    whereas a threshold of 0 menas the opposite.

    Parameters
    ----------
    gfa_graph : str
        Graph object from the gfagraphs library
    path_a : set[str]
        a set containing the different paths we are looking for
    path_b : set[str]
        a set containig the different paths we want to avoid
    reference : str
        a path name (must be in A or B)
    threshold : float, optional
        a float in between 0 and 1, by default 1.
    """
    # Confinig threshold between boundaries
    if threshold > 1.:
        threshold: float = 1.
    elif threshold < 0.:
        threshold: float = 0.
    # Return structure
    node_result: dict[str, bool] = dict()
    # Main loop over all segments of the graph
    for segment_name, segment_data in gfa_graph.segments.items():
        paths_of_node: set[str] = set(list(segment_data['PO'].keys()))
        common_paths_a: int = len(path_a.intersection(paths_of_node))
        common_paths_b: int = len(path_b.intersection(paths_of_node))
        node_result[segment_name] = common_paths_a >= len(
            path_a) * threshold and common_paths_b <= len(path_b) * (1-threshold)
    return node_result


def get_intervals(
    gfa_graph: Graph,
    node_result: dict[str, bool],
    paths_a: list[str],
) -> dict[str, Interval]:
    """From the results of an iteration over all nodes, extracts the intervals meeting the criterion
    Intervals are reported as IntPairs, and are merged when they are chained. 

    Parameters
    ----------
    gfa_graph : Graph
        Graph object from the gfagraphs library
    node_result : dict[str, bool]
        a dict mapping, for each node of the graph, to a boolean
    paths_a : list[str]
        the paths we want to extract coordinates

    Returns
    -------
    dict[str, Interval]
        Interval object for each path of paths_a
    """
    interval_result: dict[str, list[IntPair]] = {
        path_name: list() for path_name in paths_a}
    # Looping over selected nodes:
    for node_name, selected in node_result.items():
        if selected:
            for path_name in paths_a:
                if path_name in gfa_graph.segments[node_name]['PO']:
                    list_of_coordinates: list[
                        tuple[int, int, str]
                    ] = gfa_graph.segments[node_name]['PO'][path_name]
                    for coordinate in list_of_coordinates:
                        interval_result[path_name].append(
                            IntPair(coordinate[0], coordinate[1]))
    interval_result: dict[str, list[IntPair]] = {path_name: Interval(
        list_points) for path_name, list_points in interval_result.items()}
    return interval_result
