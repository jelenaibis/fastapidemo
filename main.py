from fastapi import FastAPI, Query,  Path
from enum import Enum
from pydantic import BaseModel
from typing import Annotated


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


class Month(str, Enum):
    april = "april"
    september = "september"
    june = "june"
    july = "july"


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


app = FastAPI()


@app.post("/items/")
async def create_item(item: Item):
    item_dict = item.model_dump()
    if item.tax:
        price = item.price + item.tax
        item_dict.update({"final_price": price})

    return item_dict


@app.put("/items/create/{item_id}")
async def create_item(item_id: int, item: Item, q: str | None = None):
    result = {"id": item_id, **item.model_dump()}
    if q:
        result.update({"q": q})

    return result


@app.put("/not_pydantic_items/")
async def create_item(item: Item):
    item_dict = item.model_dump()
    if item.tax:
        price = item.price + item.tax
        item_dict.update({"final_price": price})

    return item_dict


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}


@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}


@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}


@app.get("/users")
async def read_users():
    return ["Rick", "Morty"]


@app.get("/users")
async def read_users2():
    return ["Bean", "Elfo"]


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}


@app.get("/month/{month_name}")
async def get_month(month_name: Month):
    if month_name is Month.june:
        return {"month_name": month_name, "message": "ENYOY THE SUMMER!"}

    if month_name.value == "july":
        return {"month_name": month_name, "message": "ENYOY THE SUMMER!"}

    if month_name.value == "september":
        return {"month_name": month_name, "message": "OH NO! September is a rainy month."}

    return {"month_name": month_name, "message": "The best month ever!"}


@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}


fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


# query params
@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip: skip + limit]


# optional query param
@app.get("/items1/{item_id}")
async def read_item(item_id: str, q: str | None = None, short: bool = False):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item


@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
        user_id: int, item_id: str, q: str | None = None, short: bool = False
):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item


# required params
@app.get("/items/{item_id}")
async def read_user_item(item_id: str, needy: str):
    item = {"item_id": item_id, "needy": needy}
    return item


@app.get("/items2/{item_id}")
async def read_user_item(
        item_id: str, needy: str, skip: int = 0, limit: int | None = None
):
    item = {"item_id": item_id, "needy": needy, "skip": skip, "limit": limit}
    return item


@app.get("/items_qp_string_validation_with_annotated/")
async def read_items(q: Annotated[str | None, Query(min_length=3, max_length=50, pattern="^fixedquery$")] = None):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


@app.get("/items_required_param/")
async def read_items(q: Annotated[str, Query(min_length=3)] = ...):  # required param q
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# @app.get("/items_required_param/")
# async def read_items(q: Annotated[str, Query(min_length=3)] = Required):  # required param q
#     results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
#     if q:
#         results.update({"q": q})
#     return results


@app.get("/items_required_param_with_none_value/")
async def read_items(q: Annotated[str | None, Query(min_length=3)] = ...):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


@app.get("/items_list_optional_params/")
async def read_items(q: Annotated[list[str] | None, Query()] = None):
    query_items = {"q": q}
    return query_items


@app.get("/items_list_default_params_value/")
async def read_items(q: Annotated[list[str], Query()] = ["foo", "bar"]):
    query_items = {"q": q}
    return query_items


@app.get("/items_with_desc/")
async def read_items(
        q: Annotated[
            str | None,
            Query(
                title="Query string",
                description="Query string for the items to search in the database that have a good match",
                min_length=3,
            ),
        ] = None
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


@app.get("/items_with_alias/")
async def read_items(q: Annotated[str | None, Query(alias="item-query")] = None):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


@app.get("/items_final/")
async def read_items(
        q: Annotated[
            str | None,
            Query(
                alias="item-query",
                title="Query string",
                description="Desc",
                min_length=1,
                max_length=50,
                pattern="^fixedquery$",
                deprecated=True,

            )
        ] = None
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


@app.get("/items_hidden_query/")
async def read_items(
    hidden_query: Annotated[str | None, Query(include_in_schema=False)] = None
):
    if hidden_query:
        return {"hidden_query": hidden_query}
    else:
        return {"hidden_query": "Not found"}


@app.get("/items_with_annotated/{item_id}")
async def read_items(
    item_id: Annotated[int, Path(title="The ID of the item to get")],
    size: Annotated[float, Query(gt=0, lt=10.5)],
    q: Annotated[str | None, Query(alias="item-query")] = None,

):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results


