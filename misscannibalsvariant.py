'''
Name:    Hien Tran
CWID:    830889556
Class:   CPSC 481-02 17420
'''
from search import Problem, depth_first_graph_search, breadth_first_graph_search

class MissCannibalsVariant(Problem):
    """
    Missionaries & Cannibals boat capacity = 3.
    Actions: 'M', 'C', 'MM', 'MC', 'CC', 'MMM', 'MMC', 'MCC', 'CCC'

    State: (m_left, c_left, boat_on_left: bool)
    """

    POSSIBLE_ACTIONS = (
        "M", "C",
        "MM", "MC", "CC",
        "MMM", "MMC", "MCC", "CCC"
    )

    def __init__(self, N1=0, N2=0, goal=(0, 0, False)):
        # initial missionaries/cannibals on left
        initial = (N1, N2, True)  # True == left, False == right
        self.N1 = N1  # total missionaries
        self.N2 = N2  # total cannibals
        super().__init__(initial, goal)

    def actions(self, state):
        m_left, c_left, boat_left = state
        m_right = self.N1 - m_left
        c_right = self.N2 - c_left

        valid = []
        for a in self.POSSIBLE_ACTIONS:
            num_m = a.count('M')
            num_c = a.count('C')

            if boat_left:  # boat on left
                if num_m > m_left or num_c > c_left:
                    continue
                new_m = m_left - num_m
                new_c = c_left - num_c
            else:  # boat on right
                if num_m > m_right or num_c > c_right:
                    continue
                new_m = m_left + num_m
                new_c = c_left + num_c

            if self._valid_state(new_m, new_c):
                valid.append(a)

        return valid

    def _valid_state(self, m_left, c_left):
        if not (0 <= m_left <= self.N1 and 0 <= c_left <= self.N2):
            return False

        m_right = self.N1 - m_left
        c_right = self.N2 - c_left

        if m_left > 0 and c_left > m_left:
            return False
        if m_right > 0 and c_right > m_right:
            return False

        return True

    def result(self, state, action):
        m_left, c_left, boat_left = state
        num_m = action.count('M')
        num_c = action.count('C')

        if boat_left:  # boat on left, move right
            new_m = m_left - num_m
            new_c = c_left - num_c
            return (new_m, new_c, False)
        else:  # boat on right, move left
            new_m = m_left + num_m
            new_c = c_left + num_c
            return (new_m, new_c, True)

if __name__ == '__main__':
    mc = MissCannibalsVariant(4, 4)
    print("\nDFS:")
    print(depth_first_graph_search(mc).solution())
    print("\nBFS:")
    print(breadth_first_graph_search(mc).solution())
