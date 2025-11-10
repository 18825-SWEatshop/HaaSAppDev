from typing import Optional, Dict
from pymongo import ReturnDocument
from .database import db

RESOURCE_NOT_FOUND_MSG = "Resource set not found"


def _resources():
	if db is None:
		raise RuntimeError("Database not connected.")
	collection = db["resources"]
	collection.create_index("setNumber", unique=True)
	return collection


def get_resource(set_number: int) -> Optional[dict]:
	return _resources().find_one({"setNumber": set_number})


def get_capacity(set_number: int) -> int:
	resource = get_resource(set_number)
	if not resource:
		raise ValueError(RESOURCE_NOT_FOUND_MSG)
	return int(resource.get("capacity", 0))


def get_availability(set_number: int) -> int:
	resource = get_resource(set_number)
	if not resource:
		raise ValueError(RESOURCE_NOT_FOUND_MSG)
	return int(resource.get("availability", 0))


def _validate_quantity(quantity: int) -> None:
	if quantity <= 0:
		raise ValueError("Quantity must be positive")


def checkout_resource(set_number: int, quantity: int) -> Dict:
	_validate_quantity(quantity)
	collection = _resources()

	doc = collection.find_one_and_update(
		{
			"setNumber": set_number,
			"availability": {"$gte": quantity},
		},
		{"$inc": {"availability": -quantity}},
		return_document=ReturnDocument.AFTER,
	)
	if not doc:
		resource = get_resource(set_number)
		if resource is None:
			raise ValueError(RESOURCE_NOT_FOUND_MSG)
		raise ValueError("Insufficient availability")
	return doc


def checkin_resource(set_number: int, quantity: int) -> Dict:
	_validate_quantity(quantity)
	collection = _resources()

	doc = collection.find_one_and_update(
		{
			"setNumber": set_number,
			"$expr": {"$lte": [{"$add": ["$availability", quantity]}, "$capacity"]},
		},
		{"$inc": {"availability": quantity}},
		return_document=ReturnDocument.AFTER,
	)
	if not doc:
		resource = get_resource(set_number)
		if resource is None:
			raise ValueError(RESOURCE_NOT_FOUND_MSG)
		raise ValueError("Cannot exceed capacity")
	return doc
