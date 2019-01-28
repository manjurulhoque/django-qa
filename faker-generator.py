from django.contrib.auth.models import User
from faker import Faker
import random
from django_seed import Seed

from qaapp.models import Question

password = "pbkdf2_sha256$120000$pV6AiYYjHTsw$O6JzrM72XMpRTkrtXx5Q0crJTZjNoMRSY/UMtaDVuBA="

factory = Faker()

# Question.objects.all().delete()
# User.objects.all().delete()

# for i in range(1, 5):
#     user = User(username=factory.name(), email=factory.email(), password=password)
#     user.save()

# for i in range(1, 200):
#    question = Question(title=factory.text())
