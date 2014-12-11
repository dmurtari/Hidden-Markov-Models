class Viterbi:
    """
    Viterbi algorithm from: https://en.wikipedia.org/wiki/Viterbi_algorithm
    """

    def __init__(self, observations, states, start, transition, emission):
        self.observations = observations
        self.states = states
        self.start = start
        self.transition = transition
        self.emission = emission
        # self.run_viterbi()

    def run_viterbi(self):
        V = [{}]
        path = {}

        # Initialize base cases (t == 0)
        for y in self.states:
            V[0][y] = self.start[y] * self.emission[y][self.observations[0]]
            path[y] = [y]

        # Run Viterbi for t > 0
        for t in range(1, len(self.observations)):
            V.append({})
            newpath = {}

            for y in self.states:
                print y
                print self.emission[y][self.observations[t]]
                (prob, state) = max((V[t-1][y0] * self.transition[y0][y] * self.emission[y][self.observations[t]], y0) for y0 in self.states)
                V[t][y] = prob
                newpath[y] = path[state] + [y]

            # Don't need to remember the old paths
            path = newpath
        n = 0           # if only one element is observed max is sought in the initialization values
        if len(self.observations) != 1:
            n = t
        self.print_dptable(V)
        (prob, state) = max((V[n][y], y) for y in self.states)
        return (prob, path[state])

    # Don't study this, it just prints a table of the steps.
    def print_dptable(self, V):
        s = "    " + " ".join(("%7d" % i) for i in range(len(V))) + "\n"
        for y in V[0]:
            s += "%.5s: " % y
            s += " ".join("%.7s" % ("%f" % v[y]) for v in V)
            s += "\n"
