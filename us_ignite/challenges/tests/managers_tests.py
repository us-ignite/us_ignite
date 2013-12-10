from dateutil.relativedelta import relativedelta
from nose.tools import eq_

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from us_ignite.challenges.models import Challenge
from us_ignite.challenges.tests import fixtures
from us_ignite.profiles.tests.fixtures import get_user


class TestActiveChallengesManager(TestCase):

    def tearDown(self):
        for model in [Challenge, User]:
            model.objects.all().delete()

    def test_active_chalenge_is_returned(self):
        user = get_user('us-ignite')
        start = timezone.now()
        end = start + relativedelta(days=2)
        data = {
            'user': user,
            'start_datetime': start,
            'end_datetime': end,
            'status': Challenge.PUBLISHED,
        }
        instance = fixtures.get_challenge(**data)
        eq_(list(Challenge.active.all()), [instance])

    def test_past_challenge_is_not_returned(self):
        user = get_user('us-ignite')
        start = timezone.now() - relativedelta(days=3)
        end = start + relativedelta(days=2)
        data = {
            'user': user,
            'start_datetime': start,
            'end_datetime': end,
            'status': Challenge.PUBLISHED,
        }
        fixtures.get_challenge(**data)
        eq_(list(Challenge.active.all()), [])

    def test_future_challenge_is_not_returned(self):
        user = get_user('us-ignite')
        start = timezone.now() + relativedelta(days=3)
        end = start + relativedelta(days=2)
        data = {
            'user': user,
            'start_datetime': start,
            'end_datetime': end,
            'status': Challenge.PUBLISHED,
        }
        fixtures.get_challenge(**data)
        eq_(list(Challenge.active.all()), [])

    def test_not_active_chalenge_is_not_returned(self):
        user = get_user('us-ignite')
        start = timezone.now()
        end = start + relativedelta(days=2)
        data = {
            'user': user,
            'start_datetime': start,
            'end_datetime': end,
            'status': Challenge.DRAFT,
        }
        fixtures.get_challenge(**data)
        eq_(list(Challenge.active.all()), [])