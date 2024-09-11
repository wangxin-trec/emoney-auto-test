from collections import namedtuple
import re,os


def Singleton(cls):
    instance = {}
    def _singleton_wrapper(*args, **kargs):
        if cls not in instance:
            instance[cls] = cls(*args, ** kargs)
        return instance[cls]
    return _singleton_wrapper
class struct(object):
    def __new__(cls, data):
        if isinstance(data, dict):
            return namedtuple('struct', data.keys())(*(struct(val) for val in data.values()))
        elif isinstance(data, (tuple, list, set, frozenset)):
            return type(data)(struct(_) for _ in data)
        else:
            return data

class Common:
  def _isNul(object):
    """
    方法意味：オブジェクトが空かどうかを判断する
    params:
        str_param: オブジェクト
    return: なし
    """
    result = False
    if object == 'undefined' or object == 'null' or object == '' or object == [] or object == '[]' or object == None:
        result = True
    return result

  def _validatePath(name):
    """
    方法意味：filter invalid str
    params:
        name: filename
    return: filtered str
    """
    rstr = r'[\/\\\:\*\?\"\<\>\|]'
    new_name = re.sub(rstr, "_", name)
    return new_name

  def getAllureRootPath():
    """
    方法意味：get allure root dir
    params: なし
    return: allure root dir
    """
    allure_path = ''
    os_environ_var_paths = os.environ.get('PATH')
    if os_environ_var_paths.__contains__(';'):
      for os_environ_var_path in os_environ_var_paths.split(';'):
        if os_environ_var_path.lower().__contains__('allure'):
          allure_path = os.path.abspath(os.path.join(os_environ_var_path, '..'))
          break
    elif os_environ_var_paths.lower().__contains__('allure'):
      allure_path = os.path.abspath(os.path.join(os_environ_var_paths, '..'))
    return allure_path