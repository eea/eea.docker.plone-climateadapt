# Variables
IMAGE_NAME = tiberiuichim/eea.docker.plone-climateadapt
TAG=6.0.13-1
CONTAINER_NAME = plone6-cca-dev
PORT = 8080

# Default target
.PHONY: build-nocache-run
build-nocache-run: remove build-no-cache run

# Build the Docker image
.PHONY: build
build:
	docker build . -t $(IMAGE_NAME):$(TAG)

# Build the Docker image --no-cache
.PHONY: build-no-cache
build-no-cache:
	docker build --no-cache . -t $(IMAGE_NAME)

# Run the Docker container
.PHONY: run
run:
	docker run -it \
	-p $(PORT):$(PORT) \
	--name $(CONTAINER_NAME) \
	-v /home/laszlo/work/climate-adapt-eea/data-plone6:/data \
	$(IMAGE_NAME)

# Push the Docker image to the registry
.PHONY: push
push:
	docker push $(IMAGE_NAME):$(TAG)

.PHONY: start
start:
	docker start -i -a ${CONTAINER_NAME}

.PHONY: stop
stop:
	docker stop ${CONTAINER_NAME}

.PHONY: remove
remove:
	docker rm $(CONTAINER_NAME)

.PHONY: publish
publish: build push
	@echo "Done"
