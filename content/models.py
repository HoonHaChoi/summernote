from django.db import models
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.contrib.auth import settings


from datetime import date,timedelta
from account.models import user




def date_check(value):
    if date.today() > value:
            raise ValidationError("지난 날짜는 선택할수 없습니다")
    else:
        return value

class Post(models.Model):
    author = models.ForeignKey(user, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()

    user_max_count = models.PositiveIntegerField(default=0)
    user_count = models.PositiveIntegerField(default=0)     #삭제

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    deadline = models.DateField(validators=[date_check])

    users = models.ManyToManyField(user, related_name='post_users',through='Apply')

    def __str__(self):
        return self.title

    def deta(self):
        return date.today() > self.deadline
    #기간 체크
    def date_overlap(self):
        return self.deadline < date.today()

    #인원 체크
    def count_overlap(self):
        return  self.total_user() >= self.user_max_count

    #유저수 체크
    def total_user(self):
        return self.users.count()

    def get_absolute_url(self):
        return reverse('detail', args=[self.id])


    #
    # def user_apply_check(self,pk):
    #     apply_user = Apply.objects.get(post_id=pk)
    #     if apply_user.objects.filter(user_id=self.request.user.id):


    # def count_overlap(self):
    #     if self.user_count < self.user_max_count:
    #         return ValueError("넘지 못함")

#
class Apply(models.Model):
    user = models.ForeignKey(user ,on_delete=models.CASCADE)
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    date_joined = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s %s" %(self.user, self.post)


class Comment(models.Model):
    user = models.ForeignKey(user, on_delete = models.CASCADE)
    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    context = models.CharField(max_length=40)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.context



class Chatroom(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL ,on_delete=models.CASCADE)

    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message