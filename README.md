<h1 align="center">ETL Automation API</h1>

## Information About this API

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
