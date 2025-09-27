from contextlib import asynccontextmanager
from datetime import datetime, timedelta

from fastapi import FastAPI, HTTPException
from scalar_fastapi import get_scalar_api_reference
from rich import panel

from app.database.session import create_db_tables, SessionDependency
from .database.models import Shipment, ShipmentStatus

from .schemas import ShipmentRead, ShipmentCreate, ShipmentUpdate


@asynccontextmanager
async def lifespan_handler(app: FastAPI):
    print(panel.Panel("Server Started ...", border_style="green"))
    create_db_tables()
    yield
    print(panel.Panel("Server Stopped ...", border_style="red"))


app = FastAPI(lifespan=lifespan_handler)


@app.get("/shipment", response_model=ShipmentRead)
def get_shipment(id: int, session: SessionDependency):
    shipment = session.get(Shipment, id)

    if shipment is None:
        raise HTTPException(status_code=404, detail="Shipment not found")

    return shipment


@app.post("/shipment", response_model=None)
def submit_shipment(shipment: ShipmentCreate, session: SessionDependency) -> dict[str, int]:
    new_shipment = Shipment(
        **shipment.model_dump(),
        status=ShipmentStatus.placed,
        estimated_delivery=datetime.now() + timedelta(days=3)
    )
    session.add(new_shipment)
    session.commit()
    session.refresh(new_shipment)
    return {"id": new_shipment.id}


@app.patch("/shipment", response_model=ShipmentRead)
def update_shipment(id: int, shipment_update: ShipmentUpdate, session: SessionDependency):
    update = shipment_update.model_dump(exclude_none=True)

    if not update:
        raise HTTPException(
            status_code=404,
            detail="Shipment not found"
        )

    shipment = session.get(Shipment, id)
    shipment.sqlmodel_update(update)

    session.add(shipment)
    session.commit()
    session.refresh(shipment)

    return shipment


@app.delete("/shipment")
def delete_shipment(id: int, session: SessionDependency) -> dict[str, str]:
    session.delete(
        session.get(Shipment, id)
    )
    session.commit()

    return {"detail": f"Shipment id #{id} was deleted"}


@app.get("/scalar")
def get_scalar_docs():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Scalar API"
    )
