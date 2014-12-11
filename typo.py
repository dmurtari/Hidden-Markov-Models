import string
from viterbi import Viterbi

class Typo():

    def __init__(self, file):
        self.states = ()
        self.observations = ()
        self.start_probability = {}
        self.transition_probability = {}
        self.emission_probability = {}
        self.parse(file)

    def parse(self, file):
        with open(file) as robot_data:
            contents = robot_data.readlines()

        start_letters = [0]*26
        start_counter = 0
        # starts = {}
        # moves = 0
        # previous_line = "."
        # transitions = [[0 for x in range(5)] for x in range(5)]
        transitions = {}
        previous_letter = ""

        self.states = ("a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o",
            "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z")

        for i in range(26):
            self.transition_probability[chr(ord('a') + i)] = {"counter" : 0}
            for j in range(26):
                self.transition_probability[chr(ord('a') + i)][chr(ord('a') + j)] = 0

        for i in range(26):
            self.emission_probability[chr(ord('a') + i)] = {"counter" : 0}
            for j in range(26):
                self.emission_probability[chr(ord('a') + i)][chr(ord('a') + j)] = 0


        first_line = True
        for line in contents:
            read_line = line.rstrip()
            if read_line == "_ _":
                previous_line = read_line
                first_line = True
                continue
            if read_line == "..":
                print "End of Test Data"
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

        viterbi = Viterbi(("a", "c", "v", "o", "u", "n", "t"), self.states, self.start_probability, self.transition_probability, self.emission_probability)
        print viterbi.run_viterbi()

