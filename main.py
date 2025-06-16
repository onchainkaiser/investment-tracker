from fastapi import FastAPI
from schemas import CreateInvestment
from schemas import UpdateInvestment
from models import Investment
from fastapi import HTTPException

app = FastAPI(title="Investment Tracker API")

@app.get("/")
def read_root():
    return{"message":"welcome to the investment tracker API"}

investments = []

@app.post ("/investments")
def add_investment(investment: CreateInvestment):
    new_investment = Investment(
        asset_name = investment.asset_name,
        amount_invested= investment.amount_invested,
        current_value = investment.current_value,
        chain_name = investment.chain_name,
        currency = investment.currency

    )

    investments.append(new_investment)
    return {"message":"Investment has been added successfully"}

@app.get("/investments")
def get_investments():
    return [investment.__dict__ for investment in investments]


@app.get("/investment/{invetment_id}")
def get_investment_by_id(investment_id: str):
    for investment in investments:
        if investment.id == investment_id:
            return investment.__dict__
    raise HTTPException(status_code = 404, detail= "investment not found")


@app.delete("/investments/{investment_id}")
def delete_investment(investment_id: str):
    for investment in investments:
        if investment.id == investment_id:
            investments.remove(investment)
            return {"message": "Investment deleted successfully"}
    
    # This only runs if no investment matched
    raise HTTPException(status_code=404, detail="Investment not found")

@app.put("/investments/{investment_id}")
def update_investment(investment_id: str, updated_data: UpdateInvestment):
    for investment in investments:
        if investment.id == investment_id:

            if updated_data.amount_invested is not None:
                investment.amount_invested = updated_data.amount_invested
            if updated_data.current_value is not None:
                investment.current_value = updated_data.current_value
            if updated_data.chain_name is not None:
                investment.chain_name = updated_data.chain_name
            if updated_data.currency is not None:
                investment.currency = updated_data.currency      

            return{"message":"investment successfully updated", "investment":investment.__dict__}

        raise HTTPException(status_code = 404, detail= "investment not found")          
    
@app.get("/investment/{investment_id}/roi")
def calculate_roi(investment_id: str):
    for investment in investments:
        if investment.id == investment_id:
            roi = ((investment.current_value - investment.amount_invested) / investment.amount_invested) * 100
            return {
                "asset_name": investment.asset_name,
                "amount_invested": investment.amount_invested,
                "current_value": investment.current_value,
                "roi_percentage": round(roi,2)

            }

    raise HTTPException(status_code = 404, detail= "investment not found")        