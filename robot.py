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

        for line in contents:
            readline = line.rstrip()
            if readline == ".":
                break
            coordinate, color = readline.split(" ")

            if coordinate not in self.states:
                self.states = self.states + (coordinate,) 
            if color not in self.observations:
                self.observations = self.observations + (color,)

            start_probability = 1/float(len(self.states))

            for coordinate in self.states:
                self.start_probability[coordinate] = start_probability

        print self.states, self.observations, self.start_probability