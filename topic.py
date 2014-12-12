from viterbi import Viterbi
#0.863180827887

class Topic():

    def __init__(self, file):
        self.states = ()
        self.observations = ()
        self.solutions = ()
        self.start_probability = {}
        self.transition_probability = {}
        self.emission_probability = {}
        self.parse(file)
        self.run_viterbi()

    def parse(self,file):
        with open(file) as topics_data:
            contents = topics_data.readlines()

        starts = {}
        transitions_from = {}
        total_starts = 0
        total_transitions = 6
        total_moves = 0
        previous_topic = "."

        for line in contents:
            read_line = line.rstrip()
            if read_line == "..":
                print "End of Training Data"
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
                if previous_topic not in transitions_from:
                    transitions_from[previous_topic] = 1
                else:
                    transitions_from[previous_topic] += 1

                if previous_topic not in self.transition_probability:
                    self.transition_probability[previous_topic] = {}

                if current_topic not in self.transition_probability[previous_topic]:
                    self.transition_probability[previous_topic][current_topic] = 1
                else:
                    self.transition_probability[previous_topic][current_topic] += 1

            # Generate emission probabilities by counting how often certain
            # word appears in given topic
            for word in words:
                total_transitions += 1
                if current_topic not in transitions_from:
                    transitions_from[current_topic] = 1
                else:
                    transitions_from[current_topic] += 1

                if current_topic not in self.transition_probability:
                    self.transition_probability[current_topic] = {}

                if current_topic not in self.transition_probability[current_topic]:
                    self.transition_probability[current_topic][current_topic] = 1
                else:
                    self.transition_probability[current_topic][current_topic] += 1



                if current_topic not in self.emission_probability:
                    self.emission_probability[current_topic] = {}
                if word not in self.emission_probability[current_topic]:
                    self.emission_probability[current_topic][word] = 1
                else:
                    self.emission_probability[current_topic][word] += 1

            previous_topic = current_topic

        # Fill in start probabilities, fill in transitions that don't exist
        for current_topic in self.states:
            self.start_probability[current_topic] = starts[current_topic]/float(total_starts)

        for key, value in self.transition_probability.iteritems():
            for current_topic in self.states:
                if current_topic not in value:
                    self.transition_probability[key][current_topic] = 1

        for start, transition in self.transition_probability.iteritems():
            for end, count in transition.iteritems():
                self.transition_probability[start][end] = count/float(transitions_from[start] + 6)

        for current_topic, observation in self.emission_probability.iteritems():
            #print observation.keys()
            for topic in self.states:
                for key in observation.keys():
                    if key not in self.emission_probability[topic]:
                        self.emission_probability[topic][key] = 1

        # Fill in emission probabilities
        for current_topic, observation in self.emission_probability.iteritems():
            total_count = 0
            for word, count in observation.iteritems():
                total_count += count
            for word, count in observation.iteritems():
                word_count = self.emission_probability[current_topic][word]
                self.emission_probability[current_topic][word] = word_count/float(total_count)
        #print self.emission_probability["baseball"]["civil"]
        #self.print_conditions()
        # print self.states
        self.print_conditions()

        isTesting = False;
        ttl = 500

        for line in contents:
            read_line = line.rstrip()
            if read_line == "..":
                print "BeginTest"
                isTesting = True
                continue
            if isTesting:
                ttl = ttl-1
                if( ttl<=0):
                  break
                words = read_line.split(" ")
                #current_topic = words[0]
                self.solutions = self.solutions+ (words[0],)*len(words[1:])
                self.observations = self.observations+ tuple(words[1:])


    def print_conditions(self):
        total = 0
        string = ""
        print "Rounded start probability:"
        for (key, val) in self.start_probability.iteritems():
            tmp = "%s: %.9f, " % (key, self.start_probability[key])
            string = string + tmp
            total += self.start_probability[key]
        print string

        print "\nA few rounded transition probability:"
        i = 0
        for key, val in self.transition_probability.iteritems():
            string = ""
            print key
            if i > 1:
                break
            for (child_key, child_val) in val.iteritems():
                tmp = "%s: %.9f, " % (child_key, child_val)
                string += tmp
            print string
            i += 1

        print "\nA few rounded emission probability:"
        i = 0
        for key, val in self.emission_probability.iteritems():
            string = ""
            print key
            if i > 1:
                break
            for (child_key, child_val) in val.iteritems():
                tmp = "%s: %.9f, " % (child_key, child_val)
                string += tmp
            print string
            i += 1

    def run_viterbi(self):
        #print "Fin"
        #print self.observations

        viterbi = Viterbi(self.observations, self.states, self.start_probability, self.transition_probability, self.emission_probability)
        (junk, deduced_path)= viterbi.run_viterbi()
        self.checkSolutions(deduced_path)

    def checkSolutions(self,deduced_path):
        ##print len(deduced_path)
        #print len(self.solutions)
        num_correct=0
        num_wrong =0
        for num in range(0,len(deduced_path)):
            #print deduced_path[num], self.solutions[num]
            if deduced_path[num] == self.solutions[num]:
              num_correct+=1
            else:
              num_wrong+=1
        print num_correct/(float)(num_correct+num_wrong)
