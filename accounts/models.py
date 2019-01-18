from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils import timezone

GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female')
)

class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, phone, password, **extra_fields):
        """Create and save a User with the given phone and password."""
        if not phone:
            raise ValueError('The given phone must be set')
        # phone = self.phone
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone, password=None, **extra_fields):
        """Create and save a regular User with the given phone and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(phone, password, **extra_fields)

    def create_superuser(self, phone, password, **extra_fields):
        """Create and save a SuperUser with the given phone and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(phone, password, **extra_fields)


class User(AbstractUser):
    is_client = models.BooleanField(default=False)
    is_server = models.BooleanField(default=False)
    username = None
    email = None
    name = models.CharField(max_length=100, blank=False, null=False)
    phone = models.CharField(max_length=11, unique=True)
    gender = models.CharField(max_length=50, choices=GENDER_CHOICES, default='M')
    birth_date = models.DateField(default=timezone.now)
    joined_date = models.DateField(auto_now_add=True, editable=False)
    address = models.TextField(max_length=1024, blank=False, null=False)
    image = models.ImageField(blank=True, null=True)
    USERNAME_FIELD = 'phone'

    REQUIRED_FIELDS = []
    objects = UserManager()


class Category(models.Model):
    category_name=models.CharField(max_length=100, null=False, blank=False)
    img = models.ImageField(blank=False, null=False, default='')
    def __str__(self):
        return self.category_name

class Client(User, models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='client')

    def __str__(self):
        return self.name


class Server(User, models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='server')
    clients=models.ManyToManyField(Client,related_name='clients')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    experience = models.TextField(max_length=500, blank=True, null=True)
    ratings = models.IntegerField(blank=True, null=True, default=0,
                                  validators=[MinValueValidator(0), MaxValueValidator(5)])
    number_of_rating = models.IntegerField(default=0)
    total_rating = models.IntegerField(default=0)
    avg_rate=models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def __str__(self):
        return self.name


