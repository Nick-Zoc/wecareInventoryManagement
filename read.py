# Input Validation Functions

# Helper Function for getting a Natural number from the user.
def getNaturalNumber(prompt):
    """
    Helper Function
    Getting a natural number (integer > 0) from the user via input.
    It continuously prompts the user until a valid natural number is entered.

    · Parameters:
        prompt (str): The message displayed to the user, asking for input.
    · Returns:
        int: The valid natural number (integer greater than 0) entered by the user.
    · Raises:
        (Internally handles ValueError if the input cannot be converted to an integer,
         or if the number is not positive, by re-prompting the user. Does not
         propagate these exceptions if a valid number is eventually returned.)
    """
         
    while True:
        try:
            # Getting input and attempting conversion to Natural Number
            value = int(input(prompt + " ")) 
            if value > 0:
                return value # Returning valid Natural number
            else:
                print("Input Error: Please enter a Natural Number (1 or greater).")
        except ValueError:
            # Handling error if input is not a Natural number
            print("Input Error: Invalid input. Please enter a Natural number.")

# Helper Function for getting a product ID from the user that exists in our product dictionary.
def getValidProductId(prompt, productDataDict):
    """
    Helper Function
    Getting a product ID from the user and validating if it exists as a key
    in the provided product dictionary.

    · Parameters:
        prompt (str): The message displayed to the user, asking for the product ID.
        productDataDict (dict): A dictionary containing product information, where keys
                                are product IDs (int) and values are lists of product details.
    · Returns:
        int: The valid product ID (an existing key in productDataDict) entered by the user.
    · Raises:
        (Internally handles invalid numerical input via getNaturalNumber.
         Prompts again if the ID is not found in productDataDict.)
    """

    while True:
        # Using getNaturalNumber for ensuring a number is entered.
        productId = getNaturalNumber(prompt)
        # Checking if the entered productId exists as a key in the productDataDict.
        if productId in productDataDict:
            return productId # Returning the valid ID.
        else:
            # Printing an error message if ID is not found.
            print("Error: Product ID not found in inventory. Please try again.")

# File Handling Functions

# Helper Function for reading the product data from the specified text file.
def readProductFile(fileName):
    """
    Helper Function
    Reading product data from a specified text file and loading it into a dictionary.
    Each line in the file is expected to represent a product with comma-separated values.

    · Parameters:
        fileName (str): The name of the text file (e.g., "products.txt") to read from.
    · Returns:
        dict: A dictionary where keys are auto-incrementing integer product IDs and
              values are lists of product details:
              [Name (str), Brand (str), Quantity (int), CostPrice (int), Origin (str)].
              Returns an empty or partially filled dictionary if errors occur during reading
              or if the file is empty/corrupted.
    · Raises:
        (Prints error messages to the console for FileNotFoundError or other general
         exceptions encountered during file reading or data parsing, returns the current state of the productDataDict.)
    """
    productDataDict = {} # Initializing dictionary
    productId = 1        # Starting ID
    try:
        file = open(fileName, "r")      # Opening file for reading
        allLines = file.readlines()     # Reading all lines
        file.close()                    # Closing file
        for line in allLines:
            # Removing newline and splitting by comma.
            cleanedLineParts = line.replace("\n", "").split(",") 
            # converting parts to int
            name = cleanedLineParts[0]
            brand = cleanedLineParts[1]
            qty = int(cleanedLineParts[2])     
            price = int(cleanedLineParts[3])
            origin = cleanedLineParts[4]
            productDataDict[productId] = [name, brand, qty, price, origin]
            productId += 1 # Incrementing ID
    except Exception as e: # General catch for other file reading issues
        print("An error occurred reading the file '" + fileName + "': " + str(e))
    return productDataDict # Returning the dictionary


# Helper function for asking user if they want to continue
def askToContinue(prompt):
    """
    Helper Function
    Asking the user a yes/no question based on the provided prompt and returns
    their choice as a boolean value. Handles 'y', 'yes', 'n', 'no' case-insensitively.

    · Parameters:
        prompt (str): The question to display to the user.
    · Returns:
        bool: True if the user's input signifies 'yes' (e.g., 'y', 'yes').
              False if the user's input signifies 'no' (e.g., 'n', 'no').
              Defaults to False if an unexpected error occurs during input.
    · Raises:
        Dosent raise error, uses else to handle wrong input.
    """
    while True:
        choice = input(prompt + " (y/n): ")
        # Using string.lower() method for case insensitive comparison
        lowerChoice = choice.lower() 
        
        if lowerChoice == "y" or lowerChoice == "yes":
            return True
        elif lowerChoice == "n" or lowerChoice == "no":
            return False
        else:
            print("Invalid input. Please enter 'y' for yes or 'n' for no.")

