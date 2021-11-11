#!/usr/bin/env bash

VERSION=${VERSION:-wallaby}

buildah build-using-dockerfile \
    --format docker \
    --build-arg "VERSION=$VERSION" \
    --tag "generator:$VERSION" \
    $BUILD_OPTS .

podman run --rm -v $(pwd)/output:/output generator:$VERSION python3 /main.py cinder
podman run --rm -v $(pwd)/output:/output generator:$VERSION python3 /main.py keystone
podman run --rm -v $(pwd)/output:/output generator:$VERSION python3 /main.py nova
podman run --rm -v $(pwd)/output:/output generator:$VERSION python3 /main.py oslo.cache

sphinx-build -b html output build/html
