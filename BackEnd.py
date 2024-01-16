print('Welcome to Jok car park')

import string
import datetime
import csv
import random

class Carpark:
    # Initializing the car park with the total number of spaces and the hourly rate.
    def __init__(self, total_spaces, hourly_rate):
        self.total_spaces = total_spaces
        self.available_spaces = total_spaces
        self.hourly_rate = hourly_rate
        self.records = {}
        self.available_parking_spaces = list(range(1, total_spaces + 1))  # Creating a new list for available parking spaces
        # Loading any exisitng records from the CSV file.
        self.load_records() 
        
    # Generating a random ticket number consisting of uppercase letters and digits.    
    def generate_ticket_number(self):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))

    # Handling a vehicle entering the car park
    def enter_car_park(self):
        if self.available_spaces > 0:
            reg_number = input('Enter vehicle registration number(Uppercases and/or numbers): ')
            # Checking if the registration number consists of only uppercases and/or numbers
            if not reg_number.isalnum() or not reg_number.isupper():
                print('\n')
                print(f'Oops! The registration number "{reg_number}" is invalid. It should consist of uppercase letters and/or numbers.')
                return
    
            for ticket_number, record in self.records.items():
                if record['registration_number'] == reg_number and record.get('status') != 'exited':
                    print('\n')
                    print(f'Oops! Vehicle with registration number "{reg_number}" is already parked.')
                    return
    
            entry_time = datetime.datetime.now()
    
            while True:
                # Randomly generating a parking space number with the range of total spaces
                parking_space = random.randint(1, self.total_spaces)
                if parking_space in self.available_parking_spaces:
                    break
    
            # Removing the assigned parking space from the list
            self.available_parking_spaces.remove(parking_space)
            # Generating a unique ticket number for the new parking session.
            ticket_number = self.generate_ticket_number()

            # Recording the parking session details in the records dictionary.
            self.records[ticket_number] = {
                'registration_number': reg_number,
                'entry_time': entry_time,
                'parking_space': parking_space,
                'status': 'parked'
            }
            # Reducing the count of available spaces as one is now occupied.
            self.available_spaces -= 1

            # Displaying the details of the parking session to the console.            
            print('\n')
            print(f'The vehicle is safely parked.')
            print(f'Entry time : {entry_time}')
            print(f'Vehicle registration: {reg_number}')
            print(f'Your ticket number is: {ticket_number}')
            print(f'Parking space: {parking_space}\n')
            print(f'Remaining spaces: {self.available_spaces}/{self.total_spaces}')
        else:
            # Display when there are no available spaces.
            print('\n')
            print('Oops! We are full.')

        # Saving the updated records, including the new parking session.
        self.save_records()

    # Handling a vehicle exiting the car park
    def exit_car_park(self):
        # Prompting for vehicle registration number
        reg_number = input('Enter vehicle registration number: ')

        # Iterating through parking records to find the reg_number    
        for ticket_number, record in self.records.items():
            if record['registration_number'] == reg_number and record.get('status') != 'exited':
                exit_time = datetime.datetime.now()
                record['exit_time']= exit_time
                entry_time = record['entry_time']

                # Calculating the duration of the parking and the hourly rate fee
                duration = (exit_time - entry_time).total_seconds() / 3600
                parking_fee = round(duration * self.hourly_rate, 2)
                record['parking_fee']= parking_fee

                # Marking the parking record as exited
                record['status'] = 'exited'

                # Making the parking space available again
                parking_space = record.get('parking_space', None)
                if parking_space is not None and parking_space not in self.available_parking_spaces:
                    self.available_parking_spaces.append(parking_space)  # Adding the parking_space back to the list
                    self.available_spaces += 1

                # Updating the record with exit time and parking fee
                self.records[ticket_number].update({'exit_time':exit_time, 'parking_fee':parking_fee, 'status': 'exited'})

                # Printing out the parking details
                print('\n')
                print(f'Registration Number: {reg_number}')
                print(f'Parking space: {parking_space}')
                print(f'Parking Fee: £{parking_fee}')
                print(f'Entry Time: {entry_time}')
                print(f'Exit Time: {exit_time}\n')
                print(f'We hope you enjoyed your stay. Please exit within 15 minutes.\n')
                print(f'Remaining spaces: {self.available_spaces}/{self.total_spaces}')
                # Saving the updated records
                self.save_records()
                return

        else:
            # Feedback when registration number is not found in the records
            print('\n')
            print(f'Oops! Registration number "{reg_number}" is not found.')

    # Saving the records to a CSV file.
    def save_records(self):
        # Opening the CSV in write mode ('w'), inorder to overwrite any existing file with the same name
        with open("parking_records.csv", mode='w', newline='') as file:
            writer = csv.writer(file)

            # Writing the header row in the CSV file.
            writer.writerow(["Ticket Number", "Registration Number", "Entry Time", 'Exit Time', 'Parking Fee', 'Parking Space', 'Status'])

            # Iterating over each record in the car park records dictionary
            for ticket_number, record in self.records.items():
                
                # Fetch each piece of information from the record,
                exit_time = record.get('exit_time', '')
                parking_fee = record.get('parking_fee', '')
                status = record.get('status', '')

                # Converting datetime objects to ISO format strings for consistent storage.
                writer.writerow([
                    ticket_number,
                    record['registration_number'],
                    record['entry_time'].isoformat(),
                    exit_time.isoformat() if exit_time else '',
                    parking_fee if parking_fee else '',
                    record.get('parking_space', ''),
                    status
                ])

    # Loading the records from a CSV file.
    def load_records(self):
        try:
            # Opening the CSV file for reading
            with open('parking_records.csv', mode='r') as file:
                reader = csv.reader(file)
                next(reader)

                # Iterating through each row in the CSV file
                for row in reader:

                    # Ensuring each row has 7 elements,adding empty string where necessary
                    row.extend([''] * (7 - len(row)))
                    ticket_number, registration_number, entry_time, exit_time, parking_fee, parking_space, status = row

                    try:
                        # Converting parking_space to an integer if it's not empty, else setting to None
                        parking_space = int(parking_space) if parking_space else None
                    except ValueError:
                        # Handling an invalid parking_space value
                        parking_space = None

                    # Storing the record in the self.records dictionary
                    self.records[ticket_number] = {
                        'registration_number': registration_number,
                        'entry_time': datetime.datetime.fromisoformat(entry_time),
                        'exit_time': datetime.datetime.fromisoformat(exit_time) if exit_time else None,
                        'parking_fee': float(parking_fee) if parking_fee else None,
                        'parking_space': parking_space,
                        'status': status
                    }

                    # Checking if the parking space is currently occupied and update accordingly
                    if status != 'exited' and parking_space is not None:
                        if parking_space in self.available_parking_spaces:
                            self.available_parking_spaces.remove(parking_space)
                        self.available_spaces -= 1 # Reducing the count of available spaces by 1

        except FileNotFoundError:
            pass


    def view_available_spaces(self):
        # Printing the number of available parking spaces in the car park
        print(f'Number of available parking spaces: {self.available_spaces}/{self.total_spaces}')

    # Querying parking records with a ticket number
    def query_parking_record(self, ticket_number):
        try:
            # Checking if the input is a string and meets the format requirements for a ticket number
            if not isinstance(ticket_number, str):
                raise ValueError("Oops! Invalid Ticket.")
            if len(ticket_number) != 4 or not all(char in string.ascii_uppercase + string.digits for char in ticket_number):
                raise ValueError("Oops! Invalid Ticket.")

            #Printing ticket details if the ticket number is valid and exists in the records
            if ticket_number in self.records:
                record = self.records[ticket_number]

                #Printing the vehicle details as in the records via ticket number
                print('\n')
                print(f'Ticket Number: {ticket_number}')
                print(f"Registration Number: {record['registration_number']}")
                print(f"Entry Time: {record['entry_time']}")
            
                if 'exit_time' in record and record['exit_time']:
                    print(f"Exit Time: {record['exit_time']}")
                if 'parking_fee' in record and record['parking_fee']:
                    print(f"Parking Fee: £{record['parking_fee']}")
            else:
                print('\n')
                print('Oops! Ticket not found.')
        except ValueError as e:
            # Handle any ValueError that arises and print the error message
            print(f'Error: {e}')
