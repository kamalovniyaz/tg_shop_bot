from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Subcategory(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Product(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    name = models.CharField("Название", max_length=255)
    description = models.TextField("Описание")
    price = models.DecimalField("Цена", max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField("Остаток товара")
    image_url = models.CharField(max_length=255)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Cart(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    user_id = models.IntegerField("Id пользователя", null=False)
    count = models.PositiveIntegerField("Кол-во товара")

    def __str__(self):
        return self.id
