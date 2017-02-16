# FashionSense ML

## Description
Docker container hosting our machine learning stuff.

## Install
* [Install Docker](https://docs.docker.com/engine/installation/)
* Or to run outside of Docker, do a pip install
```
$ pip install -r requirements.txt
```

## Usage
* to run with Docker
    * first build everything with Docker
    ```
    $ docker build -t ml .
    ```
    * to run with Docker
    ```
    $ docker run -p 5000:5000 ml
    ```
* to run for debugging
    * set the DEBUG env variable
    ```
    $ export DEBUG=1
    ```
    * simply run the python app directly with DEBUG set
    ```
    $ python app.py
    ```
* to run in production
    * if you set the environment variable for debugging unset it
    ```
    $ unset DEBUG
    ```
    * simply run the python app directly
    ```
    $ python app.py
    ```
