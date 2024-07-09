#!/bin/bash

docker build -t hebrew-calendar .
docker run -p 80:8501 -d hebrew-calendar