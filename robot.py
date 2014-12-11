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
        moves = 0
        previous_line = "."
        transitions = [[0 for x in range(5)] for x in range(5)] 

        for line in contents:
            read_line = line.rstrip()
            if read_line == ".":
                previous_line = read_line
                continue
            if read_line == "..":
                print "End of Test Data"
                break

            coordinate, color = read_line.split(" ")
            moves += 1

            if coordinate not in self.states:
                self.states = self.states + (coordinate,) 
            if color not in self.observations:
                self.observations = self.observations + (color,)

            if coordinate not in starts:
                starts[coordinate] = 1
            else:
                starts[coordinate] += 1

        for coordinate in self.states:
                self.start_probability[coordinate] = starts[coordinate]/float(moves)

        print self.states, self.observations, self.start_probability