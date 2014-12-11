import string

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

        print contents
        start_letters = [0]*26
        start_counter = 0
        # starts = {}
        # moves = 0
        # previous_line = "."
        # transitions = [[0 for x in range(5)] for x in range(5)]
        transitions = {}
        previous_letter = ""

        for i in range(26):
            self.transition_probability[chr(ord('a') + i)] = {"counter" : 0}

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

        for key in self.emission_probability:
            for child_key in self.emission_probability[key]:
                if child_key != "counter":
                    count = self.emission_probability[key][child_key] + 1
                    self.emission_probability[key][child_key] = count / float(self.emission_probability[key]["counter"] + 26)

        #     coordinate, color = read_line.split(" ")
        #     moves += 1

        #     if coordinate not in self.states:
        #         self.states = self.states + (coordinate,)
        #     if color not in self.observations:
        #         self.observations = self.observations + (color,)

        #     if coordinate not in starts:
        #         starts[coordinate] = 1
        #     else:
        #         starts[coordinate] += 1

        # for coordinate in self.states:
        #         self.start_probability[coordinate] = starts[coordinate]/float(moves)

        # print self.states, self.observations, self.start_probability
