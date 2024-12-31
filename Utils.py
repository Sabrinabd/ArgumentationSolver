# Importing necessary modules
import sys
import itertools
from itertools import permutations


# Initialize sets to store arguments and attacks
arguments = set()
attacks = set()

# Define a function to check if an argument name is valid
def is_valid_argument(arg):
    return arg.isalnum() and arg not in {"arg", "att"}

# Define a function to process each line in the input file

def process_line(line, line_number):
    stripped_line = line.strip()
    
     # Check if the line starts with "arg(" or "att("
    if stripped_line.startswith(("arg(", "att(")):
        parts = stripped_line.split("(")
        command, item = parts[0], parts[1].rstrip(').')
        if command == "arg" and is_valid_argument(item):
            arguments.add(item)
        elif command == "att":
            items = item.split(",")
            if all(arg in arguments for arg in items):
                attacks.add(tuple(items))
            else:
                print(f"Error on line {line_number}: Arguments in attack not defined before use.")
                sys.exit(1)  # Terminate the program with an exit code
        else:
            print(f"Error on line {line_number}: Please change the argument name.")
            sys.exit(1)  # Terminate the program with an exit code

# Function to check if an argument is attacked by any other argument
def is_attacked(arg, attacks):
    return any(x[1] == arg for x in attacks)

# Functions to get attackers and attacked arguments for a given argument
def get_arg_attackers(arg, attacks):

	attackers = set()
	for i in attacks:
		if i[1] == arg:
			attackers.add(i[0])
	return attackers

def get_attacked_args(set_of_args, attacks):

	attacked = set()
	for i in attacks:
		if i[0] in set_of_args:
			attacked.add(i[1])
	return attacked

# Function to compute powerset of an iterable

def powerset(iterable):

	s = list(iterable)
	return set(itertools.chain.from_iterable(itertools.combinations(s, r) for r in range(len(s) + 1)))

# Function to compute acceptability of an argument in a given set of arguments and relations
def compute_acceptability(arg, E, relations):

	attackers = get_arg_attackers(arg, relations)
	if attackers != None:
		atks = []
		for y in attackers:
			yStatus = False
			yAtackers = get_arg_attackers(y, relations)
			if len(yAtackers.intersection(E)) > 0:
				yStatus = True
			atks.append(yStatus)
		if all(atks):
			return True
		else:
			return False

