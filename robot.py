from viterbi import Viterbi

class Robot():

    def __init__(self, file):
        self.states = ()
        self.start_probability = {}
        self.transition_probability = {}
        self.emission_probability = {}
        self.contents = []
        self.sum = 0
        self.index = 0
        self.iteration = 0
        self.parse(file)

    def parse(self, file):
        with open(file) as robot_data:
            self.contents = robot_data.readlines()

        starts = {}
        transitions_from = {}
        total_starts = 0
        total_transitions = 12
        total_moves = 0
        previous_coordinate = "."

        for index, line in enumerate(self.contents):
            read_line = line.rstrip()
            if read_line == ".":
                previous_coordinate = read_line
                continue
            if read_line == "..":
                print "End of Test Data"
                self.index = index
                break

            coordinate, color = read_line.split(" ")

            # Generate the list of available coordinates and observable colors
            # fom the given data
            if coordinate not in self.states:
                self.states = self.states + (coordinate,)
            # Keep track of start coordinates to generate the start
            # probabilities
            if coordinate not in starts and previous_coordinate == ".":
                starts[coordinate] = 1
                total_starts += 1
            elif previous_coordinate == ".":
                starts[coordinate] += 1
                total_starts += 1

            # Generate transition probabilities by seeing how often we go from
            # previous coordinate to current coordinate
            if previous_coordinate != ".":
                total_transitions += 1
                if previous_coordinate not in transitions_from:
                    transitions_from[previous_coordinate] = 1
                else:
                    transitions_from[previous_coordinate] += 1

                if previous_coordinate not in self.transition_probability:
                    self.transition_probability[previous_coordinate] = {}

                if coordinate not in self.transition_probability[previous_coordinate]:
                    self.transition_probability[previous_coordinate][coordinate] = 1
                else:
                    self.transition_probability[previous_coordinate][coordinate] += 1

            # Generate emission probabilities by counting how often certain
            # colors are observed on a given coordinate
            if coordinate not in self.emission_probability:
                self.emission_probability[coordinate] = {}
            if color not in self.emission_probability[coordinate]:
                self.emission_probability[coordinate][color] = 1
            else:
                self.emission_probability[coordinate][color] += 1

            total_moves += 1
            previous_coordinate = coordinate

        # Fill in start probabilities, fill in transitions that don't exist
        for coordinate in self.states:
            self.start_probability[coordinate] = starts[coordinate]/float(total_starts)

        for key, value in self.transition_probability.iteritems():
            for coordinate in self.states:
                if coordinate not in value:
                    self.transition_probability[key][coordinate] = 1

        # Fill in transition probabilities
        for start, transition in self.transition_probability.iteritems():
            for end, count in transition.iteritems():
                self.transition_probability[start][end] = count/float(transitions_from[start] + 12)

        # Fill in emission probabilities
        for coordinate, observation in self.emission_probability.iteritems():
            total_count = 0
            for color, count in observation.iteritems():
                total_count += count
            for color, count in observation.iteritems():
                color_count = self.emission_probability[coordinate][color]
                self.emission_probability[coordinate][color] = color_count/float(total_count)

        self.print_conditions()

    def print_conditions(self):
        total = 0
        string = ""
        print "Rounded start probability:"
        for (key, val) in self.start_probability.iteritems():
            tmp = "%s: %.4f, " % (key, self.start_probability[key])
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
                tmp = "%s: %.4f, " % (child_key, child_val)
                string += tmp
            print string
            i += 1

        print "\nA few rounded emission probability:"
        i = 0
        for key, val in self.emission_probability.iteritems():
            string = ""
            print key
            if i > 12:
                break
            for (child_key, child_val) in val.iteritems():
                tmp = "%s: %.4f, " % (child_key, child_val)
                string += tmp
            print string
            i += 1

    def run_viterbi(self):
        contents = self.contents[self.index + 1:]

        observations = ()
        correct_path = []

        for line in contents:
            read_line = line.rstrip()
            if read_line == ".":
                viterbi = Viterbi(observations, self.states, \
                                  self.start_probability, \
                                  self.transition_probability, \
                                  self.emission_probability)
                deduced_path = viterbi.run_viterbi()
                junk, guessed_path = deduced_path
                self.iteration += 1
                self.check_correctness(guessed_path, correct_path)
                observations = ()
                correct_path = []
                continue

            coordinate, color = read_line.split(" ")
            observations = observations + (color,)
            correct_path.append(coordinate)
                        
    def check_correctness(self, guessed_path, correct_path):
        total = 0
        incorrect = 0

        for i in xrange(200):
            total += 1
            if guessed_path[i] != correct_path[i]:
                incorrect += 1

        percent_correct = (total - incorrect)/float(total) * 100
        if self.iteration < 10:
            print "The guessed path is: ", guessed_path
        print "For test", self.iteration, "the percent correct is", percent_correct
        self.sum += percent_correct

    def print_average(self):
        print "Average percent correct:", self.sum/float(200)