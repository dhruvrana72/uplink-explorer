<a href="https://www.adjoint.io" target="_blank">
  <p align="center"><img src="https://www.adjoint.io/images/logo-small.png" width="250"/> </p>
</a>
<h3 align="center">Community Edition</h3>

Block Explorer
==============

[![CircleCI](https://circleci.com/gh/adjoint-io/uplink-explorer.svg?style=svg&circle-token=8c789d75f942ee92eef733755c4975968df51485)](https://circleci.com/gh/adjoint-io/uplink-explorer)

Installation
------------

```
  git clone git@github.com:adjoint-io/uplink-explorer.git && cd uplink explorer
  virtualenv -p /usr/bin/python2.7 venv
  source venv/bin/activate 
  pip install -r requirements.txt
```

Usage
-----

Local Development ( with reloader )

```
ENV=DEV READONLY=FALSE python app.py
```


Testing
-------
To run the test suite:

```
  pytest -s -vv tests/
```

License
-------

Copyright 2017 Adjoint Inc

Released under Apache 2.0.
