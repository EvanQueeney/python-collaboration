def number():
    num=int(input("Please enter a number: "))
    if num%5==0:
        print("HiFive")
    
    if num%2==0:
        print("HiEven")

#==============================================================================
# Main function to invoke the two functions
def main():
    
    print("Executing Question 1:")
    number()  # Call the function for Question 1
    
#==============================================================================
# Invoke the main function
if __name__ == "__main__":
    main()
#==============================================================================