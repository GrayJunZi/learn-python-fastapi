from typing import Any

from fastapi import FastAPI, HTTPException
from pydantic.v1 import NoneStr
from scalar_fastapi import get_scalar_api_reference

from .database import Database
from .schemas import ShipmentRead, ShipmentCreate, ShipmentUpdate

app = FastAPI()

db = Database()


@app.get("/shipment", response_model=ShipmentRead)
def get_shipment(id: int):
    shipment = db.get(id)

    if shipment is None:
        raise HTTPException(status_code=404, detail="Shipment not found")

    return shipment


@app.post("/shipment", response_model=None)
def submit_shipment(shipment: ShipmentCreate) -> dict[str, int]:
    id = db.create(shipment)
    return {"id": id}


@app.patch("/shipment", response_model=ShipmentRead)
def update_shipment(id: int, shipment: ShipmentUpdate):
    shipment = db.update(id, shipment)
    return shipment


@app.delete("/shipment")
def delete_shipment(id: int) -> dict[str, str]:
    db.delete(id)

    return {"detail": f"Shipment id #{id} was deleted"}


@app.get("/scalar")
def get_scalar_docs():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Scalar API"
    )
