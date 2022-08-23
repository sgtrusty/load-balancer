# Start from python:3.8-alpine base image
FROM python:3.8-alpine

# The latest alpine images don't have some tools like (`git` and `bash`).
# Adding git, bash and openssh to the image
RUN apk update && apk upgrade && \
    apk add --no-cache bash git openssh

# Make dir app
RUN mkdir /app
WORKDIR /app
COPY ./src/requirements.txt requirements.txt

RUN pip install -r requirements.txt

# Copy the source from the current directory to the Working Directory inside the container
COPY ./src .

# Expose port 5000 to the outside world
EXPOSE 5000

# Run the executable
CMD ["python", "balancer.py"]
