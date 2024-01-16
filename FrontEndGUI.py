# Importing necessary modules for the GUI application
from tkinter import messagebox, simpledialog, Text,Scrollbar
import tkinter as tk
from carpark import *

# GUI Implementation
class CarparkGUI:
    def __init__(self, master, carpark):
        # Initializing the GUI with a master window and a Carpark object
        self.master = master
        self.carpark = carpark
        master.title("Jok Car Park")

        # Creating and placing buttons on the GUI
        tk.Button(master, text="Enter Car Park", command=self.enter_car_park).pack(pady=10)
        tk.Button(master, text="Exit Car Park", command=self.exit_car_park).pack(pady=10)
        tk.Button(master, text="View Available Spaces", command=self.view_available_spaces).pack(pady=10)
        tk.Button(master, text="Query Parking Record", command=self.query_parking_record).pack(pady=10)
        tk.Button(master, text="Quit", command=self.quit_application).pack(pady=10)

        # Setting up the protocol for window close event
        master.protocol("WM_DELETE_WINDOW", self.quit_application)

        # Setting up the output display box for actions
        self.action_output_box = Text(master, height=15, width=70, bg='black', fg='cyan')
        self.action_output_box.pack(pady=10)
        scrollbar = Scrollbar(master, command=self.action_output_box.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.action_output_box.config(yscrollcommand=scrollbar.set)
    
    def display_action_message(self, message):
        # isplaying a message in the output box
        self.action_output_box.insert(tk.END, message + '\n\n')
        self.action_output_box.see(tk.END)  # Function for auto-scroll to the end
        
    def generate_ticket_number(self):
        # Generating a random ticket number
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    
    def enter_car_park(self):
        # Handling vehicle entry into the car park
        reg_number = simpledialog.askstring("Enter Car Park", "Enter vehicle registration number:", parent=self.master)

        # Checking if the reg_number is None (dialog closed/ cancelled) and exit if no input is provided
        if reg_number is None:
            self.display_action_message('Car park entry cancelled.')
            return

        # Checking if the registration number is valid
        if not reg_number.isalnum() or not reg_number.isupper():
            messagebox.showinfo('Invalid Input', 'Registration number invalid. Please use uppercase letters and/or numbers.')
            return

        # Checking if the vehicle is already parked
        for ticket_number, record in self.carpark.records.items():
            if record['registration_number'] == reg_number and record.get('status') != 'exited':
                messagebox.showinfo('Already Parked', f'Vehicle with registration number "{reg_number}" is already parked.')
                return

        # Proceeding if there are available spaces
        if self.carpark.available_spaces > 0:
            entry_time = datetime.datetime.now()

            # Looping until an available parking space is found and randomly selecting a parking space
            while True:
                parking_space = random.randint(1, self.carpark.total_spaces)
                if parking_space in self.carpark.available_parking_spaces:
                    break

            # Removing the chosen parking space from the list of available spaces
            self.carpark.available_parking_spaces.remove(parking_space)
            ticket_number = self.generate_ticket_number()
            # Recording the vehicle's details in the car park records
            self.carpark.records[ticket_number] = {
                'registration_number': reg_number,
                'entry_time': entry_time,
                'parking_space': parking_space,
                'status': 'parked'
            }
            self.carpark.available_spaces -= 1 # Decreasing the count of available parking spaces by one

            self.carpark.save_records()  # Saving updated records

            # Displaying the entry information in the GUI
            text = (
                f'The vehicle is safely parked.\n'
                f'Entry time: {entry_time}\n'
                f'Vehicle registration: {reg_number}\n'
                f'Your ticket number is: {ticket_number}\n'
                f'Parking space: {parking_space}\n'
                f'Remaining spaces: {self.carpark.available_spaces}/{self.carpark.total_spaces}'
            )
            self.display_action_message(text) # Displaying the message in the GUI's output box
        else:
            # Showing a message box when there are no available parking spaces
            messagebox.showinfo('Oops! We are full.')

    def exit_car_park(self):
        # Function for handling vehicle exit from the car park
        reg_number = simpledialog.askstring("Exit Car Park", "Enter vehicle registration number:", parent=self.master)

        # Checking if dialog box was cancelled and reg_number is None
        if reg_number is None:
            return
        
        found = False # Initializind a flag to track if the vehicle is found in the car park

        for ticket_number, record in self.carpark.records.items():
            # Checking if the current record matches the registration number and the vehicle hasn't exited yet
            if record['registration_number'] == reg_number and record.get('status') != 'exited':
                found = True # Setting the flag to True as the vehicle is found
                exit_time = datetime.datetime.now()
                entry_time = record['entry_time']
                
                # Calculating parking duration and fee
                duration = (exit_time - entry_time).total_seconds() / 3600
                parking_fee = round(duration * self.carpark.hourly_rate, 2)

                # Updating the record with exit time, parking fee, and status
                record['exit_time'] = exit_time
                record['parking_fee'] = parking_fee
                record['status'] = 'exited'

                # Freeing up the parking space and update available spaces
                parking_space = record.get('parking_space', None)
                if parking_space is not None:
                    self.carpark.available_parking_spaces.append(parking_space)
                self.carpark.available_spaces += 1

                # Updating the car park records and save to CSV file
                self.carpark.records[ticket_number].update({'exit_time': exit_time, 'parking_fee': parking_fee, 'status': 'exited'})
                self.carpark.save_records()

                # Displaying the exit information in the GUI
                text = (f'Registration Number: {reg_number}\n'
                    f'Parking space: {parking_space}\n'
                    f'Parking Fee: £{parking_fee}\n'
                    f'Entry Time: {entry_time}\n'
                    f'Exit Time: {exit_time}\n'
                    f'Remaining spaces: {self.carpark.available_spaces}/{self.carpark.total_spaces}')
                self.display_action_message(text)
                break  # Exiting the loop when the vehicle is processed

        # Display message when the vehicle reg_number is not found in the records
        if not found and reg_number is not None:
            self.display_action_message(f'Oops! Registration number "{reg_number}" is not found.')

    def view_available_spaces(self):
        # Displaying the number of available parking spaces
        available_spaces = self.carpark.available_spaces
        total_spaces = self.carpark.total_spaces
        self.display_action_message(f'Number of available parking spaces: {available_spaces}/{total_spaces}')

    def query_parking_record(self):
        # Function for querying and displaying a parking record based on ticket number
        ticket_number = simpledialog.askstring("Query Parking Record", "Enter the ticket number:", parent=self.master)
        if ticket_number:
            # Stripping and converting the ticket number to uppercase to standardize the format
            ticket_number = ticket_number.strip().upper()

            found = False # Initializing a flag to track whether the ticket number is found in records 

            # Iterating over the records to find a match for the given ticket number
            for tn, record in self.carpark.records.items():
                if tn == ticket_number:
                    found = True # Setting the flag to True when a matching record is found

                    # Preparing a message with the details of the parking record
                    message = (
                        f"Ticket Number: {ticket_number}\n"
                        f"Registration Number: {record['registration_number']}\n"
                        f"Entry Time: {record['entry_time']}\n"
                        f"Parking Space: {record.get('parking_space')}\n"
                        f"Status: {record.get('status')}\n"
                        f"Exit Time: {record.get('exit_time', 'N/A')}\n"
                        f"Parking Fee: £{record.get('parking_fee', 'N/A')}\n"
                    )
                    break # Exiting the loop after finding the record

            # Handling the case where the ticket number is not found in records
            if not found:
                message = f"No record found for ticket number: {ticket_number}"
            self.display_action_message(message) # Displaying the result message in the GUI
        else:
            # Handling the case where no ticket number was entered
            self.display_action_message("No ticket number entered.")



    def quit_application(self):
        # Function to handle application quit
        self.carpark.save_records()
        self.master.destroy()

# The GUI execution block
if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('600x400')
    carpark_app = Carpark(total_spaces=6, hourly_rate=2)
    gui = CarparkGUI(root, carpark_app)
    root.protocol('WM_DELETE_WINDOW', gui.quit_application)
    root.mainloop()

