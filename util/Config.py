from collections import namedtuple
import json

def Singleton(cls):
    instance = {}
    def _singleton_wrapper(*args, **kargs):
        if cls not in instance:
            instance[cls] = cls(*args, ** kargs)
        return instance[cls]
    return _singleton_wrapper

@Singleton
class Config:
  def __init__(self):
    with open('./config/config.json','r',encoding='utf-8') as file:
      self.config = struct(json.loads(file.read()))


class struct(object):
    def __new__(cls, data):
        if isinstance(data, dict):
            return namedtuple('struct', data.keys())(*(struct(val) for val in data.values()))
        elif isinstance(data, (tuple, list, set, frozenset)):
            return type(data)(struct(_) for _ in data)
        else:
            return data

ConfigInfo = Config().config