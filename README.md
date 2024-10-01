- Nama: Muhammad Afwan Hafizh
- NPM: 2306208855
- Kelas: PBP-F

- Link deploy: [click here!](http://muhammad-afwan-ameloops.pbp.cs.ui.ac.id/)

# Tugas 5: Implementasi Autentikasi, Session, dan Cookies pada Django

## Implementasikan fungsi untuk menghapus dan mengedit product.

   1. Pergi ke ```models.py``` pada direktori ```main```.

   2. Buat object baru bernama ```Cart``` dan ```CartItem```.
      ```
      
      ```
   
   1. Pergi ke ```views.py``` pada direktori ```main```.
      
   2. Implementasikan fungsi untuk edit product. Disini saya mengimplementasikan edit sebagai "update" kuantitas dari jumlah product yang ada pada cart user.
      ```
      @login_required(login_url='/login')
      def edit_product(request, cart_item_id):
          cart_item = get_object_or_404(CartItem, id=cart_item_id, cart__user=request.user)
          if request.method == 'POST':
              new_quantity = int(request.POST.get('quantity', 1))
              if new_quantity > 0 and new_quantity <= cart_item.product.stock:
                  cart_item.quantity = new_quantity
                  cart_item.save()
              else:
                  messages.error(request, 'Invalid quantity.')
          return HttpResponseRedirect(reverse('main:cart'))
      ```
      Fungsi ini memungkinkan user untuk mengedit kuantitas item dalam cart belanja mereka dengan memvalidasi input dan memberikan umpan balik melalui pesan jika kuantitas tidak valid. Jika berhasil, user akan diarahkan kembali ke cart page mereka.

      3. Lalu, implementasikan fungsi untuk remove product.
         ```
         @login_required(login_url='/login')
         def remove_from_cart(request, cart_item_id):
             cart_item = get_object_or_404(CartItem, id=cart_item_id, cart__user=request.user)
             cart_item.delete()
             return HttpResponseRedirect(reverse('main:cart'))
         ```
         Fungsi ini memungkinkan user untuk menghapus item tertentu dari cart belanja mereka. Setelah penghapusan, user diarahkan kembali ke cart page. Proses ini mencakup pemeriksaan apakah user sudah login dan validasi keberadaan item yang ingin dihapus.

      4. 
         
# Tugas 4: Implementasi Autentikasi, Session, dan Cookies pada Django

   1. Aktifkan virtual environment, lalu pergi ke ```views.py``` pada direktori ```main```.
      
   2. Tambahkan import ```UserCreationForm```, ```AuthenticationForm```, dan ```datetime``` pada code.
      ```
      from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
      from django.contrib import messages
      import datetime
      ...
      ```
      - ```UserCreationForm```: Ini adalah form bawaan Django yang digunakan untuk membuat user baru. Form ini biasanya mencakup field seperti username, password, dan konfirmasi password.
      - ```AuthenticationForm```: Ini adalah form yang digunakan untuk otentikasi user, biasanya untuk login. Form ini biasanya mencakup field untuk username dan password. Ketika user mengisi form ini dan mengirimkannya, Django akan memeriksa apakah kredensial yang diberikan valid atau tidak.
      - ```messages```: Ini adalah modul dari Django untuk menampilkan pesan kepada user, misalnya, setelah berhasil login, mendaftar, atau ketika terjadi kesalahan. Modul ini juga dapat digunakan untuk kebutuhan debugging.
      - ```datetime```: Modul datetime digunakan untuk bekerja dengan tanggal dan waktu. Pada tugas 4, modul ini berfungsi untuk mencatat waktu terakhir login dari user.
        
   3. Buatlah berkas HTML baru yang bernama ```register.html``` dan ```login.html``` dan biarkan pagenya kosong terlebih dahulu.
        
   4. Buatlah fungsi ```register_user``` yang berfungsi untuk melakukan registrasi dan menambah data user ketika telah didaftarkan.
      ```
      def register_user(request):
          if request.method == 'POST':
              form = UserCreationForm(request.POST)
              if form.is_valid():
                  form.save()
                  messages.success(request, 'Successfully created an account!')
                  return redirect('main:login')
              else:
                  messages.error(request, 'Wrong input!')
          else:
              form = UserCreationForm()
      ```
      Fungsi ini menangani pendaftaran user dengan memvalidasi input (```is_valid()```), menyimpan user baru jika data valid dengan method ```POST```, memberikan pesan kepada user (```messages```), dan mengarahkan mereka ke halaman login (```redirect```). Jika ada kesalahan dalam input, maka akan muncul pesan "Wrong input!" tanpa penghapusan input pada masing-masing field.
      
   5. Lalu, buatlah fungsi ```login_user``` yang berfungsi untuk mengautentikasi user ketika melakukan login.
      ```
      def login_user(request):
          if request.method == 'POST':
              form = AuthenticationForm(data=request.POST)
      
              if form.is_valid():
                  user = form.get_user()
                  login(request, user)
                  response = HttpResponseRedirect(reverse("main:show_main"))
                  response.set_cookie('last_login', str(datetime.datetime.now()))
                  messages.success(request, 'Login berhasil!')
                  return response
              else:
                  messages.error(request, 'Wrong username or password!')
          return render(request, 'login.html')
      ```
      Fungsi ini menangani proses login user melalui method ```POST``` yang nantinya akan dibuat instance dari AuthenticationForm dengan data yang dikirimkan. Setelah memvalidasi form, fungsi mengambil objek user dan melakukan login menggunakan ```login(request, user)```, kemudian membuat respons ```redirect``` ke halaman utama aplikasi sambil menetapkan cookie untuk mencatat waktu login terakhir dan mengirimkan pesan sukses kepada user. Jika form tidak valid, user akan diberi tahu tentang kesalahan pada kredensial yang dimasukkan.

   6. Setelah membuat fungsi untuk register dan login, buatlah fungsi ```logout_user``` untuk mekanisme logout user.
      ```
      from django.contrib.auth.decorators import login_required
      
      @login_required(login_url='/login')
      def logout_user(request):
          logout(request)
          response = HttpResponseRedirect(reverse('main:login'))
          response.delete_cookie('last_login')
          return response
      ```
      Fungsi ```logout_user``` adalah view yang dilindungi oleh decorator ```login_required```, memastikan hanya user yang sudah login yang dapat mengaksesnya. Ketika fungsi ini dipanggil, ia memanggil ```logout(request)``` untuk mengeluarkan user dari sesi, kemudian membuat objek ```HttpResponseRedirect``` yang mengarahkan user kembali ke halaman login menggunakan ```reverse('main:login')```. Selanjutnya, code akan menghapus cookie last_login dari browser lalu mengembalikan respons tersebut agar user diarahkan ke halaman login setelah logout.

   7. Pergi ke ```urls.py``` untuk mengatur routing mengenai login, register, dan logout.
      ```
      path('login/', views.login_user, name='login'),
      path('register/', views.register_user, name='register'),
      path('logout/', views.logout_user, name='logout'),
      ```
      
   8. Setelah mengatur routing pada ```urls.py```, implementasikan codenya pada ```register.html``` dan ```login.html``` pada direktori ```main```.
      ```
      ...
      <!-- login.html -->
      <h1 class="login-title">Login</h1>

        <form method="POST" action="" class="login-form">
            {% csrf_token %}
            <div class="form-group">
                <label for="username">Username:</label>
                <input type="text" name="username" id="username" required>
            </div>
            <div class="form-group">
                <label for="password">Password:</label>
                <input type="password" name="password" id="password" required>
            </div>
            <button type="submit" class="login-btn">Login</button>
        </form>
      ...
      ```
      ```
      ...
      <!-- register.html -->
      <h1 class="register-title">Register</h1>

        <form method="POST" action="" class="register-form">
            {% csrf_token %}
            {% for field in form %}
            <div class="form-group">
                <label for="{{ field.id_for_label }}">{{ field.label }}</label>
                {{ field }}
            </div>
            {% endfor %}
            <button type="submit" class="register-btn">Register</button>
        </form>
      ...
      ```

   9. Jalankan ```python manage.py runserver``` pada terminal lalu cek apakah code sudah berjalan dengan benar atau belum.

## Membuat dua akun pengguna dengan masing-masing tiga dummy data menggunakan model yang telah dibuat pada aplikasi sebelumnya untuk setiap akun di lokal.

   1. Membuat dua akun pengguna sebagai dummy data dengan pergi ke page register, lalu login pada page ```login```.
      ![image](https://github.com/user-attachments/assets/80696e62-c1e5-4556-bc89-0ae4ba70df36)
      ![image](https://github.com/user-attachments/assets/cee9d038-7092-48c2-a673-2dae7db72c61)
      Ini tampilan ketika user sudah login, lalu pergi ke halaman ```cart```dan belum memasukkan produk ke dalam keranjang (artinya belum ada data input produk untuk dimasukkan dalam cart)
      ![image](https://github.com/user-attachments/assets/621751d9-ce9f-4c2b-b170-b0ae0cb09acb)

   2. Lalu coba tambahkan 3 produk ke dalam cart dengan menggunakan user yang saat ini sedang login.
      ![image](https://github.com/user-attachments/assets/254cbbed-11ad-4c53-a108-99cbec3cd50c)

   3. Berikut hasil penambahan 3 product ke dalam cart pada user ```fvfvf4f4```
      ![image](https://github.com/user-attachments/assets/dad0c8f1-9cfb-4621-af59-4e315e47e7f2)
      Ini artinya pembuatan tiga dummy data pada user account telah berhasil.

   4. Sekarang, coba buat lagi akun baru, tambahkan 3 product ke dalam cart, lalu bandingkan dengan akun sebelumnya.
      ![image](https://github.com/user-attachments/assets/42acf93d-e3f2-4c1c-9f59-6b26727e8224)
      ![image](https://github.com/user-attachments/assets/ce9e1591-bb18-4562-8989-e87ab436d779)
      ![image](https://github.com/user-attachments/assets/165a1d0a-92de-46e2-b9f3-7da8de8a1488)
      berikut hasilnya:
      ![image](https://github.com/user-attachments/assets/23645a78-909a-41da-a079-8c3d4d7a3e4b)

   5. Bandingkan hasil penambahan produk pada masing-masing akun. Ini artinya setiap akun memiliki data penambahan product yang berbeda. Maka pembuatan dua akun user dengan masing-masing tiga dummy data telah berhasil.

## Menghubungkan model Product dengan User.

   1. Untuk menghubungkan model Product dengan User, maka pertama pergi ke models.py dan tambahkan line code berikut di bagian atas code.
      ```
      from django.contrib.auth.models import User
      ```
      ```User``` dari ```django.contrib.auth.models``` adalah model default Django yang mewakili user di aplikasi Django.
      
   2. Disini saya membuat suatu model baru bernama ```Cart``` yang berfungsi untuk menyimpan product yang dimasukkan ke dalam keranjang pada masing-masing user. Berikut potongan codenya:
      ```
      ...
      class Cart(models.Model):
          user = models.OneToOneField(User, on_delete=models.CASCADE)
      ...
      class CartItem(models.Model):
          id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
          cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
      ...
      ```
      Relasi ```OneToOneField``` ke model User. Ini berarti setiap user hanya dapat memiliki satu keranjang, dan keranjang ini terhubung langsung ke user yang bersangkutan. Jika user dihapus, maka keranjang juga ikut dihapus (```on_delete=models.CASCADE```). Lalu, model ```CartItem``` digunakan untuk menyimpan setiap item yang ada di dalam keranjang belanja,
      
   3. Sekarang, pergi ke ```views.py``` yang pada direktori main, buatlah suatu fungsi yang berfungsi untuk menambahkan produk ke keranjang masing-masing usernya.
      ```
      @require_POST
      @login_required(login_url='/login')
      def add_to_cart(request, product_id):
          product = get_object_or_404(Product, id=product_id)
          cart, created = Cart.objects.get_or_create(user=request.user)
          cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)
          return JsonResponse({'status': 'success', 'message': f'{product.name} added to cart'})
       ```
      Decorator ```@require_POST``` dan ```@login_required(login_url='/login')``` berfungsi untuk memastikan bahwa view hanya merespons permintaan HTTP POST dan memastikan bahwa hanya user yang sudah login dapat mengakses view ini. Jika user belum login, mereka akan diarahkan ke halaman login (```/login```). Lalu, fungsi ```get_or_create``` berfungsi untuk mendapatkan objek ```Cart``` yang dimiliki oleh user saat ini (```request.user```). Jika user belum memiliki keranjang, fungsi ini akan otomatis membuat keranjang baru untuk user. ```created``` adalah boolean yang menunjukkan apakah keranjang baru dibuat atau tidak. Jika keranjang sudah ada, ```created``` akan bernilai False, jika tidak, maka True. Fungsi ini juga mengembalikan respons dalam format JSON.

   5. Lakukan migrasi model dengan ```python manage.py makemigrations``` yang dilanjutkan dengan ```python manage.py migrate```.
      
   6. Ketika terjadi error, hal yang biasanya saya lakukan adalah me-reset kembali model dan database dengan cara menghapusnya lalu melakukan migrasi ulang.  
      
## Menampilkan detail informasi pengguna yang sedang logged in seperti username dan menerapkan cookies seperti last login pada halaman utama aplikasi.

   1. Untuk menampilkan detail informasi user yang sedang logged in, di sini saya sudah membuat ```navbar.html``` sebagai navigation bar pada app saya. Berikut potongan codenya.
      ```
      ...
      {% if user.is_authenticated %}
                        <li class="nav-item dropdown">
                            <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                            {{ user.username }}
                            </a>
                            <ul class="dropdown-menu" aria-labelledby="navbarDropdown">
                            <li><a class="dropdown-item" href="{% url 'main:account' %}">Account</a></li>
                            <li><hr class="dropdown-divider"></li>
                            <li><a class="dropdown-item" href="{% url 'main:logout' %}">Logout</a></li>
                            </ul>
                        </li>
                        {% else %}
                        <li class="nav-item">
                            <a class="nav-link" href="{% url 'main:login' %}">Sign in</a>
                        </li>
                        {% endif %}
      ...
      ```
      Jadi, jika user belum login (user.is_authenticated bernilai False), akan menampilkan tautan Sign in yang mengarahkan pengguna ke halaman login. Namun, apabila user sudah login, maka pada tampilan page akan ditampilkan elemen dropdown di navbar dengan nama pengguna (```{{ user.username }}```). Berikut contoh gambarnya.
      Sebelum login:
      ![image](https://github.com/user-attachments/assets/8bc8d8a0-4aed-4648-8628-fe717f6a6a97)
      Sesudah login:
      ![image](https://github.com/user-attachments/assets/cac89a3d-7829-4b4c-9dff-fe0267d7f9b2)
      Dengan adanya ini, maka artinya menampilkan detail informasi user yang sedang logged in telah berhasil.
      
   2. Lalu, pergi ke ```views.py``` yang berada pada direktori ```main```, lalu tambahkan fungsionalitas cookie yang bernama ```last_login``` di fungsi ```login_user``` untuk melihat kapan terakhir kali pengguna melakukan login.
      ```
      ...
      if form.is_valid():
            user = form.get_user()
            login(request, user)
            response = HttpResponseRedirect(reverse("main:show_main"))
            response.set_cookie('last_login', str(datetime.datetime.now()))
            messages.success(request, 'Login berhasil!')
            return response
        else:
            messages.error(request, 'Wrong username or password!')
      ...
      ```
      Apabila input valid dan user berhasil login, maka cookie bernama ```last_login``` diatur untuk menyimpan waktu login terakhir dengan nilai berupa string dari waktu saat ini (```datetime.datetime.now()```).

   3. Selanjutnya, pada fungsi ```account_page```, tambahkan potongan kode ```'last_login': request.COOKIES['last_login']``` ke dalam variabel context.
      ```
      ...
      context = {
        'form': form,
        'last_login': request.COOKIES.get('last_login'),
       }
      ...
      ```
      ```'last_login': request.COOKIES['last_login']``` berfungsi menambahkan informasi cookie ```last_login``` pada response yang akan ditampilkan pada account page.

   4. Sesuaikan pada fungsi ```logout_user``` seperti berikut.
         ```
         def logout_user(request):
             logout(request)
             response = HttpResponseRedirect(reverse('main:login'))
             response.delete_cookie('last_login')
             return response
         ```
         ```response.delete_cookie('last_login')``` berfungsi untuk menghapus cookie pada ```last_login``` ketika user melakukan logout.

   5. Tambahkan code HTML berikut untuk menampilkan waktu terakhir user melakukan login. Di sini saya menambahkannya di ```account.html```.
         ```
         ...
         <p>Sesi terakhir login: {{ last_login }}</p>
         ...
         ```
         
   6. Jalankan ```python manage.py runserver```.
   
## Apa perbedaan antara HttpResponseRedirect() dan redirect()
   ```HttpResponseRedirect()``` dan ```redirect()``` pada dasarnya adalah dua cara untuk melakukan redirection dalam Django. ```HttpResponseRedirect()``` adalah class yang merupakan bagian dari modul ```django.http``` dan menghasilkan respons HTTP dengan kode status 302 secara default, sementara ```redirect()``` adalah fungsi yang merupakan bagian dari modul ```django.shortcuts``` dan sebenarnya menggunakan ```HttpResponseRedirect()``` di balik layar. Perbedaan keduanya terletak pada fleksibilitasnya. ```HttpResponseRedirect()``` membutuhkan URL lengkap atau path absolut, sedangkan ```redirect()``` dapat menerima berbagai jenis argumen seperti nama view, URL lengkap, atau bahkan model objects, yang artinya membuatnya lebih fleksibel dan mudah digunakan dalam berbagai skema. Selain itu, ```redirect()``` secara otomatis menangani pembentukan URL yang tepat menggunakan fungsi ```reverse()``` ketika diberikan nama view, sehingga lebih aman terhadap perubahan konfigurasi URL.

## Jelaskan cara kerja penghubungan model Product dengan User!

   Di sini saya mengaitkan model ```Product```, ```Cart```, ```CartItem```, dengan User.
   
   Saya akan jelaskan dari model Product terlebih dahulu.
   ```
   class Product(models.Model):
       id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
       name = models.CharField(max_length=100)
       price = models.PositiveIntegerField(default=0)
       description = models.TextField(max_length=255)
       stock = models.PositiveIntegerField(default=0)
       category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products", null=True, blank=True)
       image = models.ImageField(upload_to='./static/img/product_img', default="", null=True)

   def __str__(self):
        return self.name
   ```
   - Model Product memiliki berbagai field, seperti ```name```, ```price```, ```description```, ```stock```, dan ```image```, untuk menyimpan informasi tentang produk.
   - Model ini memiliki hubungan dengan ```CartItem```. Model ```CartItem``` memiliki relasi ```ForeignKey``` ke model ```Product```, yang memungkinkan setiap item dalam keranjang belanja untuk terkait dengan satu produk tertentu. Dengan demikian, kita dapat menyimpan informasi produk yang ditambahkan ke keranjang dan kuantitasnya.

   Model CartItem.
   ```
   class CartItem(models.Model):
       id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
       cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
       product = models.ForeignKey(Product, on_delete=models.CASCADE)
       quantity = models.PositiveIntegerField(default=1)

   def __str__(self):
        return f"{self.quantity} of {self.product.name}"

    @property
    def total_price(self):
        return self.quantity * self.product.price
   ```
   - Model CartItem memiliki field ```quantity``` yang berguna untuk menyimpan jumlah produk yang ditambahkan ke keranjang.
   - Model ini memiliki hubungan dengan ```Cart``` dan ```Product```: Model ini memiliki dua relasi ```ForeignKey```, satu untuk cart yang menghubungkannya dengan model ```Cart```, dan satu lagi untuk product yang menghubungkannya dengan model ```Product```. Ini memungkinkan kita untuk menyimpan detail spesifik tentang produk dalam keranjang belanja dan jumlahnya.

   Model Cart.
   ```
   class Cart(models.Model):
       id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
       user = models.OneToOneField(User, on_delete=models.CASCADE)
       created_at = models.DateTimeField(auto_now_add=True)
       updated_at = models.DateTimeField(auto_now=True)
   
       def __str__(self):
           return f"Cart for {self.user.username}"
   ```
   - Model Cart berfungsi sebagai keranjang belanja user. Model ini memiliki field ```user```, yang menggunakan ```OneToOneField``` untuk menghubungkan setiap keranjang belanja dengan satu user. Ini berarti setiap user hanya dapat memiliki satu keranjang belanja.
   - Model ini memiliki hubungan dengan ```CartItem```. Model ```Cart``` juga memiliki relasi ```ForeignKey``` dengan model ```CartItem```. Ini memungkinkan kita untuk mengaitkan beberapa item ke dalam satu keranjang. Dengan relasi ini, kita dapat menyimpan berbagai produk yang ditambahkan oleh user ke dalam keranjang.

   Penghubungan model ```Product```, ```CartItem```, ```Cart``` dengan User.
   1. Membuat Keranjang untuk User: Ketika user mendaftar atau login, Django membuatkan entri baru di model ```Cart``` untuk user tersebut, jika belum ada. Hal ini menghubungkan user dengan keranjang belanja user tersebut.

   2. Menambahkan Produk ke Keranjang: Ketika user menambahkan produk ke keranjang, aplikasi membuat entri baru di model ```CartItem```, yang menghubungkan produk yang dipilih dengan keranjang user. Jika produk sudah ada di keranjang, kuantitasnya akan diperbarui.

   3. Mengambil Informasi Keranjang: Saat user ingin melihat keranjang belanja mereka, aplikasi dapat mengambil semua item dari model ```CartItem``` yang terkait dengan model ```Cart```, dan dari situ, kita bisa mengakses informasi produk yang relevan melalui relasi ```ForeignKey```.

   4. Menghitung Total Harga: Model ```CartItem``` memiliki properti ```total_price``` yang menghitung harga total berdasarkan kuantitas dan harga produk. Ini memungkinkan aplikasi untuk menampilkan total biaya keranjang kepada user.

## Apa perbedaan antara authentication dan authorization, apakah yang dilakukan saat pengguna login? Jelaskan bagaimana Django mengimplementasikan kedua konsep tersebut.

   Authentication dan Authorization jelas memiliki makna yang berbeda. Authentication berfokus kepada melakukan checking apakah user yang lewat memenuhi syarat atau tidak. Ini dapat diibaratkan ketika kita ingin menonton konser, pastinya akan ada tahap pengecekan kepemilikan tiket untuk masuk zona konser. Untuk Authorization, Authorization adalah apa saja hak-hak yang dapat dilakukan user ketika sudah berhasil terautentikasi. Apabila diibaratkan dengan mekanisme pada konser lagi, misal kita datang sebagai penonton, maka pastinya kita tidak diperbolehkan masuk ke dalam ruangan vendor. Yang diperbolehkan masuk ke dalam ruangan vendor ialah hanya user-user yang memiliki label vendor atau panitia. Artinya kita tidak punya otorisasi masuk ke dalam ruangan tersebut.
   
   Ketika user sedang login, biasanya user melakukan hal-hal berikut.
   1. Pengguna memasukkan kredensial (biasanya username dan password).
   2. Sistem memeriksa kredensial tersebut terhadap data yang tersimpan.
   3. Jika cocok, pengguna dianggap terautentikasi dan diberikan akses ke sistem. Lalu, sebuah session biasanya dibuat untuk menjaga status autentikasi pengguna.
   
   Berikut implementasi Django terkait Authentication:
   - Django menggunakan modul ```django.contrib.auth``` untuk authentication.
   - Implementasi dasar melibatkan model ```User``` secara default.
   - Django menyediakan form dan view default untuk login, logout, dan manajemen password.
   - Proses authentication dapat dikustomisasi dengan ```authentication backends```.

   Berikut implementasi Django terkait Authorization:
   - Django menggunakan sistem permissions dan groups untuk authorization.
   - Setiap model dapat memiliki permissions yang terkait.
   - Pengguna dapat diberikan permissions individual atau melalui groups.
   - Django juga menyediakan decorator seperti ```@login_required``` dan ```@permission_required``` untuk mengontrol akses ke views.

## Bagaimana Django mengingat pengguna yang telah login? Jelaskan kegunaan lain dari cookies dan apakah semua cookies aman digunakan?

   Django mengingat user yang telah login menggunakan mekanisme sesi dan cookies. Saat user berhasil login, Django membuat session unik yang disimpan di backend, dan mengirimkan ID session ke browser user sebagai cookie. Cookie ini biasanya bernama ```sessionid```, digunakan oleh Django untuk mengidentifikasi user pada setiap request berikutnya. Setiap kali user mengirimkan request, Django memeriksa cookie session tersebut untuk mengambil informasi autentikasi dari backend session, memungkinkan sistem untuk mengenali apakah user sudah login dan siapa usernya. Session ini dapat diatur agar berakhir karena pengguna logout, browser ditutup, atau session kedaluwarsa.

   Selain session, cookies memiliki berbagai kegunaan lain, seperti menyimpan preferensi user, seperti tema situs, bahasa yang dipilih, atau pengaturan tampilan. Cookies juga digunakan untuk melakukan tracking aktivitas user di berbagai page, yang bermanfaat untuk analitik mengenai personalisasi konten atau menampilkan iklan yang relevan. Selain itu, cookies mendukung fitur autentikasi berkelanjutan seperti "Remember Me," yang memungkinkan user tetap login saat mereka kembali ke situs tanpa harus melakukan login ulang. Dalam aplikasi e-commerce, cookies sering menyimpan informasi tentang item yang ditambahkan ke keranjang belanja, meskipun user belum login atau belum menyelesaikan pembelian.

   Tidak semua cookies aman. Cookies dapat dicegat oleh pihak ketiga jika situs tidak menggunakan protokol yang secure. Untuk melindunginya, maka yang dapat dilakukan yaitu menggunakan atribut ```Secure``` pada cookies untuk memastikan bahwa cookies hanya dikirim melalui koneksi yang aman. Selain itu, cookies yang disimpan di browser dapat dimodifikasi oleh user. Django menyimpan informasi autentikasi di server-side dan hanya menggunakan ID session di cookies. Risiko lainnya terdapat serangan Cross-Site Scripting (XSS), yang artinya script berbahaya dapat mencuri cookies. untuk mengurangi risiko ini, atribut ```HttpOnly``` dapat digunakan untuk mencegah akses JavaScript ke cookies, serta atribut ```SameSite``` untuk melindungi cookies dari serangan CSRF (Cross-Site Request Forgery). Selain itu, cookies harus memiliki masa berlaku yang terbatas (timeout) agar tidak tetap aktif setelah waktu tertentu.
   
   Berikut skema mengenai serangan XSS:
   ![image](https://github.com/user-attachments/assets/cbb1d7f2-2b92-4575-8d7e-4e407512f95a)

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
      - user mengisi semua field dalam form, dan saat tombol submit ```Add Product Form``` diklik, semua data form (termasuk file yang diunggah jika ada) dikirim ke server melalui metode ```POST```.
      - Saat form disubmit, form akan dikirim ke URL yang sama (jika tidak ada action pada form). Data yang dikirimkan akan divalidasi di view (```create_product_entry```) menggunakan ```form.is_valid()```.
      - CSRF token memastikan bahwa form dikirim oleh user yang sah dan tidak dari sumber berbahaya. Django akan memeriksa apakah CSRF token yang dikirimkan cocok dengan token yang diharapkan.
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

   Menurut saya JSON lebih baik dibandingkan dengan XML karena JSON memiliki readability dan struktur data yang sederhana sehingga lebih mudah untuk dibaca. Tidak seperti JSON, XML mempunyai struktur data yang cukup kompleks serta useran tag pembuka dan tag penutup yang membuat isi file menjadi lebih panjang sehingga cenderung sulit untuk dibaca. Selain itu, JSON kompatibel dengan Javascript, artinya JSON dapat digunakan langsung di Javascript tanpa adanya konversi tambahan. JSON juga lebih mudah di-serialize karena banyak built-in yang mendukung penanganan JSON pada programming language.
   
##  Jelaskan fungsi dari method is_valid() pada form Django dan mengapa kita membutuhkan method tersebut?

   Method dari ```is_valid()``` secara garis besar berfungsi untuk melakukan validasi terhadap input-input yang diberikan pada field. Method ```is_valid()``` juga memberikan pesan atau informasi apabila ada input yang salah sehingga user dapat mengetahui apa data yang seharusnya diinput pada field. Kita membutuhkan method ini untuk menjaga keamanan data dengan memastikan bahwa data yang diterima oleh input adalah data yang valid dan sesuai dengan formatnya. Ini mencegah kesalahan dan potensi masalah keamanan yang dapat muncul dari data yang tidak valid. Selain itu, data yang tidak valid dapat menyebabkan app tidak berjalan dengan semestinya. Maka dari itu, method ```is_valid()``` memiliki peran penting untuk menjaga validasi data.
   
##  Mengapa kita membutuhkan csrf_token saat membuat form di Django? Apa yang dapat terjadi jika kita tidak menambahkan csrf_token pada form Django? Bagaimana hal tersebut dapat dimanfaatkan oleh penyerang?

   useran ```csrf_token``` berfungsi untuk memastikan bahwa request yang diberikan pada app dikirimkan oleh user yang sah dan bukan dari pihak lain. Ini artinya ```csrf_token``` dapat mencegah terjadinya serangan CSRF(Cross Site Request Forgery).
   
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

## Melakukan add-commit-push ke GitHub.

   1. Lakukan command ```git add .``` pada terminal. Command ini berfungsi untuk menyimpan semua perubahan pada file ke staging area.
   2. Setelah itu, lakukan command ```git commit -m [message]```. Command ini berfungsi untuk menyimpan commit ke staging area disertai dengan adanya pesan singkat yang deskriptif.
   3. Lalu, lakukan command ```git push -u origin [nama branch]```. Command ini berfungsi untuk mengirim(push) perubahan dari branch lokal ke remote repository yang bernama origin. 


# Tugas 2: Pengenalan Aplikasi Django dan Model-View-Template (MVT) pada Django

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
