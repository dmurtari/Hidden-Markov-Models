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
        previous_topic = "."
        #first_run = True
        total_observations = ()

        for line in contents:
            read_line = line.rstrip()
            if read_line == "..":
                print "End of Test Data1"
                break
            words = read_line.split(" ")
            current_topic = words[0]
            words = tuple(words[1:])

            # Keep track of starting topics to generate the start
            # probabilities
            if current_topic not in starts:
                starts[current_topic] = 1
                total_starts += 1
            elif previous_topic == ".":
                starts[current_topic] += 1
                total_starts += 1

            if current_topic not in self.states:
                self.states = self.states + (current_topic,)

            if previous_topic != ".":
                total_transitions += 1
                if previous_topic not in self.transition_probability:
                    self.transition_probability[previous_topic] = {}

                if current_topic not in self.transition_probability[previous_topic]:
                    self.transition_probability[previous_topic][current_topic] = 1
                else:
                    self.transition_probability[previous_topic][current_topic] += 1

            # Generate emission probabilities by counting how often certain
            # word appears in given topic
            for word in words:
                if current_topic not in self.emission_probability:
                    self.emission_probability[current_topic] = {}
                if word not in self.emission_probability[current_topic]:
                    self.emission_probability[current_topic][word] = 1
                else:
                    self.emission_probability[current_topic][word] += 1

            total_moves += 1
            previous_topic = current_topic

        # Fill in start probabilities, fill in transitions that don't exist
        for current_topic in self.states:
            self.start_probability[current_topic] = starts[current_topic]/float(total_starts)

        for key, value in self.transition_probability.iteritems():
            print key, value
            for current_topic in self.states:
                if current_topic not in value:
                    self.transition_probability[key][current_topic] = 1

        print self.states
        print self.start_probability.keys()
        print self.transition_probability.keys()
        print self.emission_probability.keys()



    def run_viterbi(self):
        print "Fin"
        #print self.observations

        #viterbi = Viterbi(self.observations, self.states, self.start_probability, self.transition_probability, self.emission_probability)
        #print viterbi.run_viterbi()
