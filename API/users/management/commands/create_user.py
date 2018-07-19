import argparse

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):

    def handle(self, *args, **options):
        if options['is_superuser'] and options['is_superuser'] == 1:
            User.objects.create_superuser(username=options['username'], password=options['password'], email=options['email'])
        else:
            User.objects.create_user(username=options['username'], password=options['password'], email=options['email'])
			
    def add_arguments(self, parser):
        parser.add_argument('username', type=str)
        parser.add_argument('password', type=str)
        parser.add_argument('email', type=str)
        parser.add_argument('is_superuser', type=int, nargs='?', default=0)
