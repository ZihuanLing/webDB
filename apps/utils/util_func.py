from datetime import datetime, date

__all__ = ['json_serial', 'json_serial2']


def json_serial(obj):
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError("Type {} is not serializable.".format(type(obj)))


def json_serial2(obj):
    if isinstance(obj, (datetime, date)):
        return obj.strftime("%Y-%m-%d %H:%M:%S")
    raise TypeError("Type {} is not serializable.".format(type(obj)))
