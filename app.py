import os
from storage import Storage
from models import User
from admin import AdminPortal
from user import UserPortal

# Clears the console screen based on the OS
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Main application class managing the server portal
class ServerApp:
    def __init__(self):
        # Initialize storage and load all data into memory
        self.storage = Storage()
        self.users = self.storage.load_users()
        self.admins = self.storage.load_admins()
        self.plans = self.storage.load_plans()
        self.rentals = self.storage.load_rentals()
        self.current_user = None

    # Persists current state to text files
    def save_all_data(self):
        self.storage.save_users(self.users)
        self.storage.save_admins(self.admins)
        self.storage.save_rentals(self.rentals)

    # Main execution loop displaying the primary menu
    def run(self):
        clear_screen()
        
        # Trigger first-time setup if no admin exists
        if not self.admins:
            self.onboard_admin()

        while True:
            print("\n========================================")
            print(" Minecraft Server Hosting Portal ")
            print("========================================")
            print("  1. Register")
            print("  2. Login")
            print("  3. Exit")
            
            choice = input("\nSelect an option > ")
            
            if choice == '1':
                self.register()
            elif choice == '2':
                self.login()
            elif choice == '3':
                # Save data and exit program
                self.save_all_data()
                clear_screen()
                print("Thank you for using our Minecraft Hosting. Goodbye!")
                break
            else:
                print("Invalid option. Try again.")

    # Creates the initial master admin account
    def onboard_admin(self):
        print("\n--- First-Time Setup ---")
        print("No admin account detected in the system.")
        print("Please create the master admin account.\n")
        
        username = input("Enter Admin Username: ").lower()
        password = input("Enter Admin Password: ").lower()
        
        new_admin = User(username, password, 0.0, "admin")
        self.admins[username] = new_admin
        self.storage.save_admins(self.admins)
        
        print("Admin account created successfully! You can now log in.\n")

    # Handles new user registration
    def register(self):
        print("\n--- New Minecrafter Registration ---")
        
        username = input("Enter new username: ").lower()
        
        # Ensure username uniqueness
        if username in self.users or username in self.admins:
            print("Username already taken.")
            return
            
        password = input("Enter new password: ").lower()
        
        # Save new user and grant starting balance
        new_user = User(username, password)
        self.users[username] = new_user
        self.storage.save_users(self.users)
        print("Registration successful! You have been granted $100.00 starting balance.")

    # Authenticates users and routes them to the appropriate portal
    def login(self):
        print("\n--- System Login ---")
        
        username = input("Enter username: ").lower()
        password = input("Enter password: ").lower()
        
        # Check standard user credentials
        if username in self.users and self.users[username].password == password:
            self.current_user = self.users[username]
            clear_screen()
            print(f"Welcome back, {username}!")
            user_portal = UserPortal(self)
            user_portal.menu()
            
        # Check admin credentials
        elif username in self.admins and self.admins[username].password == password:
            self.current_user = self.admins[username]
            clear_screen()
            print(f"Welcome Admin, {username}!")
            admin_portal = AdminPortal(self)
            admin_portal.menu()
            
        else:
            print("Invalid credentials.")

if __name__ == "__main__":
    application = ServerApp()
    application.run()