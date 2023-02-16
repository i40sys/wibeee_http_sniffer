# Description

A piece of python for sniffing HTTP packets for a given interface. Get the query string of the URL in the HTTP headers and convert the parameters into JSON string. Finally, that JSON string is sent to an IP address using UDP.

# Build the image

It's based on official Python image on top of alpine for reducing the final image size. Expected size is ~270MB.

```
docker-compose build
```

# Configuration

Take a look inside docker-compose and modify the environment variables for setting proper behaviour of the sniffing process.

```
# default values:
LOGLEVEL=INFO
IFACE=qvs1
FILTER=(host 10.2.8.224 or host 10.2.8.225) and (port 8080)
UDP_IP=10.2.10.11
UDP_PORT=58088
```

# Run

```
docker-compose up -d
```

# Debugging

```
docker run -it --rm --network=host --privileged ymbihq/wibeee_sniffer:latest /bin/sh
# the run the entry command in the folder /sniffer
python3 http_sinffer.py
# or whatever that you need for debugging.
```

# Resources:

- https://git.oriolrius.cat/oriolrius/wibeee_http_sniffer
