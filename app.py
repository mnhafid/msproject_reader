import os
from flask import Flask, flash, request, redirect, url_for
from flask_restful import Resource, Api
from werkzeug.utils import secure_filename
from mpp_reader import read_mpp

UPLOAD_FOLDER = 'files'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mpp'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

api = Api(app)

class FileHandler(Resource):

    def allowed_file(self, filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    
    def post(self):
        # Get Text type fields
        form = request.form.to_dict()
        print(form)

        if 'file' not in request.files:
            return 'No file part'
        
        file = request.files.get("file")
        if file and self.allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            read_mpp(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return 'File uploaded successfully'

api.add_resource(FileHandler, "/")

app.run(debug=True)