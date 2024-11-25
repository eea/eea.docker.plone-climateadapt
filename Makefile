# Variables
IMAGE_NAME = laszlocseh/eea.docker.plone-climateadapt
TAG = plone6

# Default target
.PHONY: all
all: build tag push

# Build the Docker image
.PHONY: build
build:
	docker build . -t $(IMAGE_NAME):$(TAG)

# Build the Docker image --no-cache
.PHONY: build-no-cache
build-no-cache:
	docker build -no-cache . -t $(IMAGE_NAME):$(TAG)

# Tag the Docker image (redundant in this case, but included as per your request)
.PHONY: tag
tag:
	docker tag $(IMAGE_NAME):$(TAG) $(IMAGE_NAME):$(TAG)

# Push the Docker image to the registry
.PHONY: push
push:
	docker push $(IMAGE_NAME):$(TAG)

.PHONY: release
release:
	sh -c "python2 ./release.py"


.PHONY: remove
remove:
	docker rmi $(IMAGE_NAME):$(TAG)
