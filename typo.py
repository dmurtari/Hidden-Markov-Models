import string
from viterbi import Viterbi

class Typo():

    def __init__(self, file):
        self.states = ()
        self.observations = ()
        self.start_probability = {}
        self.transition_probability = {}
        self.emission_probability = {}
        self.contents = []
        self.index = 0
        self.iteration = 0
        self.parse(file)

    def parse(self, file):
        with open(file) as typo_data:
            self.contents = typo_data.readlines()


        start_letters = [0]*26
        start_counter = 0
        transitions = {}
        previous_letter = ""

        for i in range(26):
            self.states = self.states + (chr(ord('a') + i),)

        for i in range(26):
            self.transition_probability[chr(ord('a') + i)] = {"counter" : 0}
            for j in range(26):
                self.transition_probability[chr(ord('a') + i)][chr(ord('a') + j)] = 0

        for i in range(26):
            self.emission_probability[chr(ord('a') + i)] = {"counter" : 0}
            for j in range(26):
                self.emission_probability[chr(ord('a') + i)][chr(ord('a') + j)] = 0


        first_line = True
        for (i, line) in enumerate(self.contents):
            read_line = line.rstrip()
            if read_line == "_ _":
                previous_line = read_line
                first_line = True
                continue
            if read_line == "..":
                print "End of Test Data"
                self.index = i
                break

            letters = read_line.split(" ")
            if first_line:
                start_letters[string.lowercase.index(letters[0])] += 1
                start_counter += 1
                first_line = False
                previous_letter = letters[0]

            else:
                if letters[0] not in self.transition_probability[previous_letter]:
                    self.transition_probability[previous_letter][letters[0]] = 1
                    self.transition_probability[previous_letter]["counter"] += 1
                else:
                    self.transition_probability[previous_letter][letters[0]] += 1
                    self.transition_probability[previous_letter]["counter"] += 1
                previous_letter = letters[0]

            self.emission_probability[letters[0]][letters[1]] += 1
            self.emission_probability[letters[0]]["counter"] += 1

        for i, times in enumerate(start_letters):
            self.start_probability[chr(ord('a') + i)] = (times + 1)/float(start_counter + 26)

        for key in self.transition_probability:
            for child_key in self.transition_probability[key]:
                if child_key != "counter":
                    count = self.transition_probability[key][child_key] + 1
                    self.transition_probability[key][child_key] = count / float(self.transition_probability[key]["counter"] + 26)
            self.transition_probability[key].pop("counter", None)

        for key in self.emission_probability:
            for child_key in self.emission_probability[key]:
                if child_key != "counter":
                    count = self.emission_probability[key][child_key] + 1
                    self.emission_probability[key][child_key] = count / float(self.emission_probability[key]["counter"] + 26)
            self.emission_probability[key].pop("counter", None)


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
            if i > 1:
                break
            for (child_key, child_val) in val.iteritems():
                tmp = "%s: %.4f, " % (child_key, child_val)
                string += tmp
            print string
            i += 1


    def get_observations(self):
        self.print_conditions()

        contents = self.contents[self.index + 1:]

        correct_answers = []
        correct_answer = ()
        observations = []
        observation = ()


        for (i, line) in enumerate(contents):
            read_line = line.rstrip()
            letters = read_line.split(" ")

            if read_line == "_ _":
                observations.append(observation)
                observation = ()
                continue
            if i + 1 == len(contents):
                observation = observation + (letters[1], )
                correct_answers.append(letters[0])
                observations.append(observation)
                observation = ()
                break

            observation = observation + (letters[1], )
            correct_answers.append(letters[0])

        correct_letters = []
        corrected_letters = []


        viterbi = Viterbi(observations[0], self.states, self.start_probability, self.transition_probability, self.emission_probability)
        hit = 0
        total = 0
        for (i, observation) in enumerate(observations):
            viterbi = Viterbi(observation, self.states, self.start_probability, self.transition_probability, self.emission_probability)
            corrected_letters = corrected_letters + viterbi.run_viterbi()[1]

        print "Some of the reconstructed state sequence: "
        for (i, letter) in enumerate(corrected_letters):
            if letter == correct_answers[i]:
                hit += 1
            if self.iteration < 100:
                print letter,
                self.iteration += 1
            total += 1


        print "\nPercent correctness:", hit/float(total) * 100

