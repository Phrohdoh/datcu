# Datcu

Written in Python 3.

Requires:
* [PhantomJS](http://phantomjs.org/) (built against version 2.1.1)
* selenium 2.52.0
* selenium-requests 1.2.7

You need to set environment variables `DATCU_USERNAME` and `DATCU_PASSWORD`.

Example:
```python
DATCU_USERNAME=Phrohdoh DATCU_PASSWORD=Hunter2 python datcu.py
```

Also checkout `challenges.json` for examples of how to answer the challenge
questions you setup. You should of course add any that are missing.
