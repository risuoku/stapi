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
    self.api_list = [self._set_token(auth_info) for auth_info in auth_info_list]
    self.index = 0
    self.count = 0
    # --------------------

  def get_user(self, id=None, screen_name=None):
    return self._call(
      name = 'get_user', 
      args = {'id':id, 'screen_name':screen_name}
    )

  def favorites(self, id=None, count=None):
    return self._call(
      name = 'favorites',
      args = {'id':id, 'count':count}
    )

  def friends_ids(self, id=None, user_id=None, screen_name=None, cursor=None):
    return self._call(
      name = 'friends_ids',
      args = {'id':id, 'user_id':user_id, 'screen_name':screen_name, 'cursor':cursor}
    )

  def home_timeline(self, since_id=None, max_id=None, count=None):
    return self._call(
      name = 'home_timeline',
      args = {'since_id':since_id, 'max_id':max_id, 'count':count}
    )
  
  def user_timeline(self, id=None, user_id=None, screen_name=None, since_id=None, max_id=None, count=None, include_rts=None):
    return self._call(
      name = 'user_timeline',
      args = {'id':id, 'user_id':user_id, 'screen_name':screen_name, 'since_id':since_id, 'max_id':max_id, 'count':count, 'include_rts':include_rts}
    )
  
  def mentions_timeline(self, since_id=None, max_id=None, count=None):
    return self._call(
      name = 'mentions_timeline',
      args = {'since_id':since_id, 'max_id':max_id, 'count':count}
    )
  
  def create_list(self, name=None, mode=None, description=None):
    return self._call(
      name = 'create_list',
      args = {'name':name, 'mode':mode, 'description':description}
    )
  
  def lists_all(self, screen_name=None, user_id=None):
    return self._call(
      name = 'lists_all',
      args = {'screen_name':screen_name, 'user_id':user_id}
    )
  
  def lists_memberships(self, screen_name=None, user_id=None, filter_to_owned_lists=None, cursor=None):
    return self._call(
      name = 'lists_memberships',
      args = {'screen_name':screen_name, 'user_id':user_id, 'filter_to_owned_lists':filter_to_owned_lists, 'cursor':cursor}
    )
  
  def lists_subscriptions(self, screen_name=None, user_id=None, cursor=None):
    return self._call(
      name = 'lists_subscriptions',
      args = {'screen_name':screen_name, 'user_id':user_id, 'cursor':cursor}
    )
  
  def list_timeline(self, owner_screen_name=None, slug=None, owner_id=None, list_id=None, since_id=None, max_id=None, count=None, include_rts=None, page=None):
    return self._call(
      name = 'list_timeline',
      args = {'owner_screen_name':owner_screen_name, 'slug':slug, 'owner_id':owner_id, 'list_id':list_id, 'since_id':since_id, 'max_id':max_id, 'count':count, 'include_rts':include_rts, 'page':page}
    )
  
  def get_list(self, owner_screen_name=None, owner_id=None, slug=None, list_id=None):
    return self._call(
      name = 'get_list',
      args = {'owner_screen_name':owner_screen_name, 'owner_id':owner_id, 'slug':slug, 'list_id':list_id}
    )
  
  def list_members(self, owner_screen_name=None, slug=None, list_id=None, owner_id=None, cursor=None):
    return self._call(
      name = 'list_members',
      args = {'owner_screen_name':owner_screen_name, 'slug':slug, 'list_id':list_id, 'owner_id':owner_id, 'cursor':cursor}
    )
  
  def show_list_member(self, owner_screen_name=None, slug=None, list_id=None, owner_id=None, user_id=None, screen_name=None):
    return self._call(
      name = 'show_list_member',
      args = {'owner_screen_name':owner_screen_name, 'slug':slug, 'list_id':list_id, 'owner_id':owner_id, 'user_id':user_id, 'screen_name':screen_name}
    )
  
  # template
  def _template_(self):
    return self._call(
      name = '',
      args = {}
    )
  
  ### private
  def _set_token(self, auth_info):
    auth = tweepy.OAuthHandler(auth_info['consumer_key'], auth_info['consumer_secret'])
    auth.set_access_token(auth_info['access_token'], auth_info['access_token_secret'])
    return tweepy.API(auth)

  def _call(self, name=None, args=None):
    while True:
      try:
        api = self.api_list[self.index]
        call = getattr(api, name)
        r = call(**args)
        self.count = 0
        return r
      except tweepy.TweepError, e:
        if not self._rate_limit_exceeded(e.reason):
          raise e
        if self.count > len(self.api_list):
          raise StError('stapi rate limit exceeded!')
        self.logger.debug('switch api.. index:%s'%(self.index))
        self.count += 1
        self.index = (self.index+1)%(len(self.api_list))
  
  def _rate_limit_exceeded(self, s):
    return re.search('Rate limit exceeded', s)
