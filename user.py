import os
from models import Rental

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Interface for standard users to manage their servers and wallet
class UserPortal:
    def __init__(self, app_instance):
        self.app = app_instance

    # Main user dashboard loop
    def menu(self):
        while self.app.current_user:
            print("\n========================================")
            print(f" Minecrafter Portal: {self.app.current_user.username}")
            print("========================================")
            print(f"  Wallet Balance: ${self.app.current_user.balance:.2f}\n")
            print("  1. View Hosting Plans")
            print("  2. Deploy New Server")
            print("  3. View My Servers")
            print("  4. Renew Server")
            print("  5. Configure server.properties")
            print("  6. Cancel Server")
            print("  7. Add Funds")
            print("  8. Logout")
            
            choice = input("\nSelect an option > ")
            clear_screen()
            
            if choice == '1':
                self.view_plans()
            elif choice == '2':
                self.rent_server()
            elif choice == '3':
                self.view_current_rentals()
            elif choice == '4':
                self.renew_rentals()
            elif choice == '5':
                self.configure_properties()
            elif choice == '6':
                self.cancel_rentals()
            elif choice == '7':
                self.add_funds()
            elif choice == '8':
                self.app.save_all_data()
                self.app.current_user = None
                print("Logged out successfully.")
            else:
                print("Invalid option.")

    # Displays available tiers and their prices
    def view_plans(self):
        print("\n--- Available Minecraft Hosting Plans ---")
        if not self.app.plans:
            print("No plans available currently.")
            return
            
        print(f"{'ID':<4} | {'Name':<15} | {'Specs':<35} | {'Price/mo'}")
        print("-" * 75)
        for plan in self.app.plans.values():
            print(f"{plan.plan_id:<4} | {plan.name:<15} | {plan.specs:<35} | ${plan.price:.2f}")

    # Flow for purchasing and provisioning a new server
    def rent_server(self):
        while True:
            self.view_plans()
            print("\n[Note: Type 'exit' at any prompt to cancel and return to the menu]")
            plan_id = input("Select plan ID to deploy: ")
            
            if plan_id.lower() == 'exit':
                print("Returning to dashboard...")
                break

            if plan_id not in self.app.plans:
                print("Invalid plan ID. Please try again.")
                continue
            
            # EULA compliance requirement
            print("\n--- EULA Agreement ---")
            eula_check = input("Do you accept the End User License Agreement (EULA) from Mojang and the Server Provider? (y/n): ")
            if eula_check.lower() == 'exit': break
            if eula_check.lower() != 'y':
                print("You must accept the EULA to deploy a server. Returning to menu...")
                break

            server_name = input("\nEnter your Minecraft Server Name: ").replace("|", "-")
            if server_name.lower() == 'exit': break

            # Software selection mapping
            print("\n#Options:")
            print("[1] -- Java")
            print("[2] -- Fabric")
            print("[3] -- Forge")
            print("[4] -- Bedrock")
            print("[5] -- Paper")
            
            option_map = {"1": "Java", "2": "Fabric", "3": "Forge", "4": "Bedrock", "5": "Paper"}
            type_choice = input("Select an option: ")
            if type_choice.lower() == 'exit': break
            
            if type_choice not in option_map:
                print("Invalid software option chosen. Aborting...")
                continue
                
            software = option_map[type_choice]
            specific_version = input(f"Enter Version of ({software}): ").replace("|", "-")
            if specific_version.lower() == 'exit': break
            
            version = f"{software} {specific_version}"

            # Rent duration input
            try:
                duration_input = input("Enter duration in months: ")
                if duration_input.lower() == 'exit': break
                duration = int(duration_input)
                if duration <= 0:
                    print("Duration must be at least 1 month.")
                    continue
            except ValueError:
                print("Invalid number of months. Please enter a number.")
                continue

            selected_plan = self.app.plans[plan_id]
            total_cost = selected_plan.price * duration
            
            print(f"\nTotal Cost: ${total_cost:.2f}")
            
            # Finalize transaction if user has sufficient funds
            if self.app.current_user.balance >= total_cost:
                confirm = input("Confirm payment to provision server? (y/n): ").lower()
                if confirm == 'exit': break
                if confirm == 'y':
                    self.app.current_user.balance -= total_cost
                    
                    print("\n--- Initial Server Properties Setup ---")
                    
                    # Gather baseline server properties upon creation
                    motd = input("Enter server MOTD (Message of the Day): ")
                    if motd.lower() == 'exit': break
                    
                    while True:
                        gamemode = input("Enter default gamemode (survival/creative/adventure/spectator): ").lower()
                        if gamemode in ['exit', 'survival', 'creative', 'adventure', 'spectator']:
                            break
                        print("Error: Invalid gamemode. Must be survival, creative, adventure, or spectator.")
                    if gamemode == 'exit': break
                    
                    while True:
                        difficulty = input("Enter difficulty (peaceful/easy/normal/hard): ").lower()
                        if difficulty in ['exit', 'peaceful', 'easy', 'normal', 'hard']:
                            break
                        print("Error: Invalid difficulty. Must be peaceful, easy, normal, or hard.")
                    if difficulty == 'exit': break
                    
                    while True:
                        pvp = input("Enable PvP? (true/false): ").lower()
                        if pvp in ['exit', 'true', 'false']:
                            break
                        print("Error: Invalid input. Must be true or false.")
                    if pvp == 'exit': break
                    
                    while True:
                        max_players = input("Enter max-players (e.g., 20): ")
                        if max_players.lower() == 'exit':
                            break
                        if max_players.isdigit() and int(max_players) > 0:
                            break
                        print("Error: Invalid input. Must be a positive integer.")
                    if max_players.lower() == 'exit': break

                    # Append new rental to storage
                    new_rental = Rental(self.app.current_user.username, server_name, version, selected_plan.name, duration, "Active", motd, gamemode, difficulty, pvp, max_players)
                    self.app.rentals.append(new_rental)
                    
                    self.app.save_all_data()
                    print("\nMinecraft Server deployed successfully!.")
                    break 
                else:
                    print("Transaction cancelled. You can try again.")
            else:
                print(f"Insufficient balance. You need ${total_cost:.2f}. Please choose a different plan or duration.")

    # Helper method to print the user's active servers
    def _display_active_rentals(self):
        print("\n--- Your Active Minecraft Servers ---")
        user_rentals = [r for r in self.app.rentals if r.username == self.app.current_user.username and r.status == "Active"]
        
        if not user_rentals:
            print("No active servers found. Time to deploy one!")
            return user_rentals

        for idx, r in enumerate(user_rentals):
            print(f"[{idx}] {r.server_name} ({r.version}) | Tier: {r.plan_name} | {r.duration_months} months remaining")
        return user_rentals

    # Shows detailed configuration parameters of a specific server
    def view_current_rentals(self):
        active_rentals = self._display_active_rentals()
        if not active_rentals:
            return

        print("\n[Note: Type 'exit' to return to the menu]")
        while True:
            choice_input = input("\nEnter server ID (index) to view full information: ")
            if choice_input.lower() == 'exit':
                break
                
            try:
                choice = int(choice_input)
                if 0 <= choice < len(active_rentals):
                    server = active_rentals[choice]
                    print("\n--- Full Server Details ---")
                    print(f"Server Name:  {server.server_name}")
                    print(f"Version:      {server.version}")
                    print(f"Plan Tier:    {server.plan_name}")
                    print(f"Time Left:    {server.duration_months} months")
                    print(f"Status:       {server.status}")
                    print("\n--- server.properties ---")
                    print(f"MOTD:         {server.motd}")
                    print(f"Gamemode:     {server.gamemode}")
                    print(f"Difficulty:   {server.difficulty}")
                    print(f"PvP Enabled:  {server.pvp}")
                    print(f"Max Players:  {server.max_players}")
                else:
                    print("Invalid Server ID. Try again.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")

    # Allows editing active server properties
    def configure_properties(self):
        print("\n--- Configure Server Properties ---")
        active_rentals = self._display_active_rentals()
        if not active_rentals:
            return

        print("\n[Note: Type 'exit' at any prompt to cancel and return to the menu]")
        try:
            choice_input = input("Select server index to configure: ")
            if choice_input.lower() == 'exit':
                return
                
            choice = int(choice_input)
            if 0 <= choice < len(active_rentals):
                server = active_rentals[choice]
                print(f"\nEditing server.properties for {server.server_name}...")
                print("(Press Enter to keep the current value)")
                
                # Input prompts allowing fallback to current values
                motd = input(f"Enter server MOTD [{server.motd}]: ")
                if motd.lower() == 'exit': return
                if motd: server.motd = motd
                
                while True:
                    gamemode = input(f"Enter default gamemode [{server.gamemode}]: ").lower()
                    if gamemode in ['', 'exit', 'survival', 'creative', 'adventure', 'spectator']:
                        if gamemode and gamemode != 'exit': server.gamemode = gamemode
                        break
                    print("Error: Invalid gamemode. Must be survival, creative, adventure, or spectator.")
                if gamemode == 'exit': return
                
                while True:
                    difficulty = input(f"Enter difficulty [{server.difficulty}]: ").lower()
                    if difficulty in ['', 'exit', 'peaceful', 'easy', 'normal', 'hard']:
                        if difficulty and difficulty != 'exit': server.difficulty = difficulty
                        break
                    print("Error: Invalid difficulty. Must be peaceful, easy, normal, or hard.")
                if difficulty == 'exit': return
                
                while True:
                    pvp = input(f"Enable PvP? [{server.pvp}]: ").lower()
                    if pvp in ['', 'exit', 'true', 'false']:
                        if pvp and pvp != 'exit': server.pvp = pvp
                        break
                    print("Error: Invalid input. Must be true or false.")
                if pvp == 'exit': return
                
                max_players = input(f"Enter max-players [{server.max_players}]: ")
                if max_players.lower() == 'exit': return
                if max_players: server.max_players = max_players
                
                self.app.save_all_data()
                print("\nApplying changes to server.properties file...")
                print("Server requires a restart for changes to take effect.")
                print("server.properties updated successfully!")
            else:
                print("Invalid selection. Try again.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    # Extend time on active server rentals
    def renew_rentals(self):
        while True:
            active_rentals = self._display_active_rentals()
            if not active_rentals:
                break

            print("\n[Note: Type 'exit' at any prompt to return to the menu]")
            try:
                choice_input = input("Select server index to renew: ")
                if choice_input.lower() == 'exit':
                    break

                choice = int(choice_input)
                if 0 <= choice < len(active_rentals):
                    months_input = input("Enter months to add: ")
                    if months_input.lower() == 'exit': break
                    months = int(months_input)

                    if months <= 0:
                        print("Months must be at least 1.")
                        continue

                    # Calculate total based on server's assigned plan tier
                    selected_rental = active_rentals[choice]
                    plan_price = next(plan.price for plan in self.app.plans.values() if plan.name == selected_rental.plan_name)
                    
                    cost = plan_price * months
                    print(f"Renewal Cost: ${cost:.2f}")
                    
                    if self.app.current_user.balance >= cost:
                        self.app.current_user.balance -= cost
                        selected_rental.duration_months += months
                        self.app.save_all_data()
                        print("Server renewed successfully!")
                        break 
                    else:
                        print(f"Insufficient funds. Required: ${cost:.2f}")
                else:
                    print("Invalid selection. Try again.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")

    # Allows users to permanently terminate a server without a refund
    def cancel_rentals(self):
        while True:
            active_rentals = self._display_active_rentals()
            if not active_rentals:
                break

            print("\n[Note: Type 'exit' at any prompt to return to the menu]")
            try:
                choice_input = input("Select server index to cancel/delete: ")
                if choice_input.lower() == 'exit':
                    break
                    
                choice = int(choice_input)
                if 0 <= choice < len(active_rentals):
                    print("Warning: Deleting a server is permanent and no refunds are issued.")
                    confirm = input("Are you sure you want to delete this server? (y/n): ").lower()
                    if confirm == 'exit': break
                    if confirm == 'y':
                        # Soft deletion by changing status
                        active_rentals[choice].status = "Cancelled"
                        self.app.save_all_data()
                        print("Server successfully deleted.")
                        break 
                    else:
                        print("Cancellation aborted. Your world is safe.")
                else:
                    print("Invalid selection. Try again.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")

    # Allows the user to add funds to their wallet balance
    def add_funds(self):
        print("\n--- Add Funds to Wallet ---")
        print(f"Current Balance: ${self.app.current_user.balance:.2f}")
        print("[Note: Type 'exit' to cancel and return to the menu]")
        
        while True:
            amount_input = input("Enter amount to add: $")
            
            if amount_input.lower() == 'exit':
                print("Returning to dashboard...")
                break
                
            try:
                amount = float(amount_input)
                if amount <= 0:
                    print("Error: Amount must be greater than $0.00.")
                    continue
                
                # Add the specified amount to the user's wallet
                self.app.current_user.balance += amount
                
                # Save the updated balance to the backend
                self.app.save_all_data()
                
                print(f"\nSuccess! ${amount:.2f} has been added to your wallet.")
                print(f"New Balance: ${self.app.current_user.balance:.2f}")
                break
                
            except ValueError:
                print("Error: Invalid input. Please enter a valid numerical amount.")