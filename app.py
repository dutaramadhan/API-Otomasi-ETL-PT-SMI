from flask import Flask, request, jsonify, Response, send_file
from dotenv import load_dotenv
import json
from controller import extract, transform, embedding
import model
import os

app = Flask(__name__)
load_dotenv()

def upload_file(file):
    pdf_file = file
    if pdf_file:
        # Save the file to the specified folder
        pdf_file.save(os.path.join('files', pdf_file.filename))
        return 'http://' + os.getenv('DB_HOST') + ':' + os.getenv('APP_PORT') + '/files/' + pdf_file.filename

def extract_files(files):
    try:
        # Check if the POST request has both the JSON and PDF file parts
        if 'config' not in files or 'pdf_file' not in files:
            return jsonify({'error': 'Both JSON and PDF file parts are required'})

        # Access the JSON file
        config_file = files['config']
        config_data = json.load(config_file)

        # Access the PDF file
        pdf_file = files['pdf_file']
        pdf_filename = pdf_file.filename
        if config_data['split_mode'] == "pasal":
            pdf_content = extract.extractPDF(pdf_file)
        else:
            pdf_content = extract.extractPDFPerPage(pdf_file)

        # Perform processing with the JSON and PDF data
        result = {'config_data': config_data, 'pdf_filename': pdf_filename, 'pdf_content': pdf_content, 'message': 'Successfully processed JSON and PDF files'}

        return jsonify(result)

    except Exception as e:
        # Handle any potential errors
        error_message = {'error': str(e)}
        return jsonify(error_message), 400
    
def transform_files(data):
    try:
        if data['config_data']['split_mode'] == "pasal":
            result = transform.transform_pasal(data['pdf_content'], data['pdf_filename'], data['config_data']['unnecessary_patterns'], data['config_data']['title_patterns'])
        else:
            result = transform.transform_non_pasal(data['pdf_content'], data['pdf_filename'], data['config_data']['unnecessary_patterns'], data['config_data']['title_patterns'])
        return result
    except Exception as e:
        error_message = {'error': str(e)}
        return jsonify(error_message), 400

@app.route('/smi/source', methods=['POST'])
def post_source():
    try:
        source_uri = upload_file(request.files['pdf_file'])
        extracted_source =  extract_files(request.files).get_json()
        source_title, transformed_source = transform_files(extracted_source)
        source_id = model.insertSourceMetadata(source_uri, extracted_source['pdf_filename'], source_title)
        for index, content in enumerate(transformed_source):
            model.insertChunkData(source_id, content)
        
        header = extracted_source['config_data']['split_mode'] == 'pasal'
        embedding.threaded_create_embeddings(source_id, header=header)
        
        return(jsonify({'message': "Successfully Load File and its Embedding to Database"}))
    except Exception as e:
        error_message = {'error': str(e)}
        return jsonify(error_message), 400
    
@app.route('/smi/source', methods=['GET'])
def get_source_metadata():
    try:
        source_metadata = model.getSourceMetadata()
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
    
@app.route("/smi/source", methods=['DELETE'])
def delete_source():
    try:
        id = request.args.get('id')
        model.deleteSourceData(id)
        return jsonify({"success": "Sucessfully deleted the data"})
    except Exception as e:
        error_message = {'error': str(e)}
        return jsonify(error_message), 400
    
def root_dir():
    return os.path.abspath(os.path.dirname(__file__))

def get_file(filename):
    try:
        src = os.path.join(root_dir(), filename)
        return open(src, 'rb').read()  # Open in binary mode for files
    except IOError as exc:
        return str(exc)

@app.route('/files/<path:path>')
def serve_files(path):
    complete_path = os.path.join(root_dir(), 'files', path)
    
    try:
        return send_file(complete_path, mimetype='application/pdf')
    except Exception as e:
        return str(e)
    

if __name__ == '__main__':
    app.run(debug=False, port=os.getenv('APP_PORT'))