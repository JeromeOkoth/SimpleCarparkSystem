# Importing the Carpark class from the carpark module
from carpark import Carpark

# The main execution block
if __name__ == '__main__':
    
    # Setting up the car park with specified total spaces and hourly rate
    total_spaces = 6  
    hourly_rate = 2 
    car_park = Carpark(total_spaces, hourly_rate)
    
    # Starting an infinite loop to display the menu and handle user input
    while True:
        # Displaying the car park menu
        print('\nCar Park Menu:')
        print('1. Enter the car park')
        print('2. Exit the car park')
        print('3. View available parking spaces')
        print('4. Query parking record by ticket number')
        print('5. Quit')

        # Taking the user's choice as input
        choice = input("Please select an option from the menu: ")

        # Handling the user's choice
        if choice == '1':
            
            # Handling the case where a vehicle enters the car park
            car_park.enter_car_park()
        elif choice == '2':
            
            # Handling the case where a vehicle exits the car park
            car_park.exit_car_park()
        elif choice == '3':
            
            # Displaying the number of available parking spaces
            car_park.view_available_spaces()
        elif choice == '4':
            
            # Querying a parking record by ticket number
            ticket_number = input('Enter the ticket number: ')
            car_park.query_parking_record(ticket_number)
        elif choice == '5':
            
            # Exiting the program
            print('Thank you, see you soon and drive safe.')
            break
        else:
            
            # Handling invalid menu options
            print('Oops! Please select an option from the menu.')
