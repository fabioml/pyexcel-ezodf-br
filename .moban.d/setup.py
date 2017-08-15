{% extends 'setup.py.jj2' %}

{% block header %}
#!/usr/bin/env python
# coding:utf-8
# Author:  mozman
# Purpose: setup
# Created: 27.12.2010
# License: MIT license
#
#    Copyright (C) 2010  Manfred Moitzi
#
# Previous maintainer: 'Anton Shvein'
# Contact: 't0hashvein@gmail.com'
#
{% endblock %}

{%block platform_block%}
{%endblock%}

{%block morefiles%}'CONTRIBUTORS.rst',{%endblock%}

{%block additional_classifiers %}
          "License :: OSI Approved :: MIT License",
          "Development Status :: 3 - Alpha",
          "Operating System :: OS Independent",
          "Topic :: Office/Business :: Office Suites"
{%endblock%}
