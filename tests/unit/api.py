"""Unit tests for api.py"""

from haas import model, api
from haas.test_common import newDB, releaseDB
import pytest


class TestGroup:
    """Tests for the haas.api.group_* functions."""

    def test_group_add_user(self):
        db = newDB()
        api.user_create('alice', 'secret')
        api.group_create('acme-corp')
        api.group_add_user('acme-corp', 'alice')
        releaseDB(db)

    def test_group_remove_user(self):
        db = newDB()
        api.user_create('alice', 'secret')
        api.group_create('acme-corp')
        api.group_add_user('acme-corp', 'alice')
        api.group_remove_user('acme-corp', 'alice')
        releaseDB(db)


class TestUser:
    """Tests for the haas.api.user_* functions."""

    def test_new_user(self):
        db = newDB()
        api._assert_absent(db, model.User, 'bob')
        api.user_create('bob', 'foo')
        releaseDB(db)

    def test_duplicate_user(self):
        db = newDB()
        api.user_create('alice', 'secret')
        with pytest.raises(api.DuplicateError):
                api.user_create('alice', 'password')
        releaseDB(db)

    def test_delete_user(self):
        db = newDB()
        api.user_create('bob', 'foo')
        api.user_delete('bob')
        releaseDB(db)

    def test_delete_missing_user(self):
        db = newDB()
        with pytest.raises(api.NotFoundError):
            api.user_delete('bob')
        releaseDB(db)

    def test_delete_user_twice(self):
        db = newDB()
        api.user_create('bob', 'foo')
        api.user_delete('bob')
        with pytest.raises(api.NotFoundError):
            api.user_delete('bob')
        releaseDB(db)
