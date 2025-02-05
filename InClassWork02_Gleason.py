# Function to print "Your Name!" to the console
def print_name():
    print("Ronan Gleason and Evan Queeney!")
    
#==============================================================================
def Check_Password():
    print("Create a password. Include an uppercase letter and a number, and make it at least 8 characters long.")
    userPass = input("Please enter a password: ")
    length = (len(userPass)) >= 8
    hasDigit = False
    hasUpper = False
    
    for char in userPass:
        if char.isdigit():
            hasDigit = True
            
        if char.isupper():
            hasUpper = True
          
    
    if length and hasDigit and hasUpper:
        print("Your password is valid.")
    else:
        print("Your password is not valid.")
    
    
#==============================================================================
# Main function to invoke the three functions
def main():
    
    print("Executing Question 2:")
    Check_Password()  # Call the function for Question 2
    
    print("\nExecuting Question 3:")
    ()  # Call the function for Question 2
#==============================================================================
# Invoke the main function
if __name__ == "__main__":
    main()
#==============================================================================
