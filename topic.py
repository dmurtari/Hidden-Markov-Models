from viterbi import Viterbi

class Topic():

    def __init__(self, file):
        self.states = ()
        self.observations = ()
        self.start_probability = {}
        self.transition_probability = {}
        self.emission_probability = {}
        self.parse(file)
        self.run_viterbi()

    def parse(self,file):
        with open(file) as topics_data:
            contents = topics_data.readlines()

        starts = {}
        total_starts = 0
        total_transitions = 6
        total_moves = 0
        #previous_coordinate = "."
        #first_run = True
        total_observations = ()

        for line in contents:
            read_line = line.rstrip()
            if read_line == "..":
                print "End of Test Data1"
                break
            words = read_line.split(" ")
            curTopic = words[0]
            words = tuple(words[1:])

            if curTopic not in self.states:
                self.states = self.states + (curTopic,)

        print self.states



    def run_viterbi(self):
        print "Fin"
        #print self.observations

        #viterbi = Viterbi(self.observations, self.states, self.start_probability, self.transition_probability, self.emission_probability)
        #print viterbi.run_viterbi()
