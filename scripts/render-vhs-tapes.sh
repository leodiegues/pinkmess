#!/usr/bin/env bash

for f in $(find ./docs/tapes -name '*.tape'); do
    echo "Rendering $f";
    vhs $f;
done
