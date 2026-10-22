import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Dedicated portal for platform administrators to manage the application
class AdminPortal:
    def __init__(self, app_instance):
        self.app = app_instance

    # Main admin navigation loop
    def menu(self):
        # Enforces access control via role checking
        while self.app.current_user and self.app.current_user.role == "admin":
            print("\n========================================")
            print(" Admin Dashboard ")
            print("========================================")
            print("  1. View All Users")
            print("  2. View All Hosted Servers")
            print("  3. View Hosting Plans")
            print("  4. Add New Plan")
            print("  5. Remove Plan")
            print("  6. Logout")
            
            choice = input("\nSelect an option > ")
            clear_screen()
            
            if choice == '1':
                self.view_users()
            elif choice == '2':
                self.view_rentals()
            elif choice == '3':
                self.view_plans()
            elif choice == '4':
                self.add_plan()
            elif choice == '5':
                self.remove_plan()
            elif choice == '6':
                self.app.save_all_data()
                self.app.current_user = None
                print("Admin logged out successfully.")
            else:
                print("Invalid option.")

    # Iterates and displays all standard users and their balances
    def view_users(self):
        print("\n--- Registered Users ---")
        if not self.app.users:
            print("No regular users registered yet.")
        for u in self.app.users.values():
            print(f"• {u.username} | Balance: ${u.balance:.2f}")

    # Iterates and lists globally hosted rentals
    def view_rentals(self):
        print("\n--- Global Hosted Minecraft Servers ---")
        if not self.app.rentals:
            print("No servers are currently hosted in the system.")
            return
            
        for r in self.app.rentals:
            print(f"• {r.username} | {r.server_name} ({r.plan_name}) | {r.duration_months}mo | [{r.status}]")

    # Displays existing server hosting tiers
    def view_plans(self):
        print("\n--- Available Minecraft Hosting Plans ---")
        if not self.app.plans:
            print("No plans available currently.")
            return
            
        print(f"{'ID':<4} | {'Name':<15} | {'Specs':<35} | {'Price/mo'}")
        print("-" * 75)
        for plan in self.app.plans.values():
            print(f"{plan.plan_id:<4} | {plan.name:<15} | {plan.specs:<35} | ${plan.price:.2f}")

    # Flow to create and push a new hosting tier to storage
    def add_plan(self):
        print("\n--- Add New Hosting Plan ---")
        from models import Plan
        while True:
            plan_id = input("Enter new Plan ID (e.g., 4) or 'exit' to cancel: ")
            if plan_id.lower() == 'exit':
                print("Returning to dashboard...")
                break

            if plan_id in self.app.plans:
                print("Plan ID already exists. Try again.")
                continue
                
            name = input("Enter tier name (e.g., Nether Tier): ").replace("|", "")
            specs = input("Enter specs (e.g., 16GB RAM, Unlimited Slots): ").replace("|", "")
            
            try:
                price = float(input("Enter monthly price: $"))
            except ValueError:
                print("Invalid price format. Please try again from the beginning.")
                continue
                
            new_plan = Plan(plan_id, name, specs, price)
            self.app.plans[plan_id] = new_plan
            self.app.storage.save_plans(self.app.plans)
            print("New Minecraft plan added successfully.")
            break 

    # Removes an existing hosting tier based on its ID
    def remove_plan(self):
        self.view_plans()
        while True:
            plan_id = input("\nEnter Plan ID to remove (or 'exit' to cancel): ")
            if plan_id.lower() == 'exit':
                break
            
            if plan_id in self.app.plans:
                del self.app.plans[plan_id]
                self.app.storage.save_plans(self.app.plans)
                print("Plan removed successfully.")
                break
            else:
                print("Plan ID not found. Try again.")