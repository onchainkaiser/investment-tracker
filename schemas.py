from pydantic import BaseModel, EmailStr
from typing import Optional

class CreateInvestment(BaseModel):
    asset_name : str
    amount_invested : float
    current_value : float
    chain_name : str
    currency : str

class UpdateInvestment(BaseModel):
    amount_invested : Optional[float] = None    
    current_value : Optional[float] = None
    chain_name : Optional[str] = None
    currency : Optional[str] = None
    
class Usercreate(BaseModel):
    username:str
    email: EmailStr
    password:str

class Userlogin(BaseModel):
    email: EmailStr
    password: str