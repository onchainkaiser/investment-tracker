from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from database import engine, SessionLocal
from models import Investment, Base
from schemas import CreateInvestment, UpdateInvestment

app = FastAPI(title="Investment Tracker API")

Base.metadata.create_all(bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/investments")
def add_investment(investment: CreateInvestment, db: Session = Depends(get_db)):
    new_investment = Investment(
        asset_name=investment.asset_name,
        amount_invested=investment.amount_invested,
        current_value=investment.current_value,
        chain_name=investment.chain_name,
        currency=investment.currency
    )
    db.add(new_investment)
    db.commit()
    db.refresh(new_investment)
    return {"message": "Investment added successfully", "id": new_investment.id}


@app.get("/investments")
def get_investments(db: Session = Depends(get_db)):
    all_investments = db.query(Investment).all()
    return all_investments


@app.get("/investment/{investment_id}")
def get_investment_by_id(investment_id: str, db: Session = Depends(get_db)):
    investment = db.query(Investment).filter(Investment.id == investment_id).first()
    if not investment:
        raise HTTPException(status_code=404, detail="Investment not found")
    return investment


@app.delete("/investments/{investment_id}")
def delete_investment(investment_id: str, db: Session = Depends(get_db)):
    investment = db.query(Investment).filter(Investment.id == investment_id).first()
    if not investment:
        raise HTTPException(status_code=404, detail="Investment not found")
    db.delete(investment)
    db.commit()
    return {"message": "Investment deleted successfully"}


@app.put("/investments/{investment_id}")
def update_investment(investment_id: str, updated_data: UpdateInvestment, db: Session = Depends(get_db)):
    investment = db.query(Investment).filter(Investment.id == investment_id).first()
    if not investment:
        raise HTTPException(status_code=404, detail="Investment not found")

    if updated_data.amount_invested is not None:
        investment.amount_invested = updated_data.amount_invested
    if updated_data.current_value is not None:
        investment.current_value = updated_data.current_value
    if updated_data.chain_name is not None:
        investment.chain_name = updated_data.chain_name
    if updated_data.currency is not None:
        investment.currency = updated_data.currency

    db.commit()
    db.refresh(investment)
    return {"message": "Investment successfully updated", "investment": investment}


@app.get("/investment/{investment_id}/roi")
def calculate_roi(investment_id: str, db: Session = Depends(get_db)):
    investment = db.query(Investment).filter(Investment.id == investment_id).first()
    if not investment:
        raise HTTPException(status_code=404, detail="Investment not found")

    roi = ((investment.current_value - investment.amount_invested) / investment.amount_invested) * 100
    return {
        "asset_name": investment.asset_name,
        "amount_invested": investment.amount_invested,
        "current_value": investment.current_value,
        "roi_percentage": round(roi, 2)
    }
