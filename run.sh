#!/bin/bash

sudo docker run -it --rm \
	-v /share/CACHEDEV1_DATA/Container/python3-dev/code:/home/python3/code \
	--network="host" \
	--privileged \
	--init kuralabs/python3-dev:latest bash
