import getopt
import sys
from robot import Robot
from typo import Typo

def main():
    arguments, remainder = getopt.getopt(sys.argv[1:], 'p:o:')

    for option, argument in arguments:
        if option == "-p":
            if argument not in ("1", "2", "3"):
                print "Please specify 1, 2, or 3"
                exit()
            problem = argument
        elif option == "-o":
            if argument not in ("1", "2"):
                print "Please specify a valid order 1 or 2"
                exit()
            order = argument

        if problem == "1":
            robot = Robot("./Assignment5DataSets/robot_no_momentum.data")
        elif problem == "2":
            typo = Typo("./Assignment5DataSets/typos10.data")



if __name__ == "__main__":
    main()
