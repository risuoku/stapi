import os, json

class Config(object):
  @staticmethod
  def load_auth_info():
    return json.load(
      open(
        os.path.dirname(__file__)+'/../conf/auth_info.json', 'r'
      )
    )
  
  @staticmethod
  def load_log():
    return json.load(
      open(
        os.path.dirname(__file__)+'/../conf/log.json', 'r'
      )
    )
