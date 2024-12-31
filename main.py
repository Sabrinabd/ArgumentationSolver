import os
import sys
import Utils as utl  # Importation du module 'Utils' qui contient les fonctions utilitaires nécessaires à l'exécution du programme



if __name__ == "__main__":



    # Initialisation des variables pour le type de problème, le chemin du fichier et les arguments de la requête
    problem_type = ""
    file_path = ""
    query_args = []
    
     # Vérification du nombre d'arguments passés en ligne de commande. Si ce n'est pas suffisant, un message d'erreur est affiché.
    if len(sys.argv) < 5:
        print("Please enter a command like: python myfile.py -p [VE-CO | VE-ST | DC-CO | DS-CO | DC-ST | DS-ST] -f FILE -a ARG1,ARG2,...,ARGn")
        sys.exit(1)# Arrêt du programme avec un code d'erreur si les arguments sont insuffisants.
    else:# Si les arguments sont présents, on extrait le type de problème, le chemin du fichier et les arguments de la requête
         problem_type = sys.argv[2]# Type de problème (VE-CO, VE-ST, DC-CO, etc.)
         file_path = sys.argv[4]# Chemin du fichier à traiter
         query_args = sys.argv[6] if len(sys.argv) > 6 else "" # Arguments de la requête (peut être vide si non spécifié)

        

 
      # Vérification de l'existence du fichier spécifié
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r') as file:
                for line_number, line in enumerate(file, start=1):
                    utl.process_line(line, line_number)

        except (FileNotFoundError, IOError) as e:
            print(f"An error occurred: {e}")
            sys.exit(1)  # Terminate the program with an exit code
    else:
        print(f"The file {file_path} does not exist.")
        sys.exit(1)  #  Terminate the program with an exit code
    
 # Création d'une instance de la classe Dung avec les arguments et attaques extraits du fichier
    AF = utl.Dung(utl.arguments, utl.attacks)
    
     # Calcul des extensions stables et complètes à partir de l'instance Dung
    st = AF.semantics.compute_stable_extensions()
    co = AF.semantics.compute_complete_extensions()
    
     # Récupération des extensions stables et complète
    st_ext=st.get_Extensions()
    co_ext=co.get_Extensions()
    
    # Récupération des arguments acceptés sceptiquement pour les extensions stables et complètes
    st_skep=st.get_SkepticallyAcceptedArguments()

    co_skep=co.get_SkepticallyAcceptedArguments()
    
    # Récupération des arguments acceptés crédulement pour les extensions stables et complètes
    st_cred=st.get_CredulouslyAcceptedArguments()
    co_cred=co.get_CredulouslyAcceptedArguments()
    
    # Traitement des données de la requête (par exemple, convertir des arguments sous forme de liste)
    argument_or_set= utl.process_data(query_args)
    
     # Vérification et décision en fonction du type de problème spécifié
    if problem_type == "VE-CO":
        utl.verify_complete(argument_or_set, utl.arguments,co_ext)

    elif problem_type == "VE-ST":  
        utl.verify_stable(argument_or_set, utl.arguments,st_ext)


    elif problem_type in ["DC-CO", "DS-CO", "DC-ST", "DS-ST"]:
      
        if problem_type == "DC-CO":
            utl.decide(argument_or_set, utl.arguments,co_cred)
        elif problem_type == "DS-CO":
            utl.decide(argument_or_set, utl.arguments,co_skep)
        elif problem_type == "DC-ST":
            utl.decide(argument_or_set, utl.arguments,st_cred)
        elif problem_type == "DS-ST":
            utl.decide(argument_or_set, utl.arguments,st_skep)

