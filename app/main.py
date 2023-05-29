from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
import json
import pandas as pd
from sklearn.linear_model import LinearRegression


def fit_model(x_names, y_name, df):
    model = LinearRegression().fit(
        df[x_names], df[y_name]
    )

    score = model.score(
        df[x_names],
        df[y_name],
    )

    return {
        "score": score,
        "coefs": [model.intercept_] + list(model.coef_),
    }


app = FastAPI()


class ModelSpec(BaseModel):
    name: str
    y_name: str
    x_names: list[str]


class TrainSpec(ModelSpec):
    data: dict
    # class Config:
    #     arbitrary_types_allowed = True


@app.get("/")
def root():
    return {"message": "Hello World!"}


@app.post("/fit/")
async def fit(train_spec: TrainSpec):
    print(f"Fitting model: {train_spec.name}")

    res = fit_model(
        x_names=train_spec.x_names,
        y_name=train_spec.y_name,
        df = pd.DataFrame(train_spec.data),
    )

    return json.dumps(res)






# 1 - "data_id" retirve data from storage
# 2 - send data via REST
# 3 - send data via gRPC


# @app.get("/items/{item_id}")
# async def read_item(item_id):
#     return {"item_id": item_id}
