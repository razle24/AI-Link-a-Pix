import util


class StateNode:
    """
    Fix problem with util.PriorityQueue which tried (and failed) to use '<' operator on a tuple.
    This class is basically the same tuple with overloaded '<' operator.
    """

    def __init__(self, state, actions):
        self.state = state
        self.actions = actions

    def __lt__(self, other):
        return self.state.score(0) < other.score(0)

    def __iter__(self):
        yield self.state
        yield self.actions


def a_star_search(problem, heuristic):
    """
    Search the node that has the lowest combined cost and heuristic first.
    """
    i = 0
    explored = set()
    queue = util.PriorityQueue()

    # Contains 'state', 'total cost from start to state' and 'list of actions to the state'
    queue.push(StateNode(problem.get_start_state(), []), 0)

    while not queue.isEmpty():
        current, actions_to_current = queue.pop()

        if problem.is_goal_state(current):
            return actions_to_current

        for child_state, action, step_cost in problem.get_successors(current):
            if child_state not in explored:
                total_cost = step_cost + heuristic(child_state, problem)
                if total_cost != math.inf:
                    queue.push(StateNode(child_state, actions_to_current + [action]), total_cost)

        explored.add(current)

    return None
