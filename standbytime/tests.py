from django.test import TestCase, RequestFactory
from .views import standbytime
from django.contrib.auth.models import User
from faker import Faker
from django.contrib.auth.hashers import make_password
from django.shortcuts import resolve_url

# Create your tests here.
class StandbytimeModelTest(TestCase):
    def setUp(self):
        self.fake_ja = Faker("ja_JP")

    def setup_is_dummyuser(self, fake, N, M, su):
        users = []
        for i in range(N, M + 1):
            dummy_deta = fake.profile()
            users.append(
                User.objects.create(
                    id=i,
                    username=dummy_deta["username"],
                    first_name=dummy_deta["name"].split()[1],
                    last_name=dummy_deta["name"].split()[0],
                    email=dummy_deta["mail"],
                    is_superuser=su,
                    is_staff=False,
                    is_active=True,
                    date_joined=self.fake_ja.date_time_ad(),
                    last_login=self.fake_ja.date_time_ad(),
                    password=make_password(self.fake_ja.password(length=10)),
                )
            )
        return users

    def test_is_standbytime_view(self):
        response = self.client.get(
            resolve_url("standbytime:standbytime", "TDR", "ビッグサンダー・マウンテン", 160)
        )
        rf = RequestFactory()
        request = rf.get(
            resolve_url("standbytime:standbytime", "TDR", "ビッグサンダー・マウンテン", 160)
        )
        user = self.setup_is_dummyuser(self.fake_ja, 1, 1, False)[0]
        request.user = user
        response = standbytime(request)
        self.assertEqual(200, response.status_code)
        self.assertContains(response, "待ち時間解析")

