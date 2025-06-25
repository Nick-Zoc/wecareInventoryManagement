#importing modules

from datetime import datetime

# importing user made modules

from read import getValidProductId, askToContinue, getNaturalNumber
from write import writeProductsToFile, generateInvoiceName, writeInvoice

# Display Functions 

# Function for displaying products with calculated Selling Price
def displaySellingPrice(productDataDict):
    """
    Main Function
    Displaying the products from the inventory with their calculated selling price
    (200% markup on the cost price) in a formatted table on the console.

    · Parameters:
        productDataDict (dict): The dictionary containing product data, where keys are
                                product IDs and values are lists of product details
                                including the cost price at index 3.
    · Returns:
        None: This function only prints to the console.
    · Raises:
        Nothing
    """

    # design CLI for user
    print("\n" + "=" * 90) 
    print("---------------------------- Available Products (Selling Price) --------------------------")
    print("-" * 90)
    print("ID\tName\t\t\tBrand\t\tQty\tSelling Price\tOrigin") 
    print("-" * 90)
    
    for productId, details in productDataDict.items():
        sellingPrice = details[3] * 2 # CostPrice is at index 3
        # Using tabs for display.
        print(str(productId) + "\t" + details[0] + "\t\t" + details[1] + "\t" + str(details[2]) + "\t" + str(sellingPrice) + "\t\t" + details[4])
            
    print("=" * 90)

# Function for displaying products with Cost Price.
def displayInventory(productDataDict):
    """
    Main Function
    Displaying the products from the inventory with their original cost price
    in a formatted table on the console.

    · Parameters:
        productDataDict (dict): The dictionary containing product data, where keys are
                                product IDs and values are lists of product details
                                including the cost price at index 3.
    · Returns:
        None: This function only prints to the console.
    · Raises:
        Nothing
    """
    # design CLI for user 
    print("\n" + "=" * 90) 
    print("----------------------------- Raw Inventory Data (Cost Price) ----------------------------")
    print("-" * 90)
    print("ID\tName\t\t\tBrand\t\tQty\tCost Price\tOrigin") 
    print("-" * 90)
    

    for productId, details in productDataDict.items():
        # Displaying product details with original cost price.
        print(str(productId) + "\t" + details[0] + "\t\t" + details[1] + "\t" + str(details[2]) + "\t" + str(details[3]) + "\t\t" + details[4])
            
    print("=" * 90)

# Core Logic Functions

# Function for handling selling products.
def sellProducts(productDataDict, productFileName):
    """
    Main Function
    Managing the entire process of selling products to a customer.
    This includes:
    - Displaying available products with selling prices.
    - Allowing the user to add multiple products to a cart.
    - Applying a "buy 3 get 1 free" offer.
    - Validating stock availability.
    - Updating stock levels in memory immediately after an item is added to the cart
      for live display updates.
    - Collecting customer name and phone number.
    - Generating a sales invoice file with a unique name.
    - Displaying the generated invoice content to the terminal.
    - Adding the final stock changes to the inventory file.

    · Parameters:
        productDataDict (dict): The main inventory dictionary. This dictionary is
                                modified directly by this function to reflect stock changes.
                                Keys are product IDs (int), values are lists:
                                [Name (str), Brand (str), Quantity (int), CostPrice (int), Origin (str)].
        productFileName (str): The name of the text file where inventory data is stored
                               (e.g., "products.txt"), used for saving the updated inventory.
    · Returns:
        None: This function handles all operations and outputs directly.
    · Raises:
        (Internally handles errors like invalid input using helper functions.
         Prints warnings or error messages to the console for issues like insufficient
         stock, problems updating stock in memory, or failures in writing invoice/inventory
         files. Dosent disturb the flow of program)
    · Example (Only for demonstration purposes):
        product_data = {1: ['Serum', 'Garnier', 10, 500, 'France']}
        sellProducts(product_data, "products.txt")
            User is prompted for customer name, phone, product ID (e.g., 1), quantity (e.g., 3).
            User can continue to add more products with 'y', 'yes' or checkout with 'n', 'no'.
            The product_data in memory becomes {1: ['Serum', 'Garnier', 6, 500, 'France']} (10 - (3 paid + 1 free)).
            If successful, an invoice "SALES_CustomerName_YYYY-M-D_H-M.txt" is created.
            The invoice details are printed to the terminal.
            The "products.txt" file is updated with the new stock level.
    """

    # Checking if inventory is empty at the beginning of the function
    if not productDataDict: 
        print("\nInventory is empty. Cannot sell any products at the moment.")
        return 

    cart = [] # Initializing cart for this transaction
    
    # Getting customer details first
    customerName = input("Enter customer name for invoice: ")
    customerPhone = input("Enter customer phone number: ") # Getting phone number

    while True: # Looping for adding items to cart
        displaySellingPrice(productDataDict) # Displaying products with selling price
        
        # Getting product ID from user
        productId = getValidProductId("Enter Product ID to sell:", productDataDict)
        
        # Getting product details
        details = productDataDict[productId] 
        name, brand, currentStock, costPrice, origin  = details 
        sellingPrice = costPrice * 2
        
        print("\nSelected: " + name + ", Stock: " + str(currentStock) + ", Selling Price: " + str(sellingPrice) + ", Origin: " + str(origin))
        if currentStock == 0: 
            print("This item is currently out of stock.")
        else:
            quantityToBuy = getNaturalNumber("Enter quantity to buy:")
            freeItems = quantityToBuy // 3 # Calculating free items
            totalItemsToRemove = quantityToBuy + freeItems # Calculating total items to remove from stock
            
            if totalItemsToRemove > currentStock: # Checking stock availability
                print("Error: Not enough stock for " + str(quantityToBuy) + " + " + str(freeItems) + " free.")
            else:
                # Adding item to cart
                cart.append({"id": productId, "name": name, "brand": brand, "paidQty": quantityToBuy, "totalQty": totalItemsToRemove, "price": sellingPrice})
                print(str(quantityToBuy) + "(+" + str(freeItems) + " free) " + name + " added to cart.")
                
                # Update stock only in memory for just display
                try:
                    productDataDict[productId][2] = currentStock - totalItemsToRemove 
                except Exception as e:
                    #handly any type of exception
                    print("Error temporarily updating stock in memory for display for ID " + str(productId) + ": " + str(e))
        
        
        # Asking if user wants to add another product
        if not askToContinue("Add another product to the cart?"):
            break # Exiting loop to checkout

    # Checkout Process
    
    # Generating invoice filename including customer name
    invoiceFileName = generateInvoiceName("SALES", customerName) 
    # Initializing invoice lines including customer phone
    invoiceLines = ["--- WeCare Sales Invoice ---", "Customer: " + customerName, "Phone: " + customerPhone, "Date: " + str(datetime.now()), "-"*50]
    grandTotal = 0

    # Processing cart items for invoice and updating stock
    for item in cart:
        lineTotal = item["paidQty"] * item["price"]
        grandTotal += lineTotal
        invoiceLine = (item["name"] + " (" + item["brand"] + ") - Qty: " + str(item["totalQty"]) + " (Paid: " + str(item["paidQty"]) + ") X " + str(item["price"]) + " = " + str(lineTotal))
        invoiceLines.append(invoiceLine)

    # Extending invoice lines with footer
    invoiceLines.extend(["-"*50, "Grand Total: Nrs " + str(grandTotal), "-"*50, "Thank you!"])

    # Writing invoice to file and displaying in terminal
    if writeInvoice(invoiceFileName, invoiceLines):
        print("\n--- Invoice Details (Printed to Terminal) ---")
        for line_to_print in invoiceLines: 
            print(line_to_print)
        print("---------------------------------------------")
        # Writing updated inventory to file
        if not writeProductsToFile(productFileName, productDataDict):
            print("Warning: Invoice generated & displayed, but inventory file update failed!")
    else:
        print("Warning: Invoice writing failed. Inventory file not updated.")

# Function for handling restocking.
def restockProducts(productDataDict, productFileName):
    """
    Main Function
    Managing the process of restocking products from a supplier.
    This includes:
    - Displaying the current raw inventory with cost prices.
    - Allowing the user to add multiple products to restock in a restock list.
    - Inputting the quantity being added and the new cost price for each item.
    - Updating stock levels and cost prices in memory immediately after an item is
      processed for live display updates.
    - Collecting supplier name and phone number.
    - Generating a restock invoice file with a unique name.
    - Displaying the generated invoice content to the terminal.
    - Adding the final stock and price changes to the inventory file.

    · Parameters:
        productDataDict (dict): The main inventory dictionary. This dictionary is
                                modified directly by this function.
                                Keys are product IDs (int), values are lists:
                                [Name (str), Brand (str), Quantity (int), CostPrice (int), Origin (str)].
        productFileName (str): The name of the text file where inventory data is stored
                               (e.g., "products.txt"), used for saving the updated inventory.
    · Returns:
        None: This function handles all operations and outputs directly.
    · Raises:
        (Internally handles errors like invalid input using helper functions.
         Prints warnings or error messages to the console for issues like problems
         updating stock/price in memory, or failures in writing invoice/inventory files.
         Dosent disturb the flow of program.)
    · Example (Only for demonstration purposes):
        product_data = {1: ['Serum', 'Garnier', 6, 500, 'France']}
        restockProducts(product_data, "products.txt")
            User is prompted for supplier name, phone, product ID (e.g., 1),
            quantity to add (e.g., 10), and new cost price (e.g., 480).
            User can continue to add more products to restock with 'y', 'yes' or checkout with 'n', 'no'.
            The product_data in memory becomes {1: ['Serum', 'Garnier', 16, 480, 'France']}.
            If successful, an invoice "RESTOCK_SupplierName_YYYY-M-D_H-M.txt" is created.
            The invoice details are printed to the terminal.
            The "products.txt" file is updated with the new stock and cost price.
    """
    # Checking if inventory is empty at the beginning
    if not productDataDict:
        print("\nInventory is empty. add products to the file to restock it.")
        return

    restockList = [] 
    supplierName = input("Enter supplier name for invoice: ") # Getting supplier name once
    supplierPhone = input("Enter supplier phone number: ") # Getting phone number
    

    while True: # Looping for adding items to restock list
        displayInventory(productDataDict) # Displaying current raw inventory
        
        # Getting product ID from user for restocking
        productId = getValidProductId("Enter Product ID to restock:", productDataDict)
        
        # Getting product details
        details = productDataDict[productId] # productId is guaranteed to be valid here
        name, brand, currentStock, currentCost, origin = details

        print("\nRestocking: " + name + ", Current Stock: " + str(currentStock) + ", Current Cost: " + str(currentCost) + ", Origin: " + str(origin))
        qtyToAdd = getNaturalNumber("Enter quantity to add:")
        if qtyToAdd > 999:
            print("Cannot Add Quantity above 999")
        else:

            newCostPrice = getNaturalNumber("Enter new cost price per item for this batch:")
            # Adding item details to restock list
            restockList.append({"id": productId, "name": name, "brand": brand, "qty": qtyToAdd, "cost": newCostPrice, "origin": origin})
            print(str(qtyToAdd) + " " + name + " marked for restock.")
            # Update stock and price only in memory for  display 
            try:
                productDataDict[productId][2] = currentStock + qtyToAdd 
                productDataDict[productId][3] = newCostPrice # Update cost price as well
            except Exception as e:
                print("Error temporarily updating stock/price in memory for display for ID " + str(productId) + ": " + str(e))

        # Asking if user wants to add another product to this restock order
        if not askToContinue("Add another product to this restock order?"):
            break # Exiting loop to finalize restock

    # Finalizing Restock
    if not restockList: # Checking if any items were added
        print("\nNothing selected to restock. Restock operation cancelled.") 
        return

    # Generating invoice filename including supplier name
    invoiceFileName = generateInvoiceName("RESTOCK", supplierName) 
    # Initializing invoice lines
    invoiceLines = ["--- WeCare Restock Invoice ---", "Supplier: " + supplierName, "Phone: " + supplierPhone,"Date: " + str(datetime.now()), "-"*50]
    grandTotalCost = 0

    # Processing restock list for invoice and updating dictionary
    for item in restockList:
        itemTotal = item["qty"] * item["cost"]
        grandTotalCost += itemTotal
        invoiceLine = (item["name"] + " (" + item["brand"] + ") - Qty: " + str(item["qty"]) + " X " + str(item["cost"]) + " = " + str(itemTotal))
        invoiceLines.append(invoiceLine)

    # Extending invoice lines with footer
    invoiceLines.extend(["-"*50, "Total Restock Cost: Nrs " + str(grandTotalCost), "-"*50])
    
    # Writing invoice to file and displaying in terminal
    if writeInvoice(invoiceFileName, invoiceLines):
        print("\nInvoice Details (Printed to Terminal) ---")
        for line_to_print in invoiceLines: print(line_to_print)
        print("---------------------------------------------")
        # Writing updated inventory to file
        if not writeProductsToFile(productFileName, productDataDict):
            print("Warning: Invoice generated & displayed, but inventory file update failed!")
    else:
        print("Warning: Invoice writing failed. Inventory file not updated.")