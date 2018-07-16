import pytz

from rest_framework.test import APIClient, APITestCase
from django.contrib.auth import get_user_model
from django.utils.timezone import datetime, timedelta

from .models import Task

User = get_user_model()

USERS_LIST = [
    {'username': 'TestUser1', 'password': 'qaz123'},
    {'username': 'TestUser2', 'password': '123zaq'},
    ]

TEST_TASK = [
    {'name': 'Test Task', 'content': 'Task Content'},
    {'name': 'Test Task 2', 'content': 'Task Content 1'},
    {'name': 'Test Task 3', 'content': 'Task Content 2'},
    {'name': 'Test Task 4', 'content': 'Task Content 3'}
]


def normalize_date(date):
    if not isinstance(date, datetime):
        return None
    return f'{date.day}/{date.month and "0"+str(date.month) or date.month}/{date.year}' \
           f' {date.hour}:{date.minute}:{date.second}'


class TestTasks(APITestCase):

    @classmethod
    def setUpClass(cls):
        return super().setUpClass()

    def setUp(self):
        self.user1 = User.objects.create_user(**USERS_LIST[0])
        self.user2 = User.objects.create_user(**USERS_LIST[1])

        self.client1 = APIClient()
        self.client2 = APIClient()

        for _ in zip(TEST_TASK, [self.user1, self.user1, self.user2, self.user2]):
            Task.objects.create(**_[0], owner=_[1], start=datetime.now(tz=pytz.UTC))

    def test_new_task_success(self):
        date = datetime.now(tz=pytz.UTC) + timedelta(days=1)

        data = {'name': 'New Task',
                'content': 'New Task Content',
                'start': date}
        self.client1.force_authenticate(user=self.user1)
        response = self.client1.post('/api/task/', data=data)

        self.assertEqual(response.status_code, 201)
        self.assertDictEqual({'name': 'New Task',
                              'content': 'New Task Content',
                              'owner': 'TestUser1',
                              'start': normalize_date(date),
                              'finished': None}, response.json())

    def test_new_task_fail_bad_date(self):

        data = {'name': 'Task with date in past',
                'content': 'Task with date in past',
                'start': datetime(1999, 1, 1, 21, 37)}

        self.client1.force_authenticate(user=self.user1)
        response = self.client1.post('/api/task/', data=data)

        self.assertEqual(response.status_code, 400)

    def test_new_task_fail_unauth(self):
        date = datetime.now(tz=pytz.UTC) + timedelta(days=1)

        data = {'name': 'Task unauthenticated user',
                'content': 'Task unauthenticated user',
                'start': normalize_date(date)}

        response = self.client1.post('/api/task/', data=data)

        self.assertEqual(response.status_code, 401)

    def test_list_task(self):
        self.client1.force_authenticate(self.user1)
        response = self.client1.get('/api/task/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(2, len(response.json()))

    def test_edit_task_success(self):
        self.client1.force_authenticate(self.user1)
        response = self.client1.patch('/api/task/1/', data={'finished': datetime.now()})

        self.assertEqual(response.status_code, 200)

    def test_edit_task_fail_unauth(self):
        response = self.client1.patch('/api/task/1/', data={'finished': datetime.now()})

        self.assertEqual(response.status_code, 401)

    def test_edit_task_fail_not_owner(self):
        self.client1.force_authenticate(self.user1)
        response = self.client1.patch('/api/task/3/', data={'finished': datetime.now()})

        self.assertEqual(response.status_code, 403)

    def test_task_details_success(self):
        self.client1.force_authenticate(self.user1)
        response = self.client1.get('/api/task/1/')

        self.assertEqual(response.status_code, 200)

    def test_task_detail_fail_non_exist(self):
        self.client1.force_authenticate(self.user1)
        response = self.client1.get('/api/task/999/')

        self.assertEqual(response.status_code, 404)

    def test_delete_task_success(self):
        self.client1.force_authenticate(self.user1)
        response = self.client1.delete('/api/task/1/')

        self.assertEqual(response.status_code, 204)

    def test_delete_task_fail_non_exist(self):
        self.client1.force_authenticate(self.user1)
        response = self.client1.delete('/api/task/999/')

        self.assertEqual(response.status_code, 404)

    def test_delete_task_fail_unauth(self):
        response = self.client1.delete('/api/task/1/')

        self.assertEqual(response.status_code, 401)

    def test_delete_task_fail_not_owner(self):
        self.client1.force_authenticate(self.user1)
        response = self.client1.delete('/api/task/3/')

        self.assertEqual(response.status_code, 403)
