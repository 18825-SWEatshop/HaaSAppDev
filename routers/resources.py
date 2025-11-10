import os
import jwt
from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel, PositiveInt

from ..project_manager import get_hardware_allocation, increase_hardware_allocation, decrease_hardware_allocation
from ..resource_manager import (
	RESOURCE_NOT_FOUND_MSG,
	checkin_resource,
	checkout_resource,
	get_availability,
	get_capacity,
)

SECRET = os.getenv("JWT_SECRET", "dev-secret")

router = APIRouter()


def current_user(request: Request) -> str:
	auth_header = request.headers.get("Authorization", "")
	if not auth_header.startswith("Bearer "):
		raise HTTPException(401, "Missing token")
	token = auth_header.split(" ", 1)[1]
	try:
		payload = jwt.decode(token, SECRET, algorithms=["HS256"])
		return payload["u"]
	except Exception as exc:  # pylint: disable=broad-exception-caught
		raise HTTPException(401, "Invalid token") from exc


class ResourceAllocationChange(BaseModel):
	setNumber: int
	quantity: PositiveInt
	projectId: str


def _resource_to_response(resource_doc: dict) -> dict:
	return {k: v for k, v in resource_doc.items() if k != "_id"}


@router.get("/capacity/{set_number}")
def api_get_capacity(set_number: int, _: str = Depends(current_user)):
	try:
		capacity = get_capacity(set_number)
	except ValueError as exc:
		status = 404 if str(exc) == RESOURCE_NOT_FOUND_MSG else 400
		raise HTTPException(status, str(exc)) from exc
	return {"setNumber": set_number, "capacity": capacity}


@router.get("/availability/{set_number}")
def api_get_availability(set_number: int, _: str = Depends(current_user)):
	try:
		availability = get_availability(set_number)
	except ValueError as exc:
		status = 404 if str(exc) == RESOURCE_NOT_FOUND_MSG else 400
		raise HTTPException(status, str(exc)) from exc
	return {"setNumber": set_number, "availability": availability}


@router.post("/checkin")
def api_checkin_resources(payload: ResourceAllocationChange, _: str = Depends(current_user)):
	try:
		resource = checkin_resource(payload.setNumber, payload.quantity)
	except ValueError as exc:
		status = 404 if str(exc) == RESOURCE_NOT_FOUND_MSG else 400
		raise HTTPException(status, str(exc)) from exc
	try:
		decrease_hardware_allocation(payload.projectId, payload.setNumber, payload.quantity)
	except ValueError as exc:
		raise HTTPException(404 if "not found" in str(exc).lower() else 400, str(exc)) from exc
	return {"ok": True, "resource": _resource_to_response(resource)}


@router.post("/checkout")
def api_checkout_resources(payload: ResourceAllocationChange, _: str = Depends(current_user)):
	try:
		resource = checkout_resource(payload.setNumber, payload.quantity)
	except ValueError as exc:
		status = 404 if str(exc) == RESOURCE_NOT_FOUND_MSG else 400
		raise HTTPException(status, str(exc)) from exc
	try:
		increase_hardware_allocation(payload.projectId, payload.setNumber, payload.quantity)
	except ValueError as exc:
		raise HTTPException(404 if "not found" in str(exc).lower() else 400, str(exc)) from exc
	return {"ok": True, "resource": _resource_to_response(resource)}
