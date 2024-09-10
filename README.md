# Tugas 2: Pengenalan Aplikasi Django dan Model-View-Template (MVT) pada Django

- Nama: Muhammad Afwan Hafizh
- NPM: 2306208855
- Kelas: PBP-F

Link deploy: [masih belum bisa diakses karena pws rungkad t_t](http://muhammad-afwan-ameloops.pbp.cs.ui.ac.id/)

Berikut adalah langkah-langkah yang saya lakukan untuk mengimplementasikan poin-poin dalam checklist:

## Membuat proyek Django baru
   1. Buat atau cari suatu direktori sebagai tempat untuk mengembangkan proyek.
      
   2. Lalu, buat virtual environment dengan menggunakan command
      ```
      python -m venv env
      ```
      Virtual environment ini bertujuan untuk mengikat/mengisolasi dependensi pada suatu module yang digunakan dalam membangun suatu proyek agar tidak bertabrakan dengan sistem lainnya yang bersifat global.
      
   3. Aktifkan virtual environment dengan menggunakan command
      ```
      .\env\Scripts\activate
      ```
      Virtual environment yang aktif, akan ditandai dengan adanya (env) pada terminal.
      
   4. Setelah virtual environment aktif, lakukan instalasi django, gunicorn, whitenoise, psycopg2-binary, requests, dan urllib3. Berikut sedikit penjelasan mengenai django, gunicorn, dan lainnya:
      - django = Web framework berbasis python yang menyediakan fitur Object Relation Model, routing URL, dan autentikasi dengan konsep Model-View-Template
      - gunicorn = Server app untuk menjalankan app python seperti django (WSGI HTTP Server).
      - whitenoise = Library python yang melayani file-file statis seperti file gambar (contoh: format png), css, javascript, dan lainnya.
      - psycopg2-binary = Digunakan untuk menghubungkan django app dengan database PostgreSQL.
      - requests = Library python untuk membuat permintaan HTTP.
      - urllib3 = Library python untuk membuat permintaan HTTP tetapi dengan cakupan kontrol yang lebih luas.
    
      Pada tutorial 0 di PBP, salah satu cara untuk melakukan instalasi adalah dengan membuat file baru bernama requirements.txt yang berisi
      ```
      django
      gunicorn
      whitenoise
      psycopg2-binary
      requests
      urllib3
      ```
      lalu jalankan command
      ```
      pip install -r requirements.txt
      ```
      Alternatif lainnya untuk melakukan semua instalasi tersebut tanpa harus membuat file requirements.txt, maka dapat jalankan command
      ```
      pip install django gunicorn whitenoise psycopg2-binary requests urllib3
      ```
      
   5. Apabila instalasi sudah selesai, maka buat proyek djangonya. Proyek saya bernama "ameloops" maka commandnya
      ```
      django-admin startproject ameloots .
      ```
      
   6. Setting konfigurasi pada proyek yang baru dibangun. Tambahkan string ```localhost``` dan ```127.0.0.1``` pada ```ALLOWED_HOSTS``` yang terletak pada ```settings.py``` dalam direktori dengan nama proyek yang sebelumnya dibuat.
      ```
      ...
      ALLOWED_HOSTS = ["localhost", "127.0.0.1"]
      ...
      ```
      Dengan penambahan string ```localhost``` dan ```127.0.0.1``` pada ```ALLOWED_HOSTS```, artinya saya mengizinkan akses pada host lokal dan IP yang merujuk pada device saya sendiri. Apabila saya ingin melakukan deploy pada suatu server, maka saya bisa tambahkan host dari server tersebut pada ```ALLOWED_HOSTS```.
      
## Membuat aplikasi main
   1. Untuk membuat suatu app baru dengan nama ```main```, maka jalankan command
      ```
      python manage.py startapp main
      ```
      Berbeda dengan command ```django-admin startproject ameloots .``` yang menjadi kerangka utama dan melakukan konfigurasi yang diperlukan dalam menjalankan django, command ```python manage.py startapp main``` akan membuat app baru yang akan berfokus pada kumpulan fitur tertentu seperti shop, blog, dan lain-lain.

   2. Setelah membuat app main, maka tambahkan string ```'main'``` pada ```INSTALLED_APPS``` di ```settings.py``` pada direktori proyek. Fungsi pada penambahan string ```'main'``` pada ```INSTALLED_APPS``` berfungsi untuk menambahkan aplikasi pada yaitu ```'main'``` pada daftar aplikasi di proyek django.

## Melakukan routing pada proyek agar dapat menjalankan aplikasi main.
   1. Pergi ke ```views.py``` yang ada pada direktori main.
      
   2. Lalu, buat code seperti berikut
      ```
      from django.shortcuts import render

      def show_main(request):
          context = {
              'npm' : '2306208855',
              'name': 'Muhammad Afwan Hafizh',
              'class': 'PBP F',
              'app_name': 'Ameloops',
          }
          return render(request, "main.html", context)
      ```
      - Fungsi render pada line ```from django.shortcuts import render``` berguna untuk menggabungkan template HTML dengan konteks data di code.
      - ```def show_main(request):``` berfungsi dalam mendefinisikan fungsi view ```show_main``` yang menerima satu argumen yaitu request.
      - ```context = {...}```, konteks data yang dibuat dalam tipe data dictionary
      - ```return render(request, "main.html", context)```, berfungsi untuk memberikan konteks dari request HTTP, me-render template ```main.html```, dan memberikan konteks data yang telah diberikan pada code.
  
   3. Setelah membuat code pada ```views.py```, maka buat berkas ```urls.py``` pada direktori main.

   4. Lalu, setup routing URL ```main``` dengan buat code seperti berikut
      ```
      from django.urls import path
      from . import views
      
      app_name = 'main'
      
      urlpatterns = [
          path('', views.show_main, name='show_main'),
      ]
      ```
      Secara garis besar, code ini mengartikan apabila user mengunjungi URL yang sesuai (URL root dari aplikasi main), maka django akan mencocokkan URL tersebut dengan pola yang ada di urlpatterns. URL root ('') akan cocok dengan path('', views.show_main, name='show_main'), sehingga django akan memanggil fungsi ```show_main``` dari ```views.py``` untuk menangani request tersebut.

   5. Setelah setup routing URL ```main```, sekarang setup routing URL proyek dengan pergi ke ```urls.py``` pada direktori proyek.
   6. Ketika saya membuat proyek django baru dengan command ```django-admin startproject ameloops .```, saya mendapatkan code default pada ```urls.py``` seperti berikut.
      ```
      from django.contrib import admin
      from django.urls import path
      
      urlpatterns = [
          path("admin/", admin.site.urls),
      ]
      ```
      Secara garis besar, code ini mengatur URL routing dasar untuk admin dan dapat diperluas dengan URL lain sesuai kebutuhan.
      
   7. Tambahkan URL ```main``` dengan menambahkan ```include``` pada ```from django.urls import path``` dan ```path('', include('main.urls'))``` pada ```urlpatterns```.
      ```
      from django.contrib import admin
      from django.urls import path, include
      
      urlpatterns = [
          path("admin/", admin.site.urls),
          path('', include('main.urls'))
      ]
      ```
      Fungsi ```include``` berfungsi untuk menambahkan path pada aplikasi sehingga dengan ```path('', include('main.urls'))``` routing URL pada aplikasi main dapat terhubung ke proyek django.

## Membuat model pada aplikasi main dengan nama Product dan memiliki atribut wajib seperti name, price, description.
   
