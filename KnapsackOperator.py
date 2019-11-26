import numpy as np
import sys

class KnapsackOperator:
    def __init__(self, the_list, W):
        self._W = W
        self._cache = {}

        # Two parallel vectors that store the value and weights for items.
        self._values = np.asarray([v for (v, _) in the_list])
        self._weights = np.asarray([w for (_, w) in the_list])

        self._required_qubits = len(the_list)

        self._SCALE_FACTOR = 1

        self.minVal = 0

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

    def _get_value_from_state_string(self, state):
        self._checkCompatibility(state)

        # Converting the state to a hot-encoded vector.
        # Here each binary position in the state represents whether an item is picked.
        # For e.g. if we were represent picking the first and the last item from a list of four items,
        # we would encode it as [1, 0, 0, 1].  The position in the encoding is determined by the position of the item
        # in the initial the_list argument passed in the constructor.
        state_vector = np.asarray([float(s) for s in state]).transpose()

        # Getting the dot product of self._values vector (row vector) and state_vector (column vector). This yields the
        # sum of values for items encoded in the state.
        total_value = self._values.dot(state_vector)

        # Getting the dot product of self.weight vector (row vector) and state_vector (column vector). This yields the
        # sum of weights for items encoded in the state.
        total_weight = self._weights.dot(state_vector)

        if total_weight > self._W:
            total_value = 0

        if -total_value < self.minVal:
            self.minVal = -total_value

        return total_value* self._SCALE_FACTOR


    # The following code is the same as the code in the maxcut example posted in piazza.
    def _get_eigenstate_value(self, state):
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