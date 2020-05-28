#!/usr/bin/env bash

case "$1" in
    ninjauri|ninjauri.py)
        shift
        exec python3 $NINJAURI_DIR/ninjauri.py $@
        ;;
    *)
        # Pass through other commands, like /bin/bash
        exec "$@"
        ;;
esac
