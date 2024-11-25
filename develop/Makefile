# Variables
IMAGE_NAME = plone6-cca-dev
CONTAINER_NAME = plone6-cca-dev
PORT = 8080

# Default target
.PHONY: all
all: build run

# Build the Docker image
.PHONY: build
build:
	docker build . -t $(IMAGE_NAME)

# Build the Docker image --no-cache
.PHONY: build-no-cache
build-no-cache:
	docker build --no-cache . -t $(IMAGE_NAME)

# Run the Docker container
.PHONY: run
run:
	docker run -it --rm -p $(PORT):$(PORT) --name $(CONTAINER_NAME) $(IMAGE_NAME)

.PHONY: remove
remove:
	docker rm $(CONTAINER_NAME)