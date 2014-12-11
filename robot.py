class Robot():

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

        starts = {}
        total_starts = 0
        total_transitions = 0
        previous_coordinate = "."

        for line in contents:
            read_line = line.rstrip()
            if read_line == ".":
                previous_coordinate = read_line
                continue
            if read_line == "..":
                print "End of Test Data"
                break

            coordinate, color = read_line.split(" ")

            # Generate the list of available coordinates and observable colors 
            # fom the given data
            if coordinate not in self.states:
                self.states = self.states + (coordinate,) 
            if color not in self.observations:
                self.observations = self.observations + (color,)

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

                if previous_coordinate not in self.transition_probability:
                    self.transition_probability[previous_coordinate] = {}

                if coordinate not in self.transition_probability[previous_coordinate]:
                    self.transition_probability[previous_coordinate][coordinate] = 0
                else:
                    self.transition_probability[previous_coordinate][coordinate] += 1

            previous_coordinate = coordinate

        for coordinate in self.states:
            self.start_probability[coordinate] = starts[coordinate]/float(total_starts)

        for start, transition in self.transition_probability.iteritems():
            for end, count in transition.iteritems():
                self.transition_probability[start][end] = count/float(total_transitions)

        print self.transition_probability