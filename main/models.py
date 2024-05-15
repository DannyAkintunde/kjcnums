from django.db import models
from django.contrib.auth.models import User

class Nums(models.Model):
    """Model definition for nums."""

    num = models.CharField(max_length=11,unique=True,null=False)
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    class Meta:
        """Meta definition for nums."""

        verbose_name = 'user'
        verbose_name_plural = 'Nums'

    def __str__(self):
        """Unicode representation of nums."""
        return f'{self.user}|{self.num}'

class Platform(models.Model):
    """Model definition for Platform."""

    platform = models.CharField(max_length=100)

    class Meta:
        """Meta definition for Platform."""

        verbose_name = 'Platform'
        verbose_name_plural = 'Platforms'

    def __str__(self):
        """Unicode representation of platform."""
        return f'{self.platform}'

class Sociallink(models.Model):
    """Model definition for Sociallinks."""

    link = models.CharField(max_length=300)
    platform = models.ForeignKey(Platform,on_delete=models.DO_NOTHING)
    text = models.CharField(max_length=35)
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    class Meta:
        """Meta definition for Sociallink."""

        verbose_name = 'Sociallink'
        verbose_name_plural = 'Sociallinks'

    def __str__(self):
        """Unicode representation of Sociallinks."""
        return f'{self.user}|{self.link}'

class Otherlink(models.Model):
    """Model definition for Otherlink."""

    link = models.CharField(max_length=200)
    display_text = models.CharField(max_length=35)
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    class Meta:
        """Meta definition for Otherlink."""

        verbose_name = 'Otherlink'
        verbose_name_plural = 'Otherlinks'

    def __str__(self):
        """Unicode representation of Otherlink."""
        return f'{self.display_text}|{str(self.link)[0:20]+'...'}'

class Category(models.Model):
    """Model definition for Category."""

    name = models.CharField(max_length=50)

    class Meta:
        """Meta definition for Category."""

        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        """Unicode representation of Category."""
        return '{}'.format(self.name ) # TODO

class Nin(models.Model):
    """Model definition for Non."""

    nin = models.CharField(max_length=100,unique=True)
    user = models.OneToOneField(User,on_delete=models.CASCADE)

    class Meta:
        """Meta definition for Nin."""

        verbose_name = 'NIN'
        verbose_name_plural = 'NiNs'

    def __str__(self):
        """Unicode representation of Nin."""
        return f'{self.nin}'

class Ristriction(models.Model):
    """Model definition for Ristriction."""

    types = models.TextChoices(value='all',names=(('All users','all'),('All except','except'),('Only','only')))
    type = models.CharField(choices=types,max_length=100)
    users = models.ManyToManyField(User,blank=True)

    class Meta:
        """Meta definition for Ristriction."""

        verbose_name = 'Ristriction'
        verbose_name_plural = 'Ristrictions'

    def __str__(self):
        """Unicode representation of Ristriction."""
        return f'{str(self.type)}'


class Userdata(models.Model):
    """Model definition for Userdata."""

    image = models.URLField(blank=True,null=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    gender = models.CharField(max_length=1,null=False)
    nums = models.ManyToManyField(Nums)
    category = models.ForeignKey(Category,on_delete=models.SET_NULL,null=True)
    sociallinks = models.ManyToManyField(Sociallink,blank=True)
    otherlinks = models.ManyToManyField(Otherlink,blank=True)
    nin = models.ForeignKey(Nin,on_delete=models.CASCADE,null=True,blank=True)
    ristrictions = models.OneToOneField(Ristriction,on_delete=models.SET_NULL,null=True)


    class Meta:
        """Meta definition for Userdata."""

        verbose_name = 'Userdata'
        verbose_name_plural = 'Usersdata'

    def __str__(self):
        """Unicode representation of Userdata."""
        return f'{self.user.username}|{self.gender}'
