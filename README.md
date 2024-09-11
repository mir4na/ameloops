# Tugas 2: Pengenalan Aplikasi Django dan Model-View-Template (MVT) pada Django

- Nama: Muhammad Afwan Hafizh
- NPM: 2306208855
- Kelas: PBP-F

- Link deploy: http://muhammad-afwan-ameloopsapp.pbp.cs.ui.ac.id/products/

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
      django-admin startproject ameloops .
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
      Berbeda dengan command ```django-admin startproject ameloops .``` yang menjadi kerangka utama dan melakukan konfigurasi yang diperlukan dalam menjalankan django, command ```python manage.py startapp main``` akan membuat app baru yang akan berfokus pada kumpulan fitur tertentu seperti shop, blog, dan lain-lain.

   2. Setelah membuat app main, maka tambahkan string ```'main'``` pada ```INSTALLED_APPS``` di ```settings.py``` pada direktori proyek. Fungsi pada penambahan string ```'main'``` pada ```INSTALLED_APPS``` berfungsi untuk menambahkan aplikasi pada yaitu ```'main'``` pada daftar aplikasi di proyek django.

## Melakukan routing pada proyek agar dapat menjalankan aplikasi main.
   1. Pergi ke ```urls.py``` pada direktori proyek.
   2. Ketika saya membuat proyek django baru dengan command ```django-admin startproject ameloops .```, saya mendapatkan code default pada ```urls.py``` seperti berikut.
      ```
      from django.contrib import admin
      from django.urls import path
      
      urlpatterns = [
          path("admin/", admin.site.urls),
      ]
      ```
      Secara garis besar, code ini mengatur URL routing dasar untuk admin dan dapat diperluas dengan URL lain sesuai kebutuhan.
      
   3. Tambahkan URL ```main``` dengan menambahkan ```include``` pada ```from django.urls import path``` dan ```path('', include('main.urls'))``` pada ```urlpatterns```.
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
   1. Pergi ke ```models.py``` pada direktori main.
   2. Di sini saya berencana untuk membuat atribut name, price, description, stock, dan category.
   3. Berikut code yang saya buat
      ```
      from django.db import models

      class Product(models.Model):
          name = models.CharField(max_length=255)
          price = models.IntegerField()
          description = models.TextField()
          stock = models.PositiveIntegerField(default=0)
          category = models.CharField(max_length=50, blank=True, null=True)
      
          def __str__(self):
              return self.name
      ```
      - ```from django.db import models```, fungsinya mengimpor modul models dari django.db, yang berisi berbagai jenis field dan fungsionalitas yang digunakan untuk mendefinisikan model dalam django.
      - ```name = models.CharField(max_length=255)```, fungsinya untuk mendefinisikan field name sebagai CharField maksimal 255 karakter untuk menyimpan teks pendek seperti halnya nama produk.
      - ```price = models.IntegerField()```, fungsinya untuk mendefinisikan field price sebagai IntegerField untuk menyimpan nilai integer seperti halnya harga produk.
      - ```description = models.TextField()```, fungsinya untuk mendefinisikan field description sebagai TextField untuk menyimpan teks panjang berupa deskripsi produk.
      - ```stock = models.PositiveIntegerField(default=0)```, fungsinya untuk mendefinisikan field stock sebagai PositiveIntegerField dengan nilai default 0, artinya menyimpan integer positif karena stok produk tidak mungkin kurang dari nol.
      - ```category = models.CharField(max_length=50, blank=True, null=True)```, berfungsi untuk mendefinisikan field category sebagai CharField maksimal 50 karakter dengan nilai default blank pada form dan NULL di database, yang digunakan untuk menyimpan kategori produk.

   4. Setelah saya membuat perubahan baru pada ```models.py``` seperti menambahkan atribut, maka saya membuat migrasi model dengan menjalankan command berikut
      ```
      python manage.py makemigrations
      ```
      Command ini membuat file migrasi berdasarkan perubahan yang dibuat pada model di models.py. Migrasi adalah kumpulan instruksi yang django gunakan untuk mengubah struktur database sesuai dengan model yang telah didefinisikan atau dimodifikasi.

   5. Setelah membuat migrasi model, maka jalankan command berikut
      ```
      python manage.py migrate
      ```
      Command ini menjalankan migrasi yang telah dibuat dan mengaplikasikan perubahan ke database. Ini akan mengubah struktur tabel sesuai dengan model yang didefinisikan dalam file migrasi.

## Membuat sebuah fungsi pada views.py untuk dikembalikan ke dalam sebuah template HTML yang menampilkan nama aplikasi serta nama dan kelas kamu.
   1. Pergi ke ```views.py``` yang ada pada direktori main.
      
   2. Lalu, buat code berikut
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

   3. Sebelumnya, saya telah membuat file ```\templates\main.html``` pada direktori main, berikut potongan HTML dalam implementasinya
      ```
      ...
      <h1 class="text-center mb-4">Welcome to {{ app_name }}!</h1>
      <p class="text">Hello! I am {{ name }} from {{ class }}. A newcomer in computer science field.</p>
      ...
      ```
      Maka, output yang muncul pada HTML adalah
      ```
      Welcome to Ameloops!
      Hello! I am Muhammad Afwan Hafizh from PBP F. A newcomer in computer science field.
      ```
      Ini dapat terjadi karena adanya rendering template yang telah dilakukan oleh code pada file ```views.py```. Jadi, value dari variabel yang disisipkan dalam HTML akan menampilkan konteks dari data yang telah diatur di ```views.py```.

## Membuat sebuah routing pada urls.py aplikasi main untuk memetakan fungsi yang telah dibuat pada views.py.
   1. Setelah membuat code pada ```views.py```, maka buat berkas ```urls.py``` pada direktori main.

   2. Lalu, setup routing URL ```main``` pada ```urls.py``` dengan buat code seperti berikut
      ```
      from django.urls import path
      from . import views
      
      app_name = 'main'
      
      urlpatterns = [
          path('', views.show_main, name='show_main'),
      ]
      ```
      Secara garis besar, code ini mengartikan apabila user mengunjungi URL yang sesuai (URL root dari aplikasi main), maka django akan mencocokkan URL tersebut dengan pola yang ada di urlpatterns. URL root ('') akan cocok dengan path('', views.show_main, name='show_main'), sehingga django akan memanggil fungsi ```show_main``` dari ```views.py``` untuk menangani request tersebut.

## Melakukan deployment ke PWS terhadap aplikasi yang sudah dibuat sehingga nantinya dapat diakses oleh teman-temanmu melalui Internet.
   1. Buka Pacil Web Service melalui link ini ```https://pbp.cs.ui.ac.id/```.
   2. Apabila belum memiliki akun, maka dapat melakukan register akun terlebih dahulu. Namun, karena saya sudah membuat akun sebelumnya, maka saya dapat langsung login pada PWS.
   3. Buat proyek baru dengan memilih ```New Project``` pada PWS.
   4. Isi nama proyek pada field yang diberikan.
   5. Setelah membuat proyek baru, maka akan diberikan password credential yang hanya dapat dilihat sekali saja. Jadi, simpan credential tersebut dengan baik.
   6. Lalu, pergi ke ```settings.py``` pada direktori proyek, tambahkan URL ```muhammad-afwan-ameloops.pbp.cs.ui.ac.id``` pada ```ALLOWED_HOSTS``` untuk melakukan deploy pada PWS.
   7. Lakukan command berikut ini untuk menambahkan remote repository baru ke dalam repository git lokal.
      ```
      git remote add pws http://pbp.cs.ui.ac.id/muhammad.afwan/ameloops
      ```
      (Pada kasus saya, ketika melakukan remote add tidak dimintai credentialsnya padahal seharusnya dimintai credentialsnya. Sepertinya ini karena adanya faktor dari PWS)
   8. Cek branch dengan ```git branch```. Apabila sedang di branch ```master```, maka dapat langsung melakukan push dengan command
      ```
      git push pws master
      ```
      Namun, apabila sedang di branch ```main```, maka dapat melakukan push dengan command
      ```
      git push pws main:master
      ```
   9. Ketika sudah melakukan push, pastikan tertulis status ```succesful``` pada log proyeknya sehingga menandakan bahwa deploy telah berhasil.

## Buatlah bagan yang berisi request client ke web aplikasi berbasis Django beserta responnya dan jelaskan pada bagan tersebut kaitan antara urls.py, views.py, models.py, dan berkas html.
![image](https://github.com/user-attachments/assets/b78beffe-f004-4e9a-83c7-619bed86bd19)
Alur penjelasan bagan:
1. ```Client``` akan mengirim HTTP request ke server django.
2. Hasil request tersebut akan dicocokkan dengan pola URL pada ```urls.py``` yang apabila ditemukan kecocokan, maka akan diteruskan fungsi yang sesuai pada ```views.py```
3. ```views.py``` akan memproses request. Apabila ada data yang diperlukan, maka akan dilakukan proses pengambilan data dengan query tertentu pada ```models.py```.
4. Apabila ada proses pengambilan data, maka ```models.py``` akan memproses query dari ```views.py``` dan mengembalikan data tersebut ke ```views.py```.
5. Context value dari ```views.py``` akan disispkan pada HTML. HTML akan di-render dan dikembalikan sebagai HTTP response.
6. HTTP response yang telah di-render akan dikembalikan kepada ```client```.

## Jelaskan fungsi git dalam pengembangan perangkat lunak!
- Version control. Git dapat melacak perubahan pada suatu code sehingga developer dapat melihat history dalam perubahan code atau kembali ke versi-versi sebelumnya apabila diperlukan.
- Terdapat fitur branching dan merging. Branching berfungsi apabila developer ingin mengembangkan fitur atau bereksperimen dengan branch baru. Merging berfungsi untuk menyatukan keseluruhan code pada branch utama dari hasil branch-branch lain.
- Kemudahan dalam berkolaborasi dalam tim karena didukung oleh fitur-fitur yang ada.
- Dokumentasi perubahan code melalui fitur ```commit message``` atau ```pull request```.
- Kemudahan dalam melacak bug pada proyek.
- Setiap kali melakukan ```clone``` pada repository Git secara otomatis dapat digunakan sebagai backup dari proyek.

## Menurut Anda, dari semua framework yang ada, mengapa framework Django dijadikan permulaan pembelajaran pengembangan perangkat lunak?
Menurut saya, framework django ini lumayan "newbie friendly" karena di dalamnya sudah tersedia fitur-fitur secara default yang dapat saya manfaatkan. Adanya konsep MVT (Model-View-Template) juga sangat membantu dan mudah untuk dipahami bagi orang yang baru mulai belajar pengembangan software. Selain itu, framework django juga memiliki keamanan bawaan pada banyak aspek, salah satunya dengan adanya konsep ORM (Object-Relation Mapping) sehingga dapat meminimalisir terjadinya risiko dari pihak ilegal yang ingin mengambil data user dengan SQL Injection.

## Mengapa model pada Django disebut sebagai ORM?
Secara garis besar, konsep ORM (Object-Relation Mapping) pada framework django dapat memudahkan developer dalam pengembangan proyeknya karena developer dapat berinteraksi dengan database melalui objek bahasa pemrograman tanpa harus membuat query SQL secara langsung. Selain itu, developer dapat melakukan operasi CRUD (Copy, Read, Update, Delete) dengan menggunakan bahasa pemrograman python tanpa perlu memikirkan detail mengenai implementasi databasenya, berikut contohnya:

```
from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=150)
    author = models.CharField(max_length=150)
    
    def __str__(self):
        return self.title

# Membuat buku
new_book = Book(title="Metamorphosis", author="Franz Kafka")
new_book.save()

# Mengambil query buku dengan judul tertentu
all_books = Book.objects.all()
django_books = Book.objects.filter(title__contains="Metamorph")

# Melakukan update pada judul buku
book_to_update = Book.objects.get(id=1)
book_to_update.title = "ubah judul"
book_to_update.save()

# Menghapus buku
book_to_delete = Book.objects.get(id=2)
book_to_delete.delete()
```
