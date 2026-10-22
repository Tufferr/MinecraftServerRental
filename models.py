# Represents an account (either user or admin)
class User:
    def __init__(self, username, password, balance=100.0, role="user"):
        self.username = username
        self.password = password
        self.balance = float(balance)
        self.role = role

    # Formats user data for flat-file storage
    def to_string(self):
        return f"{self.username}|{self.password}|{self.balance}|{self.role}"

# Represents a hosting tier offering
class Plan:
    def __init__(self, plan_id, name, specs, price):
        self.plan_id = str(plan_id)
        self.name = name
        self.specs = specs
        self.price = float(price)

    # Formats plan data for flat-file storage
    def to_string(self):
        return f"{self.plan_id}|{self.name}|{self.specs}|{self.price}"

# Represents a specific user's rented Minecraft server
class Rental:
    def __init__(self, username, server_name, version, plan_name, duration_months, status="Active", motd="A Minecraft Server", gamemode="survival", difficulty="normal", pvp="true", max_players="20"):
        self.username = username
        self.server_name = server_name
        self.version = version
        self.plan_name = plan_name
        self.duration_months = int(duration_months)
        self.status = status
        self.motd = motd
        self.gamemode = gamemode
        self.difficulty = difficulty
        self.pvp = pvp
        self.max_players = max_players

    # Formats rental properties for flat-file storage
    def to_string(self):
        return f"{self.username}|{self.server_name}|{self.version}|{self.plan_name}|{self.duration_months}|{self.status}|{self.motd}|{self.gamemode}|{self.difficulty}|{self.pvp}|{self.max_players}"