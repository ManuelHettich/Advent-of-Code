#!/bin/sh

pylint --rcfile=.pylintrc $(git ls-files '*.py')