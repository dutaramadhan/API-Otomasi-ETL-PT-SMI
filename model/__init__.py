import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv
import os

load_dotenv()

db_params = {
    'host': os.getenv('DB_HOST'),
    'database':  os.getenv('DB_DATABASE'),
    'user':  os.getenv('DB_USER'),
    'password':  os.getenv('DB_PASSWORD'),
    'port':  os.getenv('DB_PORT'),
}

def insertSourceMetadata(source_uri, source_name, title):
  conn = psycopg2.connect(**db_params)
  cur = conn.cursor()

  col_name = "source_uri, source_name, source_title"
  table_name = "source_metadata"

  query = "INSERT INTO {} ({}) VALUES (%s, %s, %s) RETURNING id;".format(table_name, col_name)

  try:
    cur.execute(query, (source_uri, source_name, title))
    source_id = cur.fetchone()[0]
    conn.commit()
    return source_id
  except Exception as e:
    print(f"Error inserting data: {e}")
    conn.rollback()
    return None
  finally:
    cur.close()
    conn.close()


def insertChunkData(source_id, chunk):
  conn = psycopg2.connect(**db_params)
  cur = conn.cursor()

  col_name = "source_id, content"
  table_name = "data"

  query = "INSERT INTO {} ({}) VALUES (%s, %s) RETURNING id;"
  query = query.format(table_name, col_name)
  try:
    cur.execute(query, (source_id, chunk))
    id = cur.fetchone()[0]
    conn.commit()
    return id 
  except Exception as e:
    print(f"Error inserting data: {e}")
    conn.rollback()
    return None
  finally:
    cur.close()
    conn.close()

def selectOne(source_id):
  conn = psycopg2.connect(**db_params)
  cursor = conn.cursor()

  # Execute a SELECT query to fetch one row
  query = "SELECT content, source_title, source_name, data.id FROM data INNER JOIN source_metadata ON data.source_id = source_metadata.id WHERE embedding is NULL AND source_id=%s LIMIT 1"
  cursor.execute(query, (source_id, ))

  # Fetch the first row from the result set
  data = cursor.fetchone()
  #content = source_title + '\n' + content
  
  cursor.close()
  conn.close()
  return data

def storeEmbedding(id, embedding, token, header_embedding):
  conn = psycopg2.connect(**db_params)
  cursor = conn.cursor()
  update_query = "UPDATE data SET embedding = %s, header_embedding = %s, total_tokens = %s WHERE id = %s;"

  # Execute the update query
  cursor.execute(update_query, (embedding, header_embedding, token, id))

  # Commit the changes
  conn.commit()
  cursor.close()
  conn.close()

