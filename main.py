# importing modules
from read import readProductFile, getNaturalNumber
from operations import displayInventory, sellProducts, restockProducts

# Main Program Execution Block
if __name__ == "__main__":
    # setting product file name to a variable for passing to functions 
    productFileName = "products.txt" 
    # designing CLI
    print("======================================")
    print("   WeCare Inventory Management System ")
    print("======================================")
    
    # storing product info in a variable 
    allProducts = readProductFile(productFileName) 
    # main code loop 
    while True:
        print("\n+------------ MAIN MENU -------------+")
        print("| 1. Show Stock (Cost Price)         |") 
        print("| 2. Sell Products                   |") 
        print("| 3. Restock Products                |") 
        print("| 4. Exit                            |") 
        print("+------------------------------------+")
        
        # getting natural number as input 
        choice = getNaturalNumber("Enter choice (1-4):") 
        # call displayInventory function 
        if choice == 1:
            displayInventory(allProducts) 

        # call sellProducts function 
        elif choice == 2:
            sellProducts(allProducts, productFileName) 
            
        # call restockProducts function 
        elif choice == 3:
            restockProducts(allProducts, productFileName) 
            
        # exit the system 
        elif choice == 4:
            print("\nExiting System. Goodbye!") 
            break 
        else:
            print("Invalid choice. Please enter 1-4.") 
        
        if choice != 4: # Pause, only if not exiting
             input("\n... Press Enter to continue ...")