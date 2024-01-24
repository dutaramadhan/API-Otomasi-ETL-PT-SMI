<h1 align="center">ETL Automation API</h1>

## Information About this API
API ini berfungsi untuk melakukan otomatisasi proses penginputan dan embedding sumber data untuk data knowledge base. Pengguna dapat memasukan input berupa file peraturan dengan ekstensi PDF yang memiliki format berupa teks dan juga file config dalam format JSON untuk menentukan split mode, pattern untuk penghapusan pola yang tidak diperlukan, serta pattern pemecahan atau splitting untuk memperoleh judul dari peraturan yang dimasukan. Dengan menggunakan API ini pengguna dapat melakukan input dan embedding ke database dengan lebih cepat dan efisien dengan menyembunyikan proses yang terjadi di belakangnya.  
 
## Main Features
### 1. Extract
fitur untuk proses ektraksi file PDF menjadi sebuah teks. Untuk file yang memiliki split mode pasal, file akan diekstraksi menjadi satu teks utuh. Untuk file yang memiliki split mode non pasal, file akan diekstraksi per halaman dan menghasilkan output berupa list teks. 
### 2. Transform
Fitur untuk proses pembersihan dan transformasi untuk data yang sudah diekstraksi. Data akan dibersihkan dari pattern yang tidak diperlukan atau diinginkan, misalnya seperti nomor halaman, link, dll. Dari data juga akan dicari judul peraturan dari file yang sudah diekstraksi sebelumnya. Setelah itu untuk data yang memiliki split mode pasal, data akan di pecah berdasarkan pasal dan pada bagian depan dari data akan ditambahkan informasi mengenai bab dan juga pasal dari data tersebut. Tidak hanya itu, setiap data juga akan dicari informasi headernya, yaitu judul peraturan ditambah keterangan pasal. 
### 3. Load
Fitur untuk proses penyimpanan data ke dalam database yang kemudian di-retrieval atau diambil untuk proses embedding. Hasil dari proses embedding tersebut akan disimpan kedalam database dalam bentuk vektor. 
### 4. Embedding
Pada tahap ini setiap data yang ada didatabase akan diambil untuk proses 
### 5. Upload File
Fitur 
### 6. Delete File and Data
### 7. Serve File
### 8. Get Metadata

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
### 1. Postgresql
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
### 2. pgvector
Untuk lebih jelasnya bisa dilihat pada <a href='https://github.com/pgvector/pgvector'>repositori github pgvector</a>

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

## Related Repository
- <a href='https://github.com/dutaramadhan/API-Query-Data-PT-SMI'>API-Query-Data-PT-SMI</a>


