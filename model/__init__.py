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

def selectOne():
  conn = psycopg2.connect(**db_params)
  cursor = conn.cursor()

  # Execute a SELECT query to fetch one row
  query = "SELECT content, source_title, source_name, data.id FROM data INNER JOIN source_metadata ON data.source_id = source_metadata.id WHERE header_embedding is NULL AND is_header_embedded = FALSE LIMIT 1"
  cursor.execute(query)

  # Fetch the first row from the result set
  [content, source_title, source_name, id] = cursor.fetchone()
  content = source_title + '\n' + content
  

  cursor.close()
  conn.close()
  return [content, id, source_title, source_name]

def storeEmbedding(id, embedding):
  conn = psycopg2.connect(**db_params)
  cursor = conn.cursor()
  update_query = "UPDATE data SET header_embedding = %s, is_header_embedded = TRUE WHERE id = %s;"

  # Execute the update query
  cursor.execute(update_query, (embedding, id))

  # Commit the changes
  conn.commit()
  cursor.close()
  conn.close()

