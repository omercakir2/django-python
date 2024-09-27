from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class MemberManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field is required')
        email = self.normalize_email(email)# makes all the characters lowercase
        user = self.model(email=email, **extra_fields)
        user.set_password(password)# makes the password to be more securely stored in Db
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class Member(AbstractBaseUser, PermissionsMixin):# AbstractBaseUser does the work that gives us 
    #the chance to customise the current Djjango user models which only includes username and password
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    profile_picture = models.ImageField(upload_to='profile_pics/', default='default.jpg')
    

    objects = MemberManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email
class Friendship(models.Model):
    from_user = models.ForeignKey(Member, related_name='following', on_delete=models.CASCADE)
    to_user = models.ForeignKey(Member, related_name='followers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    # on_delete=models.CASCADE means that when the user is deleted the all records about the user
    # is also going to be deleted
    
    class Meta:
        unique_together = ('from_user', 'to_user')

    def __str__(self):
        return f"{self.from_user} follows {self.to_user}"
    
    
# the actual code that being exucuted is this:
# CREATE TABLE "members_member" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "firstname" varchar(255) NOT NULL, "lastname" varchar(255) NOT NULL); COMMIT;

    
    

