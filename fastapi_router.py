from fastapi import APIRouter, Body
from schemas import Item, Image, Offer
from typing import Annotated


router = APIRouter(prefix="/items", tags=["items"])


@router.put("/items/{item_id}")
async def update_item(item_id: int, item: Annotated[Item, Body(embed=True)]):
    results = {"item_id": item_id, "item": item}
    return results


@router.post("/offers/")
async def create_offer(offer: Offer):
    return offer

@router.post("/images/multiple/")
async def create_multiple_images(images: list[Image]):
    return images
