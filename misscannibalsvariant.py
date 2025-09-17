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

    # All possible action
    POSSIBLE_ACTIONS = (
        "M", "C",
        "MM", "MC", "CC",
        "MMM", "MMC", "MCC", "CCC"
    )

    def __init__(self, Missionary=0, Canibal=0, goal=(0, 0, False)):
        #initalz M/C
        
        initial = (Missionary, Canibal, True)  # True == left, False == right
        self.Missionary = Missionary  # total missionaries
        self.Canibal = Canibal  # total cannibals
        super().__init__(initial, goal) 

    def actions(self, state):
        #return all valid action

        m_left, c_left, boat_left = state
        m_right = self.Missionary - m_left
        c_right = self.Canibal - c_left

        valid = []
        for a in self.POSSIBLE_ACTIONS:
            num_m = a.count('M') #how many M are invold in the action
            num_c = a.count('C') #how many C are invold in the action

            # Check availability on the *departing* bank
            if boat_left: #boat on left (true)
                if num_m > m_left or num_c > c_left:
                    continue
                new_m = m_left - num_m
                new_c = c_left - num_c

            else: #boat on right (false)
                if num_m > m_right or num_c > c_right:
                    continue
                new_m =  m_left + num_m
                new_c = c_left + num_c

            # Ensure resulting state is safe/within bounds
            if self._valid_state(new_m, new_c):
                valid.append(a)

        return valid
    
    def _valid_state(self, m_left, c_left):
        #Check bounds. 
        #M are never outnumbered on either bank unless zero M.
        
        #Bounds
        if not (0 <= m_left <= self.Missionary and 0 <= c_left <= self.Canibal):
            return False

        m_right = self.Missionary - m_left
        c_right = self.Canibal - c_left

        #Check safety on left bank
        if m_left > 0 and c_left > m_left:
            return False
        
        #Check safety on right bank
        if m_right > 0 and c_right > m_right:
            return False

        return True

    def result(self, state, action):
        #Return the successor state after taking action from prev state
        
        m_left, c_left, boat_left = state
        num_m = action.count('M') #how many M are invold in the action
        num_c = action.count('C') #how many C are invold in the action

        if boat_left: #boat on left (true) move it right(false)
            new_m = m_left - num_m
            new_c = c_left - num_c
            return (new_m, new_c, False)
        
        else: #boat on right (false) move it left(true)
            new_m = m_left + num_m
            new_c = c_left + num_c
            return (new_m, new_c, True)

if __name__ == '__main__':
    mc = MissCannibalsVariant(4, 4)
    # Example quick check (depends on N1/N2 and state):
    #print(mc.actions((3, 3, True)))  # e.g., ['MC', 'MMM']

    path = depth_first_graph_search(mc).solution()
    print("\nDFS:")
    print(path)
    path = breadth_first_graph_search(mc).solution()
    print("\nBFS:")
    print(path)
