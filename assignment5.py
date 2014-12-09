import getopt
import sys

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


    
if __name__ == "__main__":
    main()