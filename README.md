<h1 align="center">ETL Automation API</h1>

## Information About this API

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
