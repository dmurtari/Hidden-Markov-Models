Hidden Markov Models
====================

Implementation of Hidden Markov Models in Python. All parts of the problem
have been successfully implements, but our implementation only supports first
order Hidden Markov Models

Robot
-----

Run with: `python assignmnet5.py -p 1 -o 1`

Algorithm will scan file building CPT's until it sees a '..', at which point
it will call Viterbi using the observations from each of the 200 steps. Output
includes some of the CPT's, the first five reconstructed movements given by
Viterbi, as well as the percentage correct of each of the 200 sets (with an
average printed at the end).

Sample output is included in `problem1_out.txt`


Typos
------

Run with: `python assignment5.py -p 2 -o 1`

Algorithm will scan file building CPT's until it sees a '..', at which point it
will call Viterbi using the words with typos. Ouput includes the CPT's, the
first 100 letters from Viterbi, and the percentage correct for the whole test
section.

Sample output is included in `problem2_out.txt`


Topics
------

Run with: `python assignment5.py -p 3 -o 1`

Algorithm scans topics file reading in topics and words associated with each
topic. After it reaches a '..', Viterbi starts running with each observation 
(set of words) and we compare the topic Viterbi generates with the actual topic.

Run time is very long, so a sample output is included in `problem3_out.txt`