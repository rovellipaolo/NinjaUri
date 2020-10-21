#!/usr/bin/env sh

case "$1" in
    ninjauri|ninjauri.py)
        shift
        exec python3 $NINJAURI_HOME/ninjauri.py $@
        ;;
    *)
        # Pass through other commands, like /bin/sh
        exec "$@"
        ;;
esac
