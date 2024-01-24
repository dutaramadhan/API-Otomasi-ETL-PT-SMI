<h1 align="center">ETL Automation API</h1>

## Table of Contents
1. [Information About API](#api-info)
2. [Our Main Feature](#main-feature)

   a. [Extract](#extract)

   b. [Transform](#transform)

   c. [Load](#load)

   d. [Embedding](#embedding)

   e. [Upload File](#upload)

   f. [Delete File and Data](#delete)

   g. [Serve File](#serve)

   h. [Get Metadata](#get-metadata) 
4. [System's Flow](#systems-flow)
5. [Tech Stack](#tech-stack)
6. [How to Set Up](#set-up)
   
   a. [Postgresql](#postgres)
   
   b. [pgvector](#pgvector)
7. [How to Run Locally](#run-local)
8. [How to Deploy](#deploy)
9. [Live Instance](#live-instance)
10. [API Endpoint](#endpoint)
11. [Related Repository](#related-repo)

<a name="api-info"></a>
## Information About this API
API ini berfungsi untuk melakukan otomatisasi proses penginputan dan embedding sumber data untuk data knowledge base. Pengguna dapat memasukan input berupa file peraturan dengan ekstensi PDF yang memiliki format berupa teks dan juga file config dalam format JSON untuk menentukan split mode, pattern untuk penghapusan pola yang tidak diperlukan, serta pattern pemecahan atau splitting untuk memperoleh judul dari peraturan yang dimasukan. Dengan menggunakan API ini pengguna dapat melakukan input dan embedding ke database dengan lebih cepat dan efisien dengan menyembunyikan proses yang terjadi di belakangnya.  

<a name="main-feature"></a>
## Main Features
<a name="extract"></a>
### a. Extract
Fitur untuk proses ektraksi file PDF menjadi sebuah teks. Untuk file yang memiliki split mode pasal, file akan diekstraksi menjadi satu teks utuh. Untuk file yang memiliki split mode non pasal, file akan diekstraksi per halaman dan menghasilkan output berupa list teks. 
<a name="transform"></a>
### b. Transform
Fitur untuk proses pembersihan dan transformasi untuk data yang sudah diekstraksi. Data akan dibersihkan dari pattern yang tidak diperlukan atau diinginkan, misalnya seperti nomor halaman, link, dll. Dari data juga akan dicari judul peraturan dari sumber yang sudah diekstraksi sebelumnya. Setelah itu untuk data yang memiliki split mode pasal, data akan di pecah berdasarkan pasal dan pada bagian depan dari data akan ditambahkan informasi mengenai bab dan juga pasal dari data tersebut. Tidak hanya itu, setiap data juga akan dicari informasi headernya, yaitu judul sumber, nama file sumber dan pasal. 
<a name="load"></a>
### c. Load
Fitur untuk proses penyimpanan data ke dalam database yang kemudian di-retrieval atau diambil untuk proses embedding. Hasil dari proses embedding tersebut akan disimpan ke database dalam bentuk vektor. 
<a name="embedding"></a>
### d. Embedding
Fitur untuk proses embedding setiap data yang baru dimuat menggunakan model text-embedding-ada-002 dari OpenAI. Embedding merupakan proses mengekstrak makna atau konsep informasi dari data teks menjadi sebuah vektor. Terdapat 2 proses embedding yaitu 
- embedding content : gabungan judul sumber dan konten
- embedding header : gabungan judul sumber, nama file sumber dan pasal (hanya untuk split mode pasal)
<a name="upload"></a>
### e. Upload File
Fitur yang memungkinkan pengguna untuk mengunggah file PDF ke sistem. Setelah berhasil diunggah, file tersebut akan siap untuk menjalani proses ekstraksi, transformasi, embedding, dan penyimpanan ke dalam database.
<a name="delete"></a>
### f. Delete File and Data
Fitur yang memungkinkan pengguna untuk menghapus file beserta data terkait dari sistem. Pengguna dapat memilih file yang ingin dihapus dengan memasukan id dari file. Id tersebut diperoleh dari id file yang tersimpan di database. Sistem kemudian akan menghapus file dari server beserta dengan data-datanya yang tersimpan di database.
<a name="serve"></a>
### g. Serve File
Fitur yang memungkinkan pengguna untuk mengakses file yang telah diunggah dengan memasukan url yang terkait dengan file tersebut.
<a name="get-metadata"></a>
### h. Get Metadata
Fitur yang memberikan informasi metadata terkait file yang telah diunggah, seperti id file, nama file, judul file, tanggal unggah, dan url tempat file disimpan. Metadata ini dapat memberikan gambaran singkat kepada pengguna mengenai file yang telah berhasil diunggah ke dalam sistem.

<a name="systems-flow"></a>
## System's Flow
Berikut adalah alur proses ETL dan penanaman data.
![Alur ETL dan Embedding](https://drive.google.com/uc?id=1m0AnbubnMsr-_8Qd88fsc0mvMIEzTQy7)
1. File PDF diekstrak menjadi teks
2. Teks dilakukan transformasi untuk dipecah menjadi potongan-potongan kecil dan dilakukan pembersihan data. Terdapat 2 mode pemecahan : per page atau per pasal.
3. Setiap potongan data dimuat ke basis data
4. Setiap potongan data dilakukan proses embedding menggunakan model OpenAI.
5. Hasil embedding berupa vector dimuat kembali ke basis data

<a name="tech-stack"></a>
## Tech Stack
### 1. Python
### 2. Flask
### 3. OpenAI
### 4. Postgresql
### 5. pgvector
### 6. Docker

<a name="set-up"></a>
## How to Set Up
<a name="postgres"></a>
### a. Postgresql
Skema database
```
CREATE DATABASE IF NOT EXISTS your_database_name;
```
```
CREATE TABLE IF NOT EXISTS public.source_metadata
(
    source_uri character varying,
    source_name character varying,
    source_title character varying,
    created_at timestamp without time zone DEFAULT now(),
    id SERIAL NOT NULL,
    CONSTRAINT source_metadata_pkey PRIMARY KEY (id)
)
```
```
CREATE TABLE IF NOT EXISTS public.data
(
    content text,
    total_tokens integer,
    source_id integer,
    id SERIAL NOT NULL,
    embedding vector(1536),
    header_embedding vector(1536),
    CONSTRAINT data_pkey PRIMARY KEY (id),
    CONSTRAINT source FOREIGN KEY (source_id)
        REFERENCES public.source_metadata (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)
```
<a name="pgvector"></a>
### b. pgvector
Untuk lebih jelasnya bisa dilihat pada <a href='https://github.com/pgvector/pgvector'>repositori github pgvector</a>

<a name="run-local"></a>
## How to Run Locally
1. Clone repositori ini
   ```
   git clone https://github.com/dutaramadhan/API-Query-Data-PT-SMI.git
   ```
2. Buka direktori API-Query-Data-PT-SMI
3. Install pyhton virtual environtment 
   ```
   pip install virtualenv
   ```
4. Buat virtual environment
   ```
   virtualenv venv
   ```
6. Aktifkan virtual environment
   - Windows
     ```
     venv/Scripts/activate
     ```
   - Linux/macOS
     ```
     source venv/bin/activate
     ```
7. Install semua library atau depedensi yang dibutuhkan
   ```
   pip install -r requirements.txt
   ```
8. Buat file .env
   ```
   API_KEY = ...
   DB_HOST = ... 
   DB_DATABASE = ...
   DB_USER = ...
   DB_PASSWORD = ...
   DB_PORT = ...
   APP_PORT = ...
   ```
9. Jalankan aplikasi
   ```
   python app.py
   ```
10. Cek apakah server sedang berjalan
    ```
    http://localhost:5000/
    ```

<a name="deploy"></a>
## How to Deploy
1. Buat file .env
   ```
      API_KEY = ...
      DB_HOST = ... 
      DB_DATABASE = ...
      DB_USER = ...
      DB_PASSWORD = ...
      DB_PORT = ...
      APP_PORT = ...
   ```
2. Build docker image
   ```
   docker build -t api-etl .
   ```
3. Run docker image
   ```
   docker run -d -p 5001:5001 -v /home/smiuser/sources-files:/app/files --name api-etl api-etl
   ```
4. Cek apakah server sedang berjalan
    ```
    http://<ip-host>:5001/
    ```
    
<a name="live-instance"></a>
## Live Instance
http://10.10.6.69:5001

<a name="endpoint"></a>
## API Endpoint
### 1. Post source file
- ##### Route
  ```
  POST /smi/source
  ```
- ##### Request Body
   | KEY           | VALUE         | DESCRIPTION |
   | ------------- |:-------------:|--|
   | pdf_file      | file.pdf      | sources files |
   | config        | config.json   | configuration of sources  |
  
  config.json
  ```
  {
     "split_mode": "pasal" OR "page",
     "unnecessary_patterns" : [ regex ],
     "title_patterns": [ regex ]
  }
  ```
- ##### Response
  ```
  { "message": "Successfully Load File and its Embedding to Database" }
  ```

### 2. Get Source Metadata
- ##### Route
  ```
  GET /smi/source
  ```
- ##### Response
  ```
  [
    {
        "created_at": timestamp,
        "id": int,
        "source_name": string,
        "source_title": string,
        "source_uri": string
    },
  ]
  ```
### 3. Delete Source Data
- ##### Route
  ```
  DELETE /smi/source
  ```
- ##### Parameters
  ```
  id: int
  ```
- ##### Response
  ```
  {"success": "Sucessfully deleted the data and file"}
  ```
### 4. Serve File
- #### Route
  ```
  GET /files/<path>
  ```
- #### Parameters
  ```
  path: filename
  ```
- #### Response
  PDF file

<a name="related-repo"></a>
## Related Repository
- <a href='https://github.com/dutaramadhan/API-Query-Data-PT-SMI'>API-Query-Data-PT-SMI</a>


