#! /usr/bin/env python

import requests
import json
import numpy as np
import pandas as pd
import time
import docker


def sim(n=10):
    b = 5
    b_price = 1.0
    b_promo = 2.0
    sigma = 0.1

    price = np.random.normal(0, 1, size=n)
    promo_ind = np.random.binomial(1, 0.5, size=n)
    error = np.random.normal(0, sigma, size=n)

    qty = (
        b
        + b_price * price
        + b_promo * promo_ind
        + error
    )

    df = pd.DataFrame(
        {
            "qty": qty,
            "price": price,
            "promo_ind": promo_ind,
        }
    )
    return df


def main():
    base_url = "http://localhost:8000/"
    url = base_url + "fit/"
    df = sim(n=200)
    post_data = {
        "name": "linear_regression",
        "y_name": "qty",
        "x_names": ["price", "promo_ind"],
        "data": df.to_dict(),
    }

    client = docker.from_env()
    container = client.containers.run(
        image="myapp",
        detach=True,
        remove=True,
        ports={'8000/tcp': 8000},
    )

    max_tries = 12
    init_wait = 0.7
    incr_wait = 0.08

    start = time.time()
    time.sleep(init_wait)
    for i in range(max_tries):
        try:
            resp = requests.get(base_url)
            break
        except requests.exceptions.ConnectionError:
            time.sleep(incr_wait)
            continue

    print(f"waited {i} times for a total of {time.time()-start:0.3f} s.")

    start = time.time()
    resp = requests.post(
        url,
        data=json.dumps(post_data),
        headers={"Content-Type": "application/json"},
    )
    print(f"model results received in {(time.time()-start)*1000:0.2f} ms.")


    if resp:
        print(resp.json())

    container.stop()


if __name__ == "__main__":
    main()
