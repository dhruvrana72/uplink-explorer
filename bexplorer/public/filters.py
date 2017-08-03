# -*- coding: utf-8 -*-
"""template filters"""
# filters.py
import time
import json
import jinja2
import flask
from bexplorer.extensions import uplink
from bexplorer.utils import formatPrec

blueprint = flask.Blueprint('filters', __name__)

# using the decorator
# @jinja2.contextfilter
# @blueprint.app_template_filter()
# def filter1(context, value):
#     return 1

# # using the method


# @jinja2.contextfilter
# def filter2(context, value):
#     return 2


CUTLENGTH = 10  # length to shorten hashes
FPREC = 0.0000001


@jinja2.contextfilter
@blueprint.app_template_filter()
def shorten(context, string):
    """shorten addresses for readability"""
    if string:
        return string[0:CUTLENGTH]
    else:
        return ''


@jinja2.contextfilter
@blueprint.app_template_filter()
def shorten_key(context, string):
    """shorten keys"""
    if string:
        return string[30:40]
    else:
        return ''


@jinja2.contextfilter
@blueprint.app_template_filter()
def peers(context, p):
    """Peers filter"""
    results = uplink.peers()
    peers = len(results)

    return peers


@jinja2.contextfilter
@blueprint.app_template_filter()
def convert(context, value, atype):
    """
        convert asset type fractional to fixed precision
        FPREC is 10^(-7) or 0.0000001
    """
    if value:
        if atype.type == 'Discrete':
            return value

        if atype.type == 'Fractional':

            prec = atype.precision or 0
            result = formatPrec(prec, value)
            return result

        if atype.type == 'Binary':
            if value <= 0:
                return 'not held'
            else:
                return 'held'
    else:
        return 'error with asset type'


@jinja2.contextfilter
@blueprint.app_template_filter()
def remove_extra_value(context, value):
    if type(value) is dict:
        value = '{} : {}'.format(value['tag'], value['contents'])
        return value
    else:
        return value


@jinja2.contextfilter
@blueprint.app_template_filter()
def to_pretty_json(context, value):
    return json.dumps(value, sort_keys=True,
                      indent=4, separators=(',', ': '))


@jinja2.contextfilter
@blueprint.app_template_filter()
def datetimeformat(context, timestamp):
    """Filter for converting timestamp to human readable"""
    print(timestamp)
    return time.strftime('%m/%d/%Y, %I:%M:%S %p', time.localtime(timestamp / 1000000))


blueprint.add_app_template_filter(datetimeformat)
