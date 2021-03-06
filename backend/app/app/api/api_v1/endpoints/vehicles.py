from typing import Any, List, Literal, Optional
from fastapi import APIRouter, Body, Depends, HTTPException, Query, Path, status
from fastapi.encoders import jsonable_encoder
from pydantic import PositiveInt
from sqlalchemy.orm import Session
from app import crud, schemas
from app.api import deps

router = APIRouter()


@router.get(
    path="/vehicle/",
    response_model=List[schemas.VehicleDatabase],
    summary="Get vehicles list",
    description="The list of vehicles can be filtered based on the presence or absence of the driver")
async def get_vehicles(
    with_drivers: Optional[Literal["yes", "no"]] = Query(None, title="Sign of the presence of the driver"),
    *,
    db: Session = Depends(deps.get_db)
) -> Any:
    """Get a filtered list of the vehicles.
    :param with_drivers: a sign of the presence or absence of a driver in the vehicle
    """
    try:
        vehicles = crud.vehicle.get_filtered(
            db,
            with_driver=True if with_drivers == "yes" else False if with_drivers == "no" else None
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Unable to connect to the database: %s" % str(e)
        )
    if not vehicles:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="There are no vehicles in the database that meet the specified criteria"
        )
    return [schemas.VehicleDatabase(**jsonable_encoder(vehicle)) for vehicle in vehicles]


@router.get(
    path="/vehicle/{vehicle_id}/",
    response_model=schemas.VehicleDatabase,
    summary="Vehicle information",
    description="Get detailed information about a particular vehicle by its ID")
async def get_vehicle_by_id(
    vehicle_id: PositiveInt = Path(..., title="Vehicle ID in the database"),
    *,
    db: Session = Depends(deps.get_db)
) -> Any:
    """Get detailed information about the vehicle.
    :param vehicle_id: vehicle ID in the database
    """
    try:
        vehicle = crud.vehicle.get(db, id=vehicle_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Unable to connect to the database: %s" % str(e)
        )
    if not vehicle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Vehicle with ID={vehicle_id} is not found in the database"
        )
    return schemas.VehicleDatabase(**jsonable_encoder(vehicle))


@router.post(
    path="/vehicle/",
    response_model=schemas.VehicleDatabase,
    summary="Add new vehicle",
    description="Create a new vehicle in the database")
async def add_vehicle(
    vehicle_in: schemas.VehicleCreate = Body(..., title="All necessary information about the vehicle"),
    *,
    db: Session = Depends(deps.get_db)
) -> Any:
    """Create a new vehicle in the database.
    :param vehicle_in: information about the vehicle to be added to the database
    """
    try:
        vehicle = crud.vehicle.create(db, obj_in=vehicle_in)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Unable to connect to the database: %s" % str(e)
        )
    return schemas.VehicleDatabase(**jsonable_encoder(vehicle))


@router.patch(
    path="/vehicle/{vehicle_id}/",
    response_model=schemas.VehicleDatabase,
    summary="Update vehicle information",
    description="Update vehicle details in the database")
async def update_vehicle(
    vehicle_id: PositiveInt = Path(..., title="Vehicle ID in the database"),
    vehicle_in: schemas.VehicleUpdate = Body(..., title="New vehicle information"),
    *,
    db: Session = Depends(deps.get_db)
) -> Any:
    """Update vehicle details in the database.
    :param vehicle_id: vehicle ID in the database
    :param vehicle_in: new vehicle information to be updated in the database
    """
    try:
        vehicle = crud.vehicle.get(db, id=vehicle_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Unable to connect to the database: %s" % str(e)
        )
    if not vehicle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Vehicle with ID={vehicle_id} is not found in the database"
        )
    try:
        updated_vehicle = crud.vehicle.update(db, db_obj=vehicle, obj_in=vehicle_in, exclude_empty=True)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Unable to connect to the database: %s" % str(e)
        )
    return schemas.VehicleDatabase(**jsonable_encoder(updated_vehicle))


@router.post(
    path="/set_driver/{vehicle_id}/",
    response_model=schemas.VehicleDatabase,
    summary="Put the driver in the vehicle",
    description="Set or remove the driver from the vehicle with the specified ID")
async def set_driver_in_vehicle(
    vehicle_id: PositiveInt = Path(..., title="Vehicle ID in the database"),
    data_in: schemas.DriverID = Body(..., title="Driver ID in the database"),
    *,
    db: Session = Depends(deps.get_db)
) -> Any:
    """Put or remove the driver from the vehicle.
    :param vehicle_id: vehicle ID in the database
    :param data_in: driver ID in the database,
    to remove the driver from the vehicle it is necessary to pass the None or empty body of the request;
    if the driver with the specified ID does not exist, then the properties of the vehicle remain unchanged.
    """
    try:
        vehicle = crud.vehicle.get(db, id=vehicle_id)
        driver = crud.driver.get(db, id=data_in.driver_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Unable to connect to the database: %s" % str(e)
        )
    if not vehicle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Vehicle with ID={vehicle_id} is not found in the database"
        )
    if driver is not None or data_in.driver_id is None:
        try:
            vehicle = crud.vehicle.update(db, db_obj=vehicle, obj_in={"driver_id": data_in.driver_id})
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Unable to connect to the database: %s" % str(e)
            )
    return schemas.VehicleDatabase(**jsonable_encoder(vehicle))


@router.delete(
    path="/vehicle/{vehicle_id}/",
    response_model=schemas.VehicleDatabase,
    summary="Delete the vehicle",
    description="Remove the specified vehicle from the database")
async def delete_vehicle(
    vehicle_id: PositiveInt = Path(..., title="Vehicle ID in the database"),
    *,
    db: Session = Depends(deps.get_db)
) -> Any:
    """Delete the specified vehicle from the database.
    :param vehicle_id: vehicle ID in the database
    :return: details of the removed vehicle
    """
    try:
        vehicle = crud.vehicle.remove(db, id=vehicle_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Unable to connect to the database: %s" % str(e)
        )
    if not vehicle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Vehicle with ID={vehicle_id} is not found in the database"
        )
    return schemas.VehicleDatabase(**jsonable_encoder(vehicle))
