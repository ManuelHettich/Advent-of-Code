#!/bin/sh

black --check --diff $(git ls-files '*.py')