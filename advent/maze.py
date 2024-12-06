
from tqdm.notebook import tqdm
import heapq
from typing import Callable

# Generic
class Node: ...

def solve_maze_no_tqdm(start, is_target, adjacent, h=None):
    # This is more intented for 'small' mazes, and if you need to solve a maze
    # in a for-loop and not get dozens of progress bars
    # There is also a third output: path_possible, because there are usecases where
    # you need to solve multiple mazes to see which are possible (e.g. try different starting points)

    # By default, use Dijkstra
    if h is None:
        h = lambda _: 0

    closed = set([])
    open = {}
    f: list[tuple[int, int, Node]] = [(h(start), 0, start)] # [(g+h, g, n)]
    open_parents: dict[Node, Node|None] = {start: None}
    closed_parents: dict[Node, Node|None] = {}
    path_possible = False

    while f:
        current_f, current_g, current_node = heapq.heappop(f)
        closed.add(current_node)
        closed_parents[current_node] = open_parents[current_node]
        if is_target(current_node):
            path_possible = True
            break

        # Here are our two day-specific functions, edit their signature if neccecary
        for adj, adj_g in adjacent(current_node):
            if adj in closed:
                continue
            new_f, new_g = current_g + adj_g + h(adj), current_g + adj_g
            if adj not in open or open[adj] > new_f:
                heapq.heappush(f, (new_f, new_g, adj))
                open[adj] = new_f
                open_parents[adj] = current_node

    return current_f, closed_parents, path_possible


def solve_maze(
        start: Node,
        is_target: Callable[[Node], bool],
        adjacent: Callable[[Node], list[tuple[Node, int]]],
        h: Callable[[Node], int]|None = None,
        total_nodes: int = 1,
        update_tqdm_every: int = 100):
    # Given start and end nodes, and an adjacent function
    # as well as optional heuristic and total number of nodes,
    # Return shortest path, and for each node in that path, its parent
    # Uses A* with by default, the 0 heuristic. The total nodes is only for the progress bar
    # adjacent: Node -> [(Node, cost)],
    # where Node is basically a 'state', and cost is the cost of moving from one node to another
    # COST MUST BE >= 0 !!!!
    # is_target function is a function that checks if a node is the target
    # If you have a constant target instead, use: lambda x: x == my_target
    # Important: Node must be hashable. So e.g. tuple, not list

    # By default, use Dijkstra
    if h is None:
        h = lambda _: 0

    closed: set[Node] = set([])
    # open and f are related: if (g+h, _, n) in f, then open[n] = g+h
    open = {}
    f: list[tuple[int, int, Node]] = [(h(start), 0, start)] # [(g+h, g, n)]
    open_parents: dict[Node, Node|None] = {start: None}
    closed_parents: dict[Node, Node|None] = {}
    current_f = h(start)

    progress, update_tqdm = 0, 0

    with tqdm(total=total_nodes) as pbar:
        while f:
            current_f, current_g, current_node = heapq.heappop(f)
            closed.add(current_node)
            # Update tqdm progress bar
            progress, update_tqdm = progress + 1, update_tqdm + 1
            if (update_tqdm % update_tqdm_every) == 0: pbar.update(progress)

            closed_parents[current_node] = open_parents[current_node]
            if is_target(current_node):
                print(f"Final path length: {current_f}")
                break

            for adj, adj_g in adjacent(current_node):
                if adj in closed:
                    continue
                new_f, new_g = current_g + adj_g + h(adj), current_g + adj_g
                if adj not in open or open[adj] > new_f:
                    heapq.heappush(f, (new_f, new_g, adj))
                    open[adj] = new_f
                    open_parents[adj] = current_node
    
    return current_f, closed_parents
