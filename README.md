# Tugas 2: Pengenalan Aplikasi Django dan Model-View-Template (MVT) pada Django

- Nama: Muhammad Afwan Hafizh
- NPM: 2306208855
- Kelas: PBP-F

- Link deploy: [click here!](http://muhammad-afwan-ameloops.pbp.cs.ui.ac.id/)

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
   9. Ketika sudah melakukan push, pastikan tertulis status ```successful``` pada log proyeknya sehingga menandakan bahwa deploy telah berhasil.

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
---

# Tugas 3: Implementasi Form dan Data Delivery pada Django

Berikut adalah langkah-langkah yang saya lakukan untuk mengimplementasikan poin-poin dalam checklist:

## Membuat input form untuk menambahkan objek model pada app sebelumnya.

   1. Buat file bernama ```forms.py``` pada direktori main (setara dengan ```models.py```, ```views.py```, dan lainnya)
   2. Buat code pada ```forms.py``` seperti berikut
      ```
      from django import forms
      from .models import *
      
      class ProductForm(forms.ModelForm):
          class Meta:
              model = Product
              fields = ['name', 'price', 'description', 'stock', 'category', 'image']
              widgets = {
                  'category': forms.Select(attrs={'class': 'form-control'}),
              }
      
      ```
      ---
      Secara garis besar, code ini membuat form untuk HTML yang terdiri dari input ```name```, ```price```, ```description```, ```stock```, ```category```, dan ```image```. Lalu, field pada ```category``` akan di-render sebagai dropdown dengan class ```form-control```.

   3. Lalu, pergi ke ```views.py``` pada direktori ```main```, lakukan import object pada ```forms.py``` yang telah dibuat.
      ```
      from main.forms import ProductForm
      ```

   4. Buatlah suatu fungsi yang bertujuan untuk menambahkan suatu produk melalui form yang telah dibuat, contohnya seperti berikut.
      ```
      def create_product_entry(request):
          form = ProductForm(request.POST or None, request.FILES or None)
          if request.method == "POST":
              if form.is_valid():
                  form.save()
                  return redirect('main:products')
              else:
                  return render(request, "account.html", {'form': form, 'error': 'Form is invalid'})
          return render(request, "account.html", {'form': form})
      ```
   
      Berikut alur eksekusi dari code di atas:
      - Ketika user mengakses halaman untuk menambahkan suatu produk, maka form dengan input kosong akan ditampilkan.
      - Apabila user melakukan input untuk data produk melalui method ```POST```, maka fungsi akan checking apakah input valid atau tidak.
      - Apabila valid, maka simpan di database dan user akan di-redirect ke page product. Jika tidak, maka akan ditampilkan pesan error.
   
   5. Pergi ke ```urls.py``` yang ada pada direktori ```main```, lalu tambahkan path URL pada variabel ```urlpatterns``` untuk mengakses fungsi pada ```views.py``` yang sudah dibuat sebelumnya.
      ```
      urlpatterns = [
      ...
      path('account/', views.create_product_entry, name='create_product_entry'),
      ...
      ]
      ```
      Disini saya melakukan konfigurasi routing fungsi ```create_product_entry``` sebagai view pada page ```account```.
   
   6. Setelah path URL diatur pada urls.py, maka implementasikan form yang telah dibuat pada page HTML. Berikut contoh implementasi mengenai potongan codenya.
      ```
      ...
      <form method="POST" enctype="multipart/form-data">
         {% csrf_token %}
         <table>
            {{ form.as_table }}
            <tr>
               <td></td>
               <td>
                  <input type="submit" value="Add Product Form"/>
               </td>
            </tr>
         </table>
      </form>
      ...
      ```
      Potongan code ini memiliki arti sebagai berikut.
      - Form ini di-render dengan method POST dan dapat menangani file yang diunggah karena menggunakan ```enctype="multipart/form-data"```. Form yang dirender mencakup field-field seperti ```name```, ```price```, ```description```, ```category```, dan ```image``` yang sudah didefinisikan di ProductForm.
      - Pengguna mengisi semua field dalam form, dan saat tombol submit ```Add Product Form``` diklik, semua data form (termasuk file yang diunggah jika ada) dikirim ke server melalui metode ```POST```.
      - Saat form disubmit, form akan dikirim ke URL yang sama (jika tidak ada action pada form). Data yang dikirimkan akan divalidasi di view (```create_product_entry```) menggunakan ```form.is_valid()```.
      - CSRF token memastikan bahwa form dikirim oleh pengguna yang sah dan tidak dari sumber berbahaya. Django akan memeriksa apakah CSRF token yang dikirimkan cocok dengan token yang diharapkan.
      - Di view Django, jika form valid, data akan disimpan ke database dengan memanggil ```form.save()```.
      
   7. Dengan berhasilnya pengisian pada form yang telah dibuat, maka data produk akan disimpan di dalam database. Saya dapat mengaksesnya apabila sekiranya sewaktu-waktu dibutuhkan.
   
## Tambahkan 4 fungsi views baru untuk melihat objek yang sudah ditambahkan dalam format XML, JSON, XML by ID, dan JSON by ID.

   1. Pergi ke ```views.py``` pada direktori ```main```.
   2. Tambahkan import ```HttpResponse``` dan ```serializers```.
      ```
      from django.http import HttpResponse
      from django.core import serializers
      ```
      - ```HttpResponse``` adalah salah satu kelas bawaan dari Django yang digunakan untuk mengirimkan respon HTTP ke client.
      - ```serializers``` adalah modul dari Django yang digunakan untuk mengubah data query menjadi format serializable yang dapat diproses lebih lanjut, seperti JSON, XML, dan lain-lain.
   3. Disini saya buat suatu fungsi bernama ```serialize_data``` yang menerima parameter ```request```, ```model```, ```fmt```(format JSON atau XML), dan ```id```. Ini dilakukan untuk menghindari inisialisasi variabel yang berulang.
      ```
      def serialize_data(request, model, fmt, id=None):
          if id:
              data = get_object_or_404(model, pk=id)
              data = [data]
          else:
              data = model.objects.all()
          return HttpResponse(serializers.serialize(fmt, data), content_type=f"application/{fmt}")
      ```
      Berikut arti dari fungsi ```serialize_data```:
      - Jika ada ```id```, data akan diambil berdasarkan primary key dan diubah menjadi list agar bisa di-serialize. Jika tidak ada ```id```, seluruh data dari model akan diambil.
      - Data kemudian diserialisasi menggunakan format yang diminta(```fmt```), baik JSON atau XML.
      - Response HTTP dikembalikan dengan data yang di-serialize.
   4. Setelah fungsi ```serialize_data``` dibuat, maka saya buat keempat fungsi lainnya yaitu ```products_json```, ```products_xml```, ```product_json_by_id```, dan ```product_xml_by_id```.
      ```
      def products_json(request):
          return serialize_data(request, Product, "json")
      ```
      Fungsi ini akan melakukan return semua data dari model Product dalam format JSON.
      ```
      def products_xml(request):
          return serialize_data(request, Product, "xml")
      ```
      Fungsi ini akan melakukan return semua data dari model Product dalam format XML.
      ```
      def product_json_by_id(request, id):
          return serialize_data(request, Product, "json", id)
      ```
      Fungsi ini akan melakukan return data dari model Product yang spesifik berdasarkan id dalam format JSON.
      ```
      def product_xml_by_id(request, id):
          return serialize_data(request, Product, "xml", id)
      ```
      Fungsi ini akan melakukan return data dari model Product yang spesifik berdasarkan id dalam format XML.

      Opsional: Karena saya memiliki object selain ```Product``` yaitu ```Category```, maka saya juga menambahkan keempat fungsi untuk melihat data untuk object ```Category``` dalam format JSON dan XML.
      ```
      def category_json(request):
          return serialize_data(request, Category, "json")
      ```
      ```
      def category_xml(request):
          return serialize_data(request, Category, "xml")
      ```
      ```
      def category_json_by_id(request, id):
          return serialize_data(request, Category, "json", id)
      ```
      ```
      def category_xml_by_id(request, id):
          return serialize_data(request, Category, "xml", id)
      ```
   6. Untuk melihat data produk yang telah terdata dalam format JSON, maka kita perlu mengonfigurasi routing pada ```urls.py``` di direktori ```main``` yang akan dibahas pada soal selanjutnya.

## Membuat routing URL untuk masing-masing views yang telah ditambahkan pada poin 2.

   1. Pergi ke ```urls.py``` pada direktori ```main```.
   2. Tambahkan path URL pada variabel ```urlpatterns```.
      ```
      path('product_json/', views.products_json, name='products_json'),
      path('product_xml/', views.products_xml, name='products_xml'),
      path('product_json/<str:id>/', views.product_json_by_id, name='product_json_by_id'),
      path('product_xml/<str:id>/', views.product_xml_by_id, name='product_xml_by_id'),
      ```
      Untuk mengakses keseluruhan data produk dalam format JSON, maka saya atur path URLnya ke ```../product_json```. Apabila saya ingin melihat satu produk secara spesifik, maka saya dapat menambahkan ```id``` dari produk tersebut dengan menambahkan path paramater seperti berikut.
      ```
      ../product_json/[id]
      ```
      Lalu, untuk mengakses keseluruhan data produk dalam format XML, maka saya atur path URLnya ke ```../product_xml```. Apabila saya ingin melihat satu produk secara spesifik, maka saya dapat menambahkan ```id``` dari produk tersebut dengan menambahkan path paramater seperti berikut.
      ```
      ../product_xml/[id]
      ```
   3. Setelah konfigurasi path URL, maka jalankan command ```python manage.py runserver``` pada terminal, lalu pergi ke ```http://localhost:8000/``` dan tambahkan path baru pada URL seperti ```../product_json``` atau ```../product_xml``` untuk melihat keseluruhan data dalam format JSON atau XML.

##  Jelaskan mengapa kita memerlukan data delivery dalam pengimplementasian sebuah platform?

   Data delivery diperlukan dalam pengimplementasian sebuah platform untuk memastikan informasi yang tepat dapat diakses oleh user sesuai kebutuhan mereka secara aman dan efisien. Ini memungkinkan adanya integrasi yang baik antara sistem backend dan frontend dalam memastikan data yang relevan tersedia tepat waktu. Selain itu, mekanisme pengiriman data yang efektif mendukung skalabilitas dan performa platform dalam menangani beban traffic user yang tinggi.

##  Menurutmu, mana yang lebih baik antara XML dan JSON? Mengapa JSON lebih populer dibandingkan XML?

   Menurut saya JSON lebih baik dibandingkan dengan XML karena JSON memiliki readability dan struktur data yang sederhana sehingga lebih mudah untuk dibaca. Tidak seperti JSON, XML mempunyai struktur data yang cukup kompleks serta penggunaan tag pembuka dan tag penutup yang membuat isi file menjadi lebih panjang sehingga cenderung sulit untuk dibaca. Selain itu, JSON kompatibel dengan Javascript, artinya JSON dapat digunakan langsung di Javascript tanpa adanya konversi tambahan. JSON juga lebih mudah di-serialize karena banyak built-in yang mendukung penanganan JSON pada programming language.
   
##  Jelaskan fungsi dari method is_valid() pada form Django dan mengapa kita membutuhkan method tersebut?

   Method dari ```is_valid()``` secara garis besar berfungsi untuk melakukan validasi terhadap input-input yang diberikan pada field. Method ```is_valid()``` juga memberikan pesan atau informasi apabila ada input yang salah sehingga user dapat mengetahui apa data yang seharusnya diinput pada field. Kita membutuhkan method ini untuk menjaga keamanan data dengan memastikan bahwa data yang diterima oleh input adalah data yang valid dan sesuai dengan formatnya. Ini mencegah kesalahan dan potensi masalah keamanan yang dapat muncul dari data yang tidak valid. Selain itu, data yang tidak valid dapat menyebabkan app tidak berjalan dengan semestinya. Maka dari itu, method ```is_valid()``` memiliki peran penting untuk menjaga validasi data.
   
##  Mengapa kita membutuhkan csrf_token saat membuat form di Django? Apa yang dapat terjadi jika kita tidak menambahkan csrf_token pada form Django? Bagaimana hal tersebut dapat dimanfaatkan oleh penyerang?

   Penggunaan ```csrf_token``` berfungsi untuk memastikan bahwa request yang diberikan pada app dikirimkan oleh user yang sah dan bukan dari pihak lain. Ini artinya ```csrf_token``` dapat mencegah terjadinya serangan CSRF(Cross Site Request Forgery).
   
   ![image](https://github.com/user-attachments/assets/f66f58cd-02ca-4f41-89f1-1979315418a5)

   CSRF adalah jenis serangan yang memungkinkan pihak ilegal untuk mengirimkan request melalui user yang sudah terautentikasi pada suatu app dengan tanpa izin dari user itu sendiri. Apabila ```csrf_token``` tidak diimplementasikan dalam form Django, atau asumsikan serangan CSRF berhasil, maka pihak penyerang dapat melakukan segala manipulasi baik dari perubahan atau penghapusan suatu data bahkan hingga melakukan transaksi yang sifatnya ilegal. Adanya ```csrf_token``` ini, mencegah dari request yang tidak valid sehingga server akan menolak apabila token yang datang merupakan token yang tidak cocok.

##  Mengakses keempat URL di poin 2 menggunakan Postman, membuat screenshot dari hasil akses URL pada Postman, dan menambahkannya ke dalam README.md.

   - ```http://localhost:8000/product_json```
     ![image](https://github.com/user-attachments/assets/3e15f048-63bb-4307-8546-663b57f4c3ee)
   - Misal, saya memasukkan id dari item ```Banana Cat``` dan menambahkannya ke path parameter.
     ```http://localhost:8000/product_json/0775c3fc-e7fb-415e-be27-08b2faf63e8e```
     ![image](https://github.com/user-attachments/assets/80ca333b-fce4-4831-aa35-895e0368a848)
   - ```http://localhost:8000/product_xml```
     ![image](https://github.com/user-attachments/assets/098fdc08-c321-400b-bc28-0ce7d4f1355a)
   - Misal, saya memasukkan id dari item ```Anti-Matil``` dan menambahkannya ke path parameter.
     ```http://localhost:8000/product_xml/00167025-564d-491f-8e9b-d974b9446d65```
     ![image](https://github.com/user-attachments/assets/fb0ac0fc-cca8-43f8-985a-3ab6616985bf)
