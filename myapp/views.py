from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import  login, logout
from django.contrib.auth.models import User 
from .forms import LoginForm
from django.contrib import messages
from django.contrib.auth import logout
from sklearn.metrics import classification_report
from .models import Balita
from .models import BalitaDiskritis, BalitaPelatihan, BalitaPengujian
from django.core.files.storage import FileSystemStorage
import csv
from sklearn.model_selection import train_test_split
from django.conf import settings
from django.http import HttpResponse
from datetime import datetime
import csv
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from .forms import UploadCSVForm
import os
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
import joblib 
from django.views.decorators.csrf import csrf_protect
from .forms import SimpleRegisterForm

def register(request):
    if request.method == 'POST':
        form = SimpleRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SimpleRegisterForm()
    return render(request, 'base/register.html', {'form': form})


@login_required(login_url='login')  
def home(request):
    return render(request, 'base/home.html')

def data_awal(request):
    return render(request, 'base/data_awal.html')


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user_exists = User.objects.filter(username=username, password=password).exists()
            if user_exists:  
                user = User.objects.get(username=username)
                login(request, user)
                return redirect('home')  
            else:     
                messages.error(request, 'Username atau Password Salah.')
    else:
        form = LoginForm()
    return render(request, 'base/login.html', {'form': form})

def user_logout(request):
    logout(request)
    response = redirect('login')
    response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response['Expires'] = '{} GMT'.format(datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S'))
    return response



def data_awal(request):
    data_balita = Balita.objects.all()

    if request.method == 'POST':
        data_awal_csv = request.FILES.get('data_awal')

        if not data_awal_csv.name.endswith('.csv'):
            messages.info(request, 'Format file salah')
            return render(request, 'base/data_awal.html', {'data_balita': data_balita})

        media_root = settings.MEDIA_ROOT
        custom_folder = 'folder_penyimpanan_kustom'
        custom_folder_path = os.path.join(media_root, custom_folder)

        os.makedirs(custom_folder_path, exist_ok=True)
        file_path = os.path.join(custom_folder_path, data_awal_csv.name)

        with open(file_path, 'wb') as destination:
            for chunk in data_awal_csv.chunks():
                destination.write(chunk)

        with open(file_path, newline='') as csv_file:
            csv_reader = csv.DictReader(csv_file)

            for row in csv_reader:
              
                balita_instance = Balita(
                    jenis_kelamin=row['jenis_kelamin'],
                    usia=int(float(row['usia'])),
                    berat_badan=int(float(row['berat_badan'])),
                    tinggi_badan=int(float(row['tinggi_badan'])),
                    status_gizi=row['status_gizi']
                )
                balita_instance.save()

                jenis_kelamin_mapping = {'laki-laki': 1, 'perempuan': 2, 'laki laki': 1}
                jenis_kelamin_diskritis = jenis_kelamin_mapping.get(row['jenis_kelamin'].replace(" ", "").lower(), 0)

                status_gizi_mapping = {'gizi_buruk': 1, 'gizi_kurang': 2, 'gizi_normal': 3,'normal': 3, 'gizi_lebih': 4,
                               'gizi buruk': 1, 'gizi kurang': 2, 'gizi normal': 3, 'gizi lebih': 4}
                status_gizi_diskritis = status_gizi_mapping.get(row['status_gizi'].replace(" ", "").lower(), 0)

            
                balita_diskritis = BalitaDiskritis(
                    jenis_kelamin=jenis_kelamin_diskritis,
                    usia=int(float(row['usia'])),
                    berat_badan=int(float(row['berat_badan'])),
                    tinggi_badan=int(float(row['tinggi_badan'])),
                    status_gizi=status_gizi_diskritis
                )
                balita_diskritis.save()

        messages.success(request, 'File CSV berhasil diunggah dan data disimpan.')
        return render(request, 'base/data_awal.html', {'data_balita': data_balita})

    return render(request, 'base/data_awal.html', {'data_balita': data_balita})

def diskritisasi(request):
    data_balita_diskritis = BalitaDiskritis.objects.all()
    return render(request, 'base/diskritisasi.html', {'data_balita_diskritis': data_balita_diskritis})

 


def proses_bagi_data(request):
    if request.method == 'POST':
    
        data_balita_diskritis = BalitaDiskritis.objects.all()

    
        X = [[balita.jenis_kelamin, balita.usia, balita.berat_badan, balita.tinggi_badan] for balita in data_balita_diskritis]
        y = [balita.status_gizi for balita in data_balita_diskritis]

      
        total_data = len(data_balita_diskritis)
        persentase_data_pelatihan = 0.8
        ukuran_data_pelatihan = int(total_data * persentase_data_pelatihan)

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=1 - persentase_data_pelatihan, random_state=42)

     
        for i in range(len(X_train)):
            balita_pelatihan = BalitaPelatihan(
                balita_diskritis=data_balita_diskritis[i],
                atribut_tambahan_pelatihan='Atribut Pelatihan',  
            )
            balita_pelatihan.save()

  
        for i in range(len(X_test)):
            balita_pengujian = BalitaPengujian(
                balita_diskritis=data_balita_diskritis[i],
                atribut_tambahan_pengujian='Atribut Pengujian',  
            )
            balita_pengujian.save()

        return render(request, 'base/pembagian_data.html', {'data_balita_diskritis': data_balita_diskritis})

    return render(request, 'base/pembagian_data.html')
  


def pembagian_data(request):
 
    data_balita_pelatihan = BalitaPelatihan.objects.all()
    data_balita_pengujian = BalitaPengujian.objects.all()

    return render(request, 'base/pembagian_data.html', {
        'data_balita_pelatihan': data_balita_pelatihan,
        'data_balita_pengujian': data_balita_pengujian,
    })


def klasifikasi(request):
    data_balita_diskritis = BalitaDiskritis.objects.all()

    X = [[balita.jenis_kelamin, balita.usia, balita.berat_badan, balita.tinggi_badan] for balita in data_balita_diskritis]
    y = [balita.status_gizi for balita in data_balita_diskritis]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=100)

    model_svm = SVC(kernel='linear')  

    model_svm.fit(X_train, y_train)

    y_pred = model_svm.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average='weighted')  
    recall = recall_score(y_test, y_pred, average='weighted')  
    f1 = f1_score(y_test, y_pred, average='weighted')  



    print(f'Accuracy of SVM model on test data: {accuracy}')
    print(f'Precision of SVM model on test data: {precision}')
    print(f'Recall of SVM model on test data: {recall}')
    print(f'F1 Score of SVM model on test data: {f1}')

    return render(request, 'base/klasifikasi.html', {'accuracy': accuracy, 'precision': precision, 'recall': recall, 'f1': f1})




def tampilkan_form_uji_data(request):
    return render(request, 'base/uji_data.html')



def uji_data(request):
   
    jenis_kelamin = float(request.POST.get('jenis_kelamin'))
    usia = float(request.POST.get('usia'))
    berat_badan = float(request.POST.get('berat_badan'))
    tinggi_badan = float(request.POST.get('tinggi_badan'))

    
    data_uji = [[jenis_kelamin, usia, berat_badan, tinggi_badan]]

   
    data_balita_diskritis = BalitaDiskritis.objects.all()

  
    X = [[balita.jenis_kelamin, balita.usia, balita.berat_badan, balita.tinggi_badan] for balita in data_balita_diskritis]
    y = [balita.status_gizi for balita in data_balita_diskritis]

    # Split data menjadi data latihan dan data uji
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Normalisasi data menggunakan StandardScaler
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(data_uji)

    # Inisialisasi dan latih model SVM
    svm_model = SVC(kernel='linear', C=1.0)
    svm_model.fit(X_train_scaled, y_train)

    # Lakukan prediksi untuk data uji
    hasil_prediksi = svm_model.predict(X_test_scaled)
    print("hasil prediksi :",hasil_prediksi)
    return render(request, 'base/uji_data.html', {'hasil_prediksi': hasil_prediksi[0]})

