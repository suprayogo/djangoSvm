from django.db import models

class UserProfile(models.Model):
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)

class Balita(models.Model):
    jenis_kelamin = models.CharField(max_length=10)
    usia = models.FloatField()
    berat_badan = models.FloatField()
    tinggi_badan = models.FloatField()
    status_gizi = models.CharField(max_length=20)

class BalitaDiskritis(models.Model):
    JENIS_KELAMIN_CHOICES = [
        ('Laki-laki', 'Laki-laki'),
        ('Perempuan', 'Perempuan'),
    ]

    STATUS_GIZI_CHOICES = [
        ('Gizi Buruk', 'Gizi Buruk'),
        ('Gizi Kurang', 'Gizi Kurang'),
        ('Gizi Normal', 'Gizi Normal'),
        ('Gizi Lebih', 'Gizi Lebih'),
    ]

    jenis_kelamin = models.CharField(max_length=10, choices=JENIS_KELAMIN_CHOICES)
    usia = models.FloatField()
    berat_badan = models.FloatField()
    tinggi_badan = models.FloatField()
    status_gizi = models.CharField(max_length=20, choices=STATUS_GIZI_CHOICES)

class BalitaPelatihan(models.Model):
    balita_diskritis = models.ForeignKey(BalitaDiskritis, on_delete=models.CASCADE)
    atribut_tambahan_pelatihan = models.CharField(max_length=255)  # Sesuaikan dengan atribut tambahan yang diperlukan

class BalitaPengujian(models.Model):
    balita_diskritis = models.ForeignKey(BalitaDiskritis, on_delete=models.CASCADE)
    atribut_tambahan_pengujian = models.CharField(max_length=255)  # Sesuaikan dengan atribut tambahan yang diperlukan
