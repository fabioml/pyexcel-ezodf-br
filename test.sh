pip freeze
nosetests --with-cov --cover-package ezodf --cover-package tests  tests ezodf
# && flake8 . --exclude=.moban.d --builtins=unicode,xrange,long
