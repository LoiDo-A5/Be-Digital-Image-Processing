
from accounts.models import User
import factory

from common.tests.factory_base import FactoryBase


class UserFactory(FactoryBase):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'email{n}@io')
    birthday = factory.Faker('date')
    phone_number = factory.Sequence(lambda n: str(n).zfill(10))
    is_phone_verified = True
    email = factory.Sequence(lambda n: f'email{n}@io')
    name = factory.Faker('name')
    password = factory.Faker('password')
    time_zone = 'Asia/Ho_Chi_Minh'

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        user = super(UserFactory, cls)._create(model_class, *args, **kwargs)
        password = kwargs['password']
        user.set_password(password)
        user.raw_password = password
        user.save()
        return user