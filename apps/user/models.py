from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.fields.files import ImageFieldFile
import os
from tiku.settings import MEDIA_ROOT, THUMB_SIZE
from lib.images import make_thumb


# Create your models here.


class User(AbstractUser):
    real_name = models.CharField(max_length=20, verbose_name="真实姓名")
    mobile = models.CharField(max_length=11, verbose_name="手机号码")
    qq = models.CharField(max_length=11, verbose_name="qq号码")
    avator = models.ImageField(upload_to="avator/%Y%M%D", default="avator/default.jpg", verbose_name="头像")
    avator_sm = models.ImageField("头像缩略图", upload_to="avator/%Y%M%D/", default='avator/default_sm.jpg')

    def save(self, *args, **kwargs):
        super().save()
        if self.avator.name == 'avator/default.jpg':
            return
        base, ext = os.path.splitext(self.avator.name)
        thumb_pixbuf = make_thumb(os.path.join(MEDIA_ROOT, self.avator.name), size=THUMB_SIZE)
        thumb_path = os.path.join(MEDIA_ROOT, base + f'.{THUMB_SIZE}x{THUMB_SIZE}' + ext)
        relate_thumb_path = os.path.join('/'.join(self.avator.name.split('/')[:-1]), os.path.basename(thumb_path))
        relate_thumb_path = base + f'.{THUMB_SIZE}x{THUMB_SIZE}' + ext
        thumb_pixbuf.save(thumb_path)
        self.avator_sm = ImageFieldFile(self, self.avator_sm, relate_thumb_path)
        super().save()  # 再保存一下，包括缩略图等

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.real_name
