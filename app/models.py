from django.db import models
from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.urls import reverse

#title
#create_data
#update_data
#description
#price
#auction

# Create your models here.

User = get_user_model()

class Advertisement(models.Model):
    user = models.ForeignKey(User, verbose_name="пользователь", on_delete=models.CASCADE)
    title = models.CharField("Название", max_length=128)
    description = models.TextField("Описание")
    price = models.DecimalField("Цена", max_digits=10, decimal_places=2)
    auction = models.BooleanField("Торг", help_text="Отметье, если торг уместен")
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    image = models.ImageField("Изображение", upload_to="hello/")

    def get_absolute_url(self):
        return reverse("adv-detail", kwargs={'pk': self.pk})

    def __str__(self):
        return f"Advertisement(id={self.id}, title={self.title}, price={self.price})"
    
    class Meta:
        db_table = "advertisement"


    @admin.display(description="Дата создания")
    def created_date(self):
        from django.utils import timezone, html
        if self.created_at.date() == timezone.now().date():
            created_time = self.created_at.time().strftime("%H:%M:%S")
            return html.format_html(
                "<span style='color:green; font-weight: bold;'> Сегодня в {} </span>", created_time
            )
        return self.created_at.strftime("%d.%m.%y в %H:%M:%S")

    @admin.display(description="Дата обновления")
    def updated_date(self):
        from django.utils import timezone, html
        if self.updated_at.date() == timezone.now().date():
            updated_time = self.updated_at.time().strftime("%H:%M:%S")
            # тэг - это элемент в html
            # тэг span - односрочный текст
            return html.format_html(
                "<span style='color:graeen; font-weight: bold;'> Сегодня в {} </span>", updated_time
            )
        return self.updated_at.strftime("%d.%m.%y в %H:%M:%S")
    
    @admin.display(description="изображение")
    def img_view(self):
        from django.utils import timezone, html
        return html.format_html("<img src='{}' style='width:50px; height:50px' alt ='not loaded'/>", self.image.url)
    
