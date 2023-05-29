# Slim Model Docker Images


## Installation

Create the virtual environment.

```sh
python -m venv .venv &&
. .venv/bin/activate &&
pip install -r requirements.txt
```


Test the app localy.

```sh
uvicorn app.main:app --reload

# using poetry
# poetry run uvicorn app.main:app --reload
```

Build the docker image to containerize the app.

```sh
docker build -t myapp .
docker run --rm -p 8000:8000 myapp
```

## testing server

```sh
curl -X POST -H "Content-Type: application/json" \
    -d '{"name": "linuxize", "price": 2.89}' \
    localhost:8000/items/
```

Stress testing many times.

```sh
docker run --rm -p 8000:8000 --name foo -d myapp && \
sleep 0.5 && \
time ( for i in `seq 20`; do; python test.py >> /dev/null; done; ) && \
docker container stop foo

# 20 iter
# 8.91s user 32.45s system 784% cpu 5.271 total

# 100 iter
# 51.30s user 161.74s system 773% cpu 27.530 total
```

Stress test with spinning container up every time.

```sh
time (for i in `seq 20`; do  docker run --rm -p 8000:8000 --name foo -d myapp && sleep 0.4 && python test.py && docker container stop foo; done >> /dev/null)

# WRONG? 11.29s user 35.88s system 169% cpu 27.817 total
# 14.92s user 35.28s system 132% cpu 38.016 total
```


## build image
docker build -t foo_ex .
docker build -t foo_ex --progress=plain --no-cache .


## test image
docker run --rm -t foo_ex -c "print('foo')"
docker run --rm -t foo_ex -c "import numpy as np; print(np.random.random())"


## inspect image, TAB to switch
dive build -t foo_ex .   


## slim builds

### testing

docker pull --platform linux/x86_64 archlinux:latest

slim build --target archlinux:latest --tag archlinux:curl --http-probe=false --exec "curl checkip.amazonaws.com"

docker run archlinux:curl curl checkip.amazonaws.com


