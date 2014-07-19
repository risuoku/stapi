from stapi.api import API
import nose.tools

class TestAPI(object):
  def __init__(self):
    self.api = API()

  def test_get_user(self):
    self.api.get_user(id=2454470028)

  def test_favorites(self):
    self.api.favorites(id=2454470028)

  def test_friends_ids(self):
    self.api.friends_ids(id=2454470028)

  def test_home_timeline(self):
    self.api.home_timeline()

  def test_user_timeline(self):
    self.api.user_timeline(id=2454470028)

  def test_mentions_timeline(self):
    self.api.mentions_timeline()

  def test_lists_all(self):
    self.api.lists_all(user_id=2454470028)

  def test_lists_memberships(self):
    self.api.lists_memberships(user_id=2454470028)

  def test_lists_subscriptions(self):
    self.api.lists_subscriptions(user_id=2454470028)

  def test_lists_timeline(self):
    self.api.list_timeline(owner_id=2454470028, list_id=158797307)

  def test_get_list(self):
    self.api.get_list(owner_id=2454470028, list_id=158797307)

  def test_list_members(self):
    self.api.list_timeline(owner_id=2454470028, list_id=158797307)

  def test_show_list_member(self):
    self.api.list_timeline(owner_id=2454470028, list_id=158797307)
