
from tqdm.notebook import tqdm

def solve_maze_no_tqdm(start, is_target, adjacent, h=None):
    # This is more intented for 'small' mazes, and if you need to solve a maze
    # in a for-loop and not get dozens of progress bars
    # There is also a third output: path_possible, because there are usecases where
    # you need to solve multiple mazes to see which are possible (e.g. try different starting points)

    # By default, use Dijkstra
    if h is None:
        h = lambda _: 0

    closed = set([])
    f = {start: (start, (0, h(start)))} # n: (n, (g, h))
    open_parents, closed_parents = {start: None}, {}
    path_possible = False

    while len(f) > 0:
        current_node, current_f = min(f.values(), key=lambda n: sum(n[1]))
        del f[current_node]
        closed.add(current_node)
        closed_parents[current_node] = open_parents[current_node]
        if is_target(current_node):
            path_possible = True
            break

        # Here are our two day-specific functions, edit their signature if neccecary
        for adj, adj_g in adjacent(current_node):
            if adj in closed:
                continue
            new_f = (current_f[0] + adj_g, h(adj))
            if (adj not in f) or (sum(new_f) < sum(f[adj][1])):
                f[adj] = (adj, new_f)
                open_parents[adj] = current_node
    
    return sum(current_f), closed_parents, path_possible
    

def solve_maze(start, is_target, adjacent, h=None, total_nodes=1):
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

    closed = set([])
    f = {start: (start, (0, h(start)))} # n: (n, (g, h))
    open_parents, closed_parents = {start: None}, {}

    progress=0  # out o

    with tqdm(total=1) as pbar:

        while len(f) > 0:
            current_node, current_f = min(f.values(), key=lambda n: sum(n[1]))
            del f[current_node]
            closed.add(current_node)
            closed_parents[current_node] = open_parents[current_node]
            if is_target(current_node):
                print(f"Final path length: {sum(current_f)}")
                break

            # Here are our two day-specific functions, edit their signature if neccecary
            for adj, adj_g in adjacent(current_node):
                if adj in closed:
                    continue
                new_f = (current_f[0] + adj_g, h(adj))
                if (adj not in f) or (sum(new_f) < sum(f[adj][1])):
                    f[adj] = (adj, new_f)
                    open_parents[adj] = current_node
            
            # Update progress bar
            progress_tmp = len(closed) / total_nodes
            if progress_tmp > progress:
                pbar.update(progress_tmp - progress)
                progress = progress_tmp
    
    return sum(current_f), closed_parents