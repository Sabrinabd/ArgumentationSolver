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

# Function to check if arguments are defined in relations
def checkArgumentsInRelations(arguments, relations):

	if len(arguments) > 0:
		if len(relations) > 0:
			for x in relations:
				lst = []
				status = True
				if x[0] not in arguments or x[1] not in arguments:
					status = False
				lst.append(status)	 
				if all(lst):
					return True
				else:
					return False
		else:
			return True
	else:
		return False

# Class for representing extensions
class Extensions:

	def __init__(self, extensions, arguments):
		self.__extensions = extensions
		self.__arguments = arguments

	def get_Extensions(self):

		return self.__extensions
		
	def get_SkepticallyAcceptedArguments(self):

		accepted = set()
		if len(self.__extensions) > 0:
			for a in self.__arguments:
				lst = []
				for extension in self.__extensions:
					if a in extension:
						lst.append(True)
					else:
						lst.append(False)
				if all(lst):
					accepted.add(a)
		return accepted

	def get_CredulouslyAcceptedArguments(self):

		accepted = set()
		if len(self.__extensions) > 0:
			for a in self.__arguments:
				for extension in self.__extensions:
					if a in extension:
						accepted.add(a)
		return accepted

				

# Class for representing Dung Argumentation Framework
class Dung:

	def __init__(self, arguments, relations):
		self.__arguments = arguments
		self.__relations = relations
		self.semantics = Dung.Semantics(self)

	def compute_cfs(self):

		args = self.__arguments
		rel = self.__relations

		pwr = powerset(args)

		la = len(args)
		lr = len(rel)

		if la > 0:
			if lr > 0:
				for x in rel:
					x1 = x[0]
					x2 = x[1]
					dele = []
					for i in pwr:
						if (x1 in i) and (x2 in i):
							dele.append(i)
					for e in dele:
						pwr.remove(e)
		return set(pwr)


	def compute_admissibility(self):
		cfs = self.compute_cfs()

		rel = self.__relations

		admissible = []
		if checkArgumentsInRelations(self.__arguments, rel) == True:
			if len(cfs) > 0:
				for cfset in cfs:
					attackers = set()
					for cfsetmember in cfset:
						attackers = attackers.union(get_arg_attackers(cfsetmember, rel))
					attackedbycfsmembers = []
					for attacker in attackers:
						atk = False
						attackedby = get_arg_attackers(attacker, rel)
						for cfsetmember in cfset:
							if cfsetmember in attackedby:
								atk = True
						attackedbycfsmembers.append(atk)
					if all(attackedbycfsmembers):
						if cfset == ():
							admissible.append(set())
						else:
							d = set()
							for k in cfset:
								for kk in k:
									d.add(kk)
							admissible.append(d)
				return admissible
			else:
				return []
		else:
			return None

 