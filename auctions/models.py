from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    def __str__(self):
        return f"{self.username}"


class Goods(models.Model):
    title = models.CharField(max_length = 50, verbose_name="Товар")
    content = models.TextField(null = True, blank = True, verbose_name="Опис")
    price = models.FloatField(null = True, blank = True, verbose_name="Ціна")
    published = models.DateTimeField(auto_now_add = True, db_index = True, verbose_name="Опубліковано")
    image = models.ImageField(upload_to='images/', blank=True, verbose_name="Зображення")
    winner = models.ForeignKey(User, related_name="won_item", on_delete=models.SET_NULL, null=True, default=None)
    # rubric = models.ForeignKey('Rubric', null=True, on_delete=models.PROTECT, verbose_name='Рубрика')

    def delete(self, *args, **kwargs):
        # You have to prepare what you need before delete the model
        storage, path = self.image.storage, self.image.path
        # Delete the model before the file
        super(Goods, self).delete(*args, **kwargs)
        # Delete the file after the model
        storage.delete(path)
    

    def __str__(self):
        return f"{self.title}"

