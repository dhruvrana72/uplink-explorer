<a href="https://www.adjoint.io" target="_blank">
  <p align="center"><img src="https://www.adjoint.io/images/logo-small.png" width="250"/> </p>
</a>
<h3 align="center">Community Edition</h3>

Block Explorer
==============

[![CircleCI](https://circleci.com/gh/adjoint-io/uplink-explorer.svg?style=svg&circle-token=8c789d75f942ee92eef733755c4975968df51485)](https://circleci.com/gh/adjoint-io/uplink-explorer)

Installation
------------

Install Directions : [https://www.youtube.com/watch?v=VeWkuNf83Kw](https://www.youtube.com/watch?v=VeWkuNf83Kw)

<center>
  <a href="https://www.youtube.com/watch?v=VeWkuNf83Kw">
    <p align="center">
      <img src="https://img.youtube.com/vi/VeWkuNf83Kw/0.jpg"/>
    </p>
  </a>
</center>

```bash
$ git clone git@github.com:adjoint-io/uplink-explorer.git && cd uplink explorer
$ virtualenv -p /usr/bin/python2.7 venv
$ source venv/bin/activate 
$ pip install -r requirements.txt
```

Usage
-----

Video tutorial series:

* [Creating Accounts](https://www.youtube.com/watch?v=pAO8DOOOuWw&index=3&list=PLssH0Xui89Ex2ou_U96t8l7Nk04ycr5zV)
* [Creating Assets](https://www.youtube.com/watch?v=XROH210vC4M&index=1&list=PLssH0Xui89Ex2ou_U96t8l7Nk04ycr5zV)
* [Creating Contracts](https://www.youtube.com/watch?v=cu2BXQFOj7U&index=2&list=PLssH0Xui89Ex2ou_U96t8l7Nk04ycr5zV)

To run the web application locally start the webserver and [Uplink node](https://github.com/adjoint-io/uplink#running-a-node).

```bash
$ ENV=DEV READONLY=FALSE python app.py
```


Testing
-------
To run the test suite:

```bash
$ pytest -s -vv tests/
```

License
-------

Copyright 2017-2018 Adjoint Inc

Released under Apache 2.0.
