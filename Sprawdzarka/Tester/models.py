from django.db import models


# Tabela z użytkownikami #

class Uzytkownicy(models.Model):
    # Id użytkownika
    identyfikator = models.CharField(max_length=20, primary_key=True)
    # Hasło zahashowane
    haslo = models.CharField(max_length=20)

    def __str__(self):
        return self.identyfikator

    class Meta:
        verbose_name = 'Uzytkownik'
        verbose_name_plural = 'Uzytkownicy'


# Dostepne zadanie #

class Zadania(models.Model):
    # 3-literowe ID
    identyfikator = models.CharField(max_length=3, primary_key=True)
    # Nazwa zadania
    nazwa = models.CharField(max_length=20)
    # Poziom trudnosci
    trudnosc = models.IntegerField()

    def __str__(self):
        return self.nazwa

    class Meta:
        verbose_name = 'Zadanie'
        verbose_name_plural = 'Zadania'


# Wysyłki użytkowników #

class Wysylki(models.Model):
    # ID zadania
    zadanie = models.ForeignKey(Zadania, on_delete=models.CASCADE)
    # ID użytkownika (kto wysłał)
    uzytkownik = models.ForeignKey(Uzytkownicy, on_delete=models.CASCADE)
    # Kiedy wysłano
    data = models.DateTimeField(null=True)
    # Raport sprawdzania
    raport = models.TextField(max_length=2000, null=True)

    def __str__(self):
        return str(self.pk)

    class Meta:
        verbose_name = 'Wysyłka'
        verbose_name_plural = 'Wysyłki'


