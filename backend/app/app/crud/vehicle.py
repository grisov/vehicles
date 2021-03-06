from typing import List, Optional
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app.models import Vehicle
from app.schemas import VehicleCreate, VehicleUpdate
from .base import CRUDBase


class CRUDVehicle(CRUDBase[Vehicle, VehicleCreate, VehicleUpdate]):
    """CRUD object with basic methods for manipulation of the vehicles records in a database."""

    def create(
        self,
        db: Session,
        *,
        obj_in: VehicleCreate,
        driver_id: Optional[int] = None
    ) -> Vehicle:
        """Add a new vehicle object to the database."""
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, driver_id=driver_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_filtered(
        self,
        db: Session,
        *,
        with_driver: Optional[bool] = None
    ) -> List[Vehicle]:
        """Get a list of vehicles which can be filtered by the presence of the driver.
        :param with_driver: a sign of the presence or absence of a driver in the vehicle
        (if this value is empty, it is not taken into account)
        """
        query = db.query(Vehicle)
        if with_driver:
            query = query.filter(Vehicle.driver_id.isnot(None))
        elif with_driver is False:
            query = query.filter(Vehicle.driver_id.is_(None))
        return query.all()


vehicle = CRUDVehicle(Vehicle)
