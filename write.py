# Importing the datetime library. This is needed for getting the current date and time 
from datetime import datetime 

# File Handling Functions

# Helper Function for writing the current state of the product dictionary back to the text file.
def writeProductsToFile(fileName, productDataDict):
    """
    Helper Function
    Writing the current product data from a dictionary back to a specified text file,
    overwriting any existing content in that file.

    · Parameters:
        fileName (str): The name of the text file (e.g., "products.txt") to write to.
        productDataDict (dict): A dictionary containing the current product data,
                                where keys are product IDs and values are lists of details.
    · Returns:
        bool: True if the data was successfully written to the file, if False otherwise.
    · Raises:
        (Prints error messages to the console for IOErrors or other general exceptions
         encountered during file writing, instead, returns False.)
    """

    try:
        # Opening the file in write mode ("w").
        file = open(fileName, "w")
        # Looping through each product (value) in the dictionary.
        for details in productDataDict.values():
            # Building the line item by item, converting all to string
            line = details[0] + "," + details[1] + "," + str(details[2]) + "," + str(details[3]) + "," + details[4] + "\n"
            file.write(line)      # Writing the formatted line to the file.
        file.close()      # Closing the file after writing all product entries.
        return True
    except Exception as e:      # Handling errors during writing
        print("Error writing to file '" + fileName + "': " + str(e))
        return False

# Invoice Generation Functions

# Helper Function for creating a unique filename for an invoice, including customer/supplier name.
def generateInvoiceName(type, name):
    """
    Helper Function
    Creating a unique filename for an invoice, having the type of invoice,
    a relevant name (customer or supplier), and a timestamp.

    · Parameters:
        type (str): A string indicating the type of invoice (e.g., "SALES", "RESTOCK").
        name (str): The customer or supplier name to be included in the filename.
    · Returns:
        str: The generated unique invoice filename (e.g., "SALES_Customer_Name_YYYY-M-D_H-M.txt").
    · Raises:
        (Prints an error message if an exception occurs during timestamp generation. )
    """

    try:
        # store present date and time .
        now = datetime.now()
        # convert and store time as string.
        timestamp = str(now.year) + "-" + str(now.month) + "-" + str(now.day) + "_" + str(now.hour) + "-" + str(now.minute)    
        return type + "_" + name + "_" + timestamp + ".txt" # Constructing filename
    except Exception as e:
        print("Error generating invoice name: " + str(e))

# Helper Function for writing invoice lines to a file.
def writeInvoice(fileName, lines):
    """
    Helper Function
    Writing an invoice to a specified text file.

    · Parameters:
        fileName (str): The name of the invoice file to be created/written to.
        lines (list): A list of strings, where each string is one line of the
                      invoice content.
    · Returns:
        bool: True if the invoice file was written successfully, False otherwise.
    · Raises:
        (Prints error messages to the console for IOErrors or other general exceptions
         encountered during file writing, returns False.)
    """
    try:
        invoiceFile = open(fileName, "w") # Opening invoice file for writing
        for line in lines:
            invoiceFile.write(line + "\n") # Writing each line
        invoiceFile.close() # Closing file
        print("Invoice file generated successfully: " + fileName) 
        return True # Signaling success
    except Exception as e: # General exception for file writing issues
        print("Error writing invoice file '" + fileName + "': " + str(e))
        return False
