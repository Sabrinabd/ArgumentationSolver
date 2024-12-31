# Importing necessary modules
import sys
import itertools
from itertools import permutations


# Initialize sets to store arguments and attacks
arguments = set()
attacks = set()

# Vérifie que le nom d'un argument est alphanumérique et qu'il ne fait pas partie des mots réservés arg ou att.
def is_valid_argument(arg):
    return arg.isalnum() and arg not in {"arg", "att"}

# Define a function to process each line in the input file
#Traite chaque ligne d'un fichier, en ajoutant les arguments valides à arguments et les attaques à attacks. Les attaques doivent concerner uniquement des arguments définis au préalable.
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

# Vérifie si un argument donné est attaqué par un autre argument (dans la relation d'attaque)
def is_attacked(arg, attacks):
    return any(x[1] == arg for x in attacks)

#Cette fonction renvoie l'ensemble des arguments qui attaquent un argument donné.
def get_arg_attackers(arg, attacks):

	attackers = set()
	for i in attacks:
		if i[1] == arg:
			attackers.add(i[0])
	return attackers
#Renvoie les arguments attaqués par un ensemble donné d'arguments.
def get_attacked_args(set_of_args, attacks):

	attacked = set()
	for i in attacks:
		if i[0] in set_of_args:
			attacked.add(i[1])
	return attacked

# Cette fonction génère tous les sous-ensembles possibles (ou "powerset") d'un ensemble donné.

def powerset(iterable):

	s = list(iterable)
	return set(itertools.chain.from_iterable(itertools.combinations(s, r) for r in range(len(s) + 1)))

#Vérifie si un argument est "acceptable" en fonction des attaques reçues et des extensions (ensemble E).
def compute_acceptability(arg, E, relations):

	attackers = get_arg_attackers(arg, relations)
	if attackers != None:
		atks = []
		for y in attackers:
			yStatus = False
			yAtackers = get_arg_attackers(y, relations)# Récupère les arguments attaquants
			if len(yAtackers.intersection(E)) > 0:# Vérifie si l'argument attaquant est dans l'ensemble E
				yStatus = True
			atks.append(yStatus)
		if all(atks):
			return True
		else:
			return False

# Vérifie que tous les arguments utilisés dans les relations d'attaque sont bien définis au préalable dans l'ensemble arguments.
def checkArgumentsInRelations(arguments, relations):

	if len(arguments) > 0:
		if len(relations) > 0:
			for x in relations:
				lst = []
				status = True
				if x[0] not in arguments or x[1] not in arguments:# Vérifie si les arguments utilisés dans les relations d'att aque sont bien définis
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

# Représente les extensions (ensembles d'arguments) obtenues à partir des sémantiques de la logique des argumentations
class Extensions:

	def __init__(self, extensions, arguments):
		self.__extensions = extensions
		self.__arguments = arguments

	def get_Extensions(self):

		return self.__extensions
	#Récupère les arguments acceptés de manière sceptique (acceptés dans toutes les extensions).
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
     # Récupère les arguments acceptés de manière crédule (acceptés dans au moins une extension)
	def get_CredulouslyAcceptedArguments(self):

		accepted = set()
		if len(self.__extensions) > 0:
			for a in self.__arguments:
				for extension in self.__extensions:
					if a in extension:
						accepted.add(a)
		return accepted

				

# La classe principale représentant le cadre d'argumentation de Dung. Elle contient les arguments, relations d'attaque, et les différentes méthodes pour calculer les extensions.
class Dung:

	def __init__(self, arguments, relations):
		self.__arguments = arguments
		self.__relations = relations
		self.semantics = Dung.Semantics(self)
 #Calcule les sous-ensembles admissibles (candidates for admissibility) en fonction des arguments et relations d'attaque.
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

 #Calcule l'admissibilité des sous-ensembles en vérifiant les attaques et en utilisant la méthode compute_cfs.
	def compute_admissibility(self):
		cfs = self.compute_cfs()

		rel = self.__relations

		admissible = []
		if checkArgumentsInRelations(self.__arguments, rel) == True:# Vérifie que les arguments utilisés dans les relations d attaque sont bien définis
			if len(cfs) > 0:
				for cfset in cfs:
					attackers = set()
					for cfsetmember in cfset:
						attackers = attackers.union(get_arg_attackers(cfsetmember, rel))# Récupère les arguments attaquants
					attackedbycfsmembers = []
					for attacker in attackers:
						atk = False
						attackedby = get_arg_attackers(attacker, rel)# Récupère les arguments attaqués
						for cfsetmember in cfset:
							if cfsetmember in attackedby:# Vérifie si l'argument attaqué est dans l'ensemble admissible
								atk = True
						attackedbycfsmembers.append(atk)
					if all(attackedbycfsmembers):# Vérifie si tous les arguments attaqués sont dans l'ensemble admissible
						if cfset == ():
							admissible.append(set())# Ajoute un ensemble vide si l'ensemble admissible est vide
						else:
							d = set()
							for k in cfset:# Ajoute les arguments attaqués à l'ensemble admissible
								for kk in k:
									d.add(kk)
							admissible.append(d)
				return admissible
			else:
				return []
		else:
			return None

 # Définit les sémantiques utilisées dans le cadre de Dung (extensions stables, complètes, etc.)	
	class Semantics:
		def __init__(self, af):
			self.af = af
         #Calcule les extensions stables en utilisant la sémantique stable.
		def compute_stable_extensions(self):

			if checkArgumentsInRelations(self.af._Dung__arguments, self.af._Dung__relations) == True:# Vérifie que les arguments utilisés dans les relations d attaque sont bien définis
				adm = self.af.compute_cfs()# Calcule les sous-ensembles admissibles
				stb = []
				if len(adm) > 0:
					for x in adm:
						if set(x).union(get_attacked_args(set(x), self.af._Dung__relations)) == self.af._Dung__arguments:# Vérifie si l'ensemble est stable
							stb.append(x)
				ext = Extensions(stb, self.af._Dung__arguments)# Crée une instance de la classe Extensions
				return ext 
			else:
				return None

		
		def compute_complete_extensions(self):#Calcule les extensions complètes en utilisant la sémantique complète.
	
			if checkArgumentsInRelations(self.af._Dung__arguments, self.af._Dung__relations)==True:# Vérifie que les arguments utilisés dans les relations d attaque sont bien définis
				compl = []
				adm = self.af.compute_admissibility()# Calcule les sous-ensembles admissibles
				if len(adm) > 0:
					for conj in adm:# Vérifie si l'ensemble est complet
						accArgs = set()# Arguments acceptés
						for x in self.af._Dung__arguments:
							if compute_acceptability(x, conj, self.af._Dung__relations) == True:# Vérifie si l'argument est acceptable
								accArgs.add(x)
						if accArgs == conj:
							compl.append(conj)

				ext = Extensions(compl, self.af._Dung__arguments) # Crée une instance de la classe Extensions
				return ext
			else:
				return None

# Décide si un argument appartient ou non à un ensemble d'arguments donné

def decide(elem, arg,set1):
    if elem in arg:
        if elem in set1:
            print("YES")
        else:
            print("NO")
    else:
        print("Argument not known")
        
#Vérifie si un ensemble d'arguments est une extension complète.
def verify_complete(set1, arg, bigset):
    for argument in set1:
        if argument not in arg:
            print(f"Error argument \"{argument}\"  not my arguments, Please change the argument name.")
            sys.exit(1) # Arrêt du programme avec un code d'erreur si les arguments sont insuffisants.
    if set(set1) in bigset:
        print("YES")
    else:
        print("NO")

#Vérifie si un ensemble d'arguments est une extension stable.
def verify_stable(set1, arg, bigset):
    for argument in set1:
        if argument not in arg:
            print(f"Error argument \"{argument}\"  not my arguments, Please change the argument name.")
            sys.exit(1) 
    if is_combination_in_list(set1, bigset):
         print("YES")
    else:
         print("NO")
         
#Traite les données d'entrée, soit un argument unique, soit un ensemble d'arguments séparés par des virgules.

def process_data(input_data):
    if input_data== "arg" or input_data=="att":
        print(f"An argument cannot be named {input_data}")
        sys.exit(1)
    # Check if input_data contains commas
    if ',' in input_data:
        # If commas are present, split the data and store it in a tuple
        dataDecide = tuple(map(str.strip, input_data.split(',')))
    else:
        # If no commas, store the single alphanumeric word
        dataDecide = input_data.strip()

    return dataDecide
 #Vérifie si une combinaison (ou permutation) d'arguments existe dans une liste de tuples
def is_combination_in_list(check_tuple, tuple_list):
    
    for permuted_tuple in permutations(check_tuple):# Génère toutes les permutations possibles de l'ensemble d'arguments
        if permuted_tuple in tuple_list:# Vérifie si la combinaison existe dans la liste
            return True
    return False

