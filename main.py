import os
import sys
import Utils as utl


if __name__ == "__main__":



    
    problem_type = ""
    file_path = ""
    query_args = []
    
    if len(sys.argv) < 5:
        print("Please enter a command like: python myfile.py -p [VE-CO | VE-ST | DC-CO | DS-CO | DC-ST | DS-ST] -f FILE -a ARG1,ARG2,...,ARGn")
        sys.exit(1)
    else:
         problem_type = sys.argv[2]
         file_path = sys.argv[4]
         query_args = sys.argv[6] if len(sys.argv) > 6 else "" 

        

 
    
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
    

    AF = utl.Dung(utl.arguments, utl.attacks)
    
    st = AF.semantics.compute_stable_extensions()
    co = AF.semantics.compute_complete_extensions()
    
    st_ext=st.get_Extensions()
    co_ext=co.get_Extensions()
    
    st_skep=st.get_SkepticallyAcceptedArguments()

    co_skep=co.get_SkepticallyAcceptedArguments()
    
    st_cred=st.get_CredulouslyAcceptedArguments()
    co_cred=co.get_CredulouslyAcceptedArguments()
    
    argument_or_set= utl.process_data(query_args)
    
    
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

