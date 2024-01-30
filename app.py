from flask import Flask, request, jsonify, Response, send_file, abort
from dotenv import load_dotenv
import json
from controller import extract, transform, embedding
import model
import os
import logging
import threading

app = Flask(__name__)
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def upload_file(pdf_file):
    try:
        if pdf_file:
            # Save the file to the specified folder
            path = os.path.join('files', pdf_file.filename)
            pdf_file.save(path)
            url = 'http://' + os.getenv('DB_HOST') + ':' + os.getenv('APP_PORT') + '/files/' + pdf_file.filename
            return url, path, pdf_file.filename
    except Exception as e:
        abort(400, str(e))

def delete_file(filename):
    try:
        file_path = os.path.join('files', filename)
        if os.path.exists(file_path):
            os.remove(file_path)
            logger.info(f"File '{filename}' deleted successfully.")
        else:
            logger.warning(f"File '{filename}' not found.")
    except Exception as e:
        abort(400, str(e))

def extract_files(filepath, filename, config_data):
    try:
        # Access the PDF file
        if config_data['split_mode'] == "pasal": 
            pdf_content = extract.extract_pdf(filepath)
        else:
            pdf_content = extract.extract_pdf_per_page(filepath)

        result = {'config_data': config_data, 'pdf_filename': filename, 'pdf_content': pdf_content, 'message': 'Successfully processed JSON and PDF files'}

        return result

    except Exception as e:
        abort(400, str(e))
    
def transform_files(data):
    try:
        if data['config_data']['split_mode'] == "pasal":
            result = transform.transform_pasal(data['pdf_content'], data['pdf_filename'], data['config_data']['unnecessary_patterns'], data['config_data']['title_patterns'], data['config_data']['split_patterns'], data['config_data']['resplit_patterns'])
        else:
            result = transform.transform_non_pasal(data['pdf_content'], data['pdf_filename'], data['config_data']['unnecessary_patterns'], data['config_data']['title_patterns'])
        return result
    except Exception as e:
        abort(400, str(e))

def ETL_proccess(path, filename, config_data, source_uri):
    extracted_source = extract_files(path, filename, config_data)
    source_title, transformed_source = transform_files(extracted_source)

    source_id = model.insert_source_metadata(source_uri, extracted_source['pdf_filename'], source_title)

    for index, content in enumerate(transformed_source):
        model.insert_chunk_data(source_id, content)
    
    header = extracted_source['config_data']['split_mode'] == 'pasal'
    return source_id, header

@app.route('/smi/source', methods=['POST'])
def post_source():
    try:
        if 'pdf_file' not in request.files or 'config' not in request.files:
            return jsonify({'error': 'No PDF or config file part'}), 400
        
        # Access the JSON config file
        config_data = json.load(request.files['config'])

        sources = []

        # save file and ETL
        for pdf_file in request.files.getlist('pdf_file'):
            source_uri, path, filename = upload_file(pdf_file)
            source_id, header = ETL_proccess(path, filename, config_data, source_uri)
            sources.append((source_id, header))

        # embedding proccess
        for source_id, header in sources:
            embedding.threaded_create_embeddings(source_id, header=header)  

        return jsonify({
            'message': "Successfully Load File to Database and start Embedding Proccess", 
            'source_id': [source_id for source_id, _ in sources]
        })
    except Exception as e:
        error_message = {'error': str(e)}
        return jsonify(error_message), 400

    
@app.route('/smi/source', methods=['GET'])
def get_source_metadata():
    try:
        source_metadata = model.get_source_metadata()
        response = []
        for metadata in source_metadata:
            entry = {
                "id" : metadata[4], 
                "source_uri" : metadata[0],
                "source_name" : metadata[1],
                "source_title" : metadata[2],
                "created_at" : metadata[3],
            }
            response.append(entry)
        return jsonify(response)      
    except Exception as e:
        error_message = {'error': str(e)}
        return jsonify(error_message), 400
    
@app.route('/smi/source/data', methods=['GET'])
def get_data():
    try:
        source_id = request.args.get('id')
        source_data = model.get_data(source_id)
        source_info = model.get_data_info(source_id)
        
        response = {
            'count': source_info[0],
            'count_embedded': source_info[1],
            'embedding_proccess': f'{source_info[1] / source_info[0] * 100:.3f}%',
            'source_name': source_info[2],
            'source_uri': source_info[3],
            'source_title': source_info[4],
            'data': [],
        }
        for data in source_data:
            entry = {
                "content" : data[0], 
                "length" : data[1],
            }
            response['data'].append(entry)
        return jsonify(response)
    except Exception as e:
        error_message = {'error': str(e)}
        return jsonify(error_message), 400
    
@app.route("/smi/source", methods=['DELETE'])
def delete_source():
    try:
        id = request.args.get('id')
        source_name = model.delete_source_data(id)
        delete_file(source_name)
        return jsonify({"success": "Sucessfully deleted the data and file"})
    except Exception as e:
        error_message = {'error': str(e)}
        return jsonify(error_message), 400
    
def root_dir():
    return os.path.abspath(os.path.dirname(__file__))

def get_file(filename):
    try:
        src = os.path.join(root_dir(), filename)
        return open(src, 'rb').read()
    except IOError as exc:
        return str(exc)

@app.route('/files/<path:path>')
def serve_files(path):
    complete_path = os.path.join(root_dir(), 'files', path)
    
    try:
        return send_file(complete_path, mimetype='application/pdf')
    except Exception as e:
        return str(e)
    
@app.route('/')
def info():
    return 'Server is Running on port ' + os.getenv('APP_PORT') 

if __name__ == '__main__':
    app.run(debug=False, port=os.getenv('APP_PORT'))