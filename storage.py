import os
from models import User, Plan, Rental

# Handles file-based data persistence (saving/loading)
class Storage:
    def __init__(self):
        self.users_file = "users.txt"
        self.admins_file = "admins.txt"
        self.plans_file = "plans.txt"
        self.rentals_file = "rentals.txt"

    # Reads standard users from text file
    def load_users(self):
        users = {}
        if os.path.exists(self.users_file):
            with open(self.users_file, 'r') as f:
                for line in f:
                    parts = line.strip().split('|')
                    if len(parts) == 4 and parts[3] == "user":
                        users[parts[0]] = User(parts[0], parts[1], parts[2], parts[3])
        return users

    # Writes user dictionaries to text file
    def save_users(self, users_dict):
        with open(self.users_file, 'w') as f:
            for user in users_dict.values():
                f.write(user.to_string() + "\n")

    # Reads admin accounts from text file
    def load_admins(self):
        admins = {}
        if os.path.exists(self.admins_file):
            with open(self.admins_file, 'r') as f:
                for line in f:
                    parts = line.strip().split('|')
                    if len(parts) == 4 and parts[3] == "admin":
                        admins[parts[0]] = User(parts[0], parts[1], parts[2], parts[3])
        return admins

    # Writes admin accounts to text file
    def save_admins(self, admins_dict):
        with open(self.admins_file, 'w') as f:
            for admin in admins_dict.values():
                f.write(admin.to_string() + "\n")

    # Loads plans or creates defaults if none exist
    def load_plans(self):
        plans = {}
        if os.path.exists(self.plans_file):
            with open(self.plans_file, 'r') as f:
                for line in f:
                    parts = line.strip().split('|')
                    if len(parts) == 4:
                        plans[parts[0]] = Plan(parts[0], parts[1], parts[2], parts[3])
        else:
            # Default fallback plans
            plans["1"] = Plan("1", "Dirt Tier", "2GB RAM (Vanilla/Bedrock)", 5.0)
            plans["2"] = Plan("2", "Iron Tier", "4GB RAM (Paper/Spigot - Plugins)", 15.0)
            plans["3"] = Plan("3", "Diamond Tier", "8GB RAM (Forge/Fabric - Modpacks)", 30.0)
            self.save_plans(plans)
        return plans

    # Writes current plans to text file
    def save_plans(self, plans_dict):
        with open(self.plans_file, 'w') as f:
            for plan in plans_dict.values():
                f.write(plan.to_string() + "\n")

    # Parses rental properties mapping to their respective attributes
    def load_rentals(self):
        rentals = []
        if os.path.exists(self.rentals_file):
            with open(self.rentals_file, 'r') as f:
                for line in f:
                    parts = line.strip().split('|')
                    if len(parts) >= 6:
                        status = parts[5]
                        motd = parts[6] if len(parts) > 6 else "A Minecraft Server"
                        gamemode = parts[7] if len(parts) > 7 else "survival"
                        difficulty = parts[8] if len(parts) > 8 else "normal"
                        pvp = parts[9] if len(parts) > 9 else "true"
                        max_players = parts[10] if len(parts) > 10 else "20"
                        
                        rentals.append(Rental(parts[0], parts[1], parts[2], parts[3], parts[4], status, motd, gamemode, difficulty, pvp, max_players))
        return rentals

    # Writes active/cancelled server rentals to text file
    def save_rentals(self, rentals_list):
        with open(self.rentals_file, 'w') as f:
            for rental in rentals_list:
                f.write(rental.to_string() + "\n")