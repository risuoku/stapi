#!/usr/bin/python
# -*- coding: utf-8 -*-

import tweepy
import re, sys
import logging
from stapi.config import Config
from stapi.error import StError
from stapi.logger import Logger

class API(object):
  def __init__(self):
    auth_info_list = Config.load_auth_info()
    self.logger = Logger()

    # mutable -----------
    self.api_list = map(self._get_authorized_api, auth_info_list)
    self.index = 0
    self.count = 0
    # --------------------

  def __getattr__(self, name):
    return MethodMissing(self, name)
  
  ### private
  def _get_authorized_api(self, auth_info):
    auth = tweepy.OAuthHandler(auth_info['consumer_key'], auth_info['consumer_secret'])
    auth.set_access_token(auth_info['access_token'], auth_info['access_token_secret'])
    return tweepy.API(auth)

class MethodMissing(object):
  def __init__(self, stapi, name):
    self.stapi = stapi 
    self.name = name

  def __call__(self, *arg, **kw):
    while True:
      try:
        api = self.stapi.api_list[self.stapi.index]
        call = getattr(api, self.name)
        r = call(**kw)
        self.stapi.count = 0
        return r
      except tweepy.TweepError, e:
        if not self._rate_limit_exceeded(e.reason):
          raise e
        if self.stapi.count > len(self.stapi.api_list):
          raise StError('stapi rate limit exceeded!')
        self.stapi.logger.debug('switch api.. index:%s'%(self.stapi.index))
        self.stapi.count += 1
        self.stapi.index = (self.stapi.index+1)%(len(self.stapi.api_list))
  
  def _rate_limit_exceeded(self, s):
    return re.search('Rate limit exceeded', s)
