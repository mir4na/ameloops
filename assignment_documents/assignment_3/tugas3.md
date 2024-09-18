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
