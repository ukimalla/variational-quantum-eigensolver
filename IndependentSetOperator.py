import numpy as np
import sys

class IndependentSetOperator:
    def __init__(self, edge_list):
        # Inserting all the vertices in set _V
        V_set = set()
        for (x, y) in edge_list:
            V_set .add(x)
            V_set.add(y)

        self._num_vertex = len(V_set)
        self._cache = {}

        # Assigning each vertex a number. This makes it easier to represent it in hot-encoded vectors.
        self._V_num = {x : i for i, x in enumerate(V_set) }

        self._required_qubits = len(self._V_num)

        self.minVal = 0


        # Creating a dictionary that maps each vertex to a hot-encoded vector that represents all of the edges of
        # the vector. For e.g., in a graph G = {[ (v1, v2), (v1, v3) ], [v1, v2, v3]},
        # where self._V_num[v1] = 1, self._V_num[v2] = 2, and self._V_num[v3] = 3,
        # self._G = { 0 : [0, 1, 1],
        #             1 : [1, 0, 0]
        #             3 : [1, 0, 0]}.
        self._G = {}
        for (x, y) in edge_list:
            # Getting encoding position for each vector in the edge
            x_pos = self._V_num[x]
            y_pos = self._V_num[y]

            # Initializing non-initialized edge vector keys.
            if self._G.get(x_pos) is None:
                self._G[x_pos] = np.zeros(self._num_vertex)
            if self._G.get(y_pos) is None:
                self._G[y_pos] = np.zeros(self._num_vertex)

            # Making the corresponding positions in edge vectors "hot"
            self._G[x_pos][y_pos] = 1
            self._G[y_pos][x_pos] = 1

            self._SCALING_FACTOR = 1


    def _get_value_from_state_string(self, state):
        # Converting the state to a hot-encoded vector:
        # Here each binary position in the state represents whether the vector represented by that position is picked.
        # For e.g. if we were to encode picking the first and the second vertex from a list of four vertices,
        # we would encode it as [1, 1, 0, 0]. The position in the encoding for all vertices are stored self._V_num and
        # is calculated in the constructor.
        state_vector = np.asarray([float(s) for s in state]).transpose()

        has_edges = 0 # Variable to keep track of whether there are edges in the set represented in the state
        num_vertex = 0 # Number of vertex in the state set
        for i, isHot in enumerate(state_vector):
            # dot product of state and hot-encoded edge vector of the i-th edge
            if isHot == 1: # If the vertex is "hot" in the state
                has_edges += state_vector.dot(self._G[i].transpose()) # Adds a value greater than one when an edge exists.
                num_vertex += 1

        if has_edges: # If there is an edge between two vertex in the state set
            num_vertex = 0

        if -num_vertex < self.minVal:
            self.minVal = -num_vertex



        return num_vertex * self._SCALING_FACTOR

    def _checkCompatibility(self, state):
        # Number of used to encode the 'state'
        qubitsInState = len(state)

        # Bool to check whether the number of qubits in the state is compatible with the problem
        isCompitable = (qubitsInState == self._required_qubits)

        if not isCompitable:
            print("[ERROR] Qubits length mismatch:\nThe problem requires " + str(self._required_qubits) +
                  " qubits, but the input state encoding has " + str(qubitsInState) +
                  " qubits. Please use the exact number of qubits required by the problem.")
            sys.exit()


    # The following code is the same as the code in the maxcut example posted in piazza.
    def _get_eigenstate_value(self, state):
        self._checkCompatibility(state)

        cached_value = self._cache.get(state)
        if cached_value is None:
            value = self._get_value_from_state_string(state)
            self._cache[state] = value
            return value
        else:
            return cached_value

    def get_expectation_value(self, shot_dictionary):
        keys = shot_dictionary.keys()
        total_counts = sum([shot_dictionary.get(key) for key in keys])
        probs = {}
        for key in keys:
            probs[key] = shot_dictionary.get(key) / total_counts

        expectation_value = 0
        for key in keys:
            associated_value = self._get_eigenstate_value(key)
            expectation_value += probs.get(key) * associated_value
        return -expectation_value










