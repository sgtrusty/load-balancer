# '''
#  # SpinachSocket - a metric load balancer with multi-threading
#  # Copyright (C) 2022  Santiago González <https://github.com/sgtrusty>
#  #             ~ Assembled through trust in coffee. ~
#  #
#  # This program is free software; you can redistribute it and/or modify
#  # it under the terms of the CC BY-NC-ND 4.0 as published by
#  # the Creative Commons; either version 2 of the License, or
#  # (at your option) any later version.
#  #
#  # This program is distributed in the hope that it will be useful,
#  # but WITHOUT ANY WARRANTY; without even the implied warranty of
#  # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  # CC BY-NC-ND 4.0 for more details.
#  #
#  # You should have received a copy of the CC BY-NC-ND 4.0 along
#  # with this program; if not, write to the  Creative Commons Corp.,
#  # PO Box 1866, Mountain View, CA 94042.
#  #
# '''
# Start from python:3.8-alpine base image
FROM python:3.8-alpine

# The latest alpine images don't have some tools like (`git` and `bash`).
# Adding git, bash and openssh to the image
RUN apk update && apk upgrade
RUN apk add --no-cache bash git openssh vim

# Make dir app
RUN mkdir /app
WORKDIR /app
COPY ./requirements.txt requirements.txt

RUN pip install -r requirements.txt

# Copy the source from the current directory to the Working Directory inside the container
COPY . .

RUN chmod +x utils/*

# Expose port 5000 to the outside world
EXPOSE 5000

# Run the executable
CMD utils/bind_eth0.sh
