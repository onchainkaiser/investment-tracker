import uuid
from datetime import datetime

class Investment:
    def __init__(self, asset_name, amount_invested, current_value, chain_name, currency):
        self.id = str(uuid.uuid4())
        self.asset_name = asset_name
        self.amount_invested = amount_invested
        self.current_value = current_value
        self.chain_name = chain_name
        self.currency = currency
        self.date_invested = datetime.now()