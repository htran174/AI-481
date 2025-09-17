'''
Name:    Hien Tran
CWID:    830889556
Class:   CPSC 481-02 17420
'''
from search import *

class MissCannibalsVariant(Problem):
    """
    Missionaries & Cannibals variant with boat capacity = 3.
    State: (m_left, c_left, boat_on_left: bool)
    Actions: 'M', 'C', 'MM', 'MC', 'CC', 'MMM', 'MMC', 'MCC', 'CCC'
    """

    # All boat-load patterns of size 1..3 (capacity = 3)
    POSSIBLE_ACTIONS = (
        "M", "C",
        "MM", "MC", "CC",
        "MMM", "MMC", "MCC", "CCC"
    )

    def __init__(self, N1=4, N2=4, goal=(0, 0, False)):
        """ Define goal state and initialize a problem """
        initial = (N1, N2, True)  # all on left bank; boat on left
        self.N1 = N1  # total missionaries
        self.N2 = N2  # total cannibals
        super().__init__(initial, goal)

    # Default Problem.goal_test is fine (tuple equality), so no override needed.

    def _valid_state(self, m_left, c_left):
        """
        Check bounds and safety: missionaries are never outnumbered
        on either bank unless there are zero missionaries there.
        """
        # Bounds
        if not (0 <= m_left <= self.N1 and 0 <= c_left <= self.N2):
            return False

        m_right = self.N1 - m_left
        c_right = self.N2 - c_left

        # Safety on left bank
        if m_left > 0 and c_left > m_left:
            return False
        # Safety on right bank
        if m_right > 0 and c_right > m_right:
            return False

        return True

    def result(self, state, action):
        """
        Return the successor state after taking `action` from `state`.
        Assumes action was produced by actions(state).
        """
        m_left, c_left, boat_left = state
        dm = action.count('M')
        dc = action.count('C')

        if boat_left:
            # move from left to right
            return (m_left - dm, c_left - dc, False)
        else:
            # move from right to left
            return (m_left + dm, c_left + dc, True)

    def actions(self, state):
        """
        Return all valid actions from `state`.
        An action is valid if:
         - the departing bank has enough M/C to load the boat,
         - the resulting state satisfies safety/bounds constraints.
        """
        m_left, c_left, boat_left = state
        m_right = self.N1 - m_left
        c_right = self.N2 - c_left

        valid = []
        for a in self.POSSIBLE_ACTIONS:
            dm = a.count('M')
            dc = a.count('C')

            # Check availability on the *departing* bank
            if boat_left:
                if dm > m_left or dc > c_left:
                    continue
                nm, nc = m_left - dm, c_left - dc
            else:
                if dm > m_right or dc > c_right:
                    continue
                nm, nc = m_left + dm, c_left + dc

            # Ensure resulting state is safe/within bounds
            if self._valid_state(nm, nc):
                valid.append(a)

            # Note: no need to encode direction; it's implied by boat side.
        return valid


if __name__ == '__main__':
    mc = MissCannibalsVariant(4, 4)
    # Example quick check (depends on N1/N2 and state):
    # print(mc.actions((3, 3, True)))  # e.g., ['MC', 'MMM']

    path = depth_first_graph_search(mc).solution()
    print("\nDFS:")
    print(path)
    path = breadth_first_graph_search(mc).solution()
    print("\nBFS:")
    print(path)
