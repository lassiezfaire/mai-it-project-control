from flask import Flask, request, send_file
import os
import subprocess

app = Flask(__name__)


@app.route('/test', methods=['GET'])
def conn_test():
    return 'OK'


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part in the request', 400
    file = request.files['file']
    name = request.form['name']
    if file.filename == '':
        return 'No selected file', 400
    if file:
        uploads_path = '/var/cartoonizer/uploads'
        results_path = '/var/cartoonizer/uploads'
        file.save(os.path.join(uploads_path, name))
        whitebox_run(source_path=uploads_path + '/' + name, result_path=results_path)
        return send_file(results_path + '/' + name + '_infered.png', as_attachment=True)


def whitebox_run(source_path, result_path):
    python = 'python'

    ml_directory = 'White-box-Cartoonization-PyTorch/'
    executable = 'inference.py'

    source_key = '--source'

    weight_key = '--weight_path'
    weight_path = ml_directory + 'weights/sceneryonly.pth.tar'

    result_key = '--dest_folder'

    command = (python + ' ' +
               ml_directory + executable + ' ' +
               source_key + ' ' + source_path + ' ' +
               weight_key + ' ' + weight_path + ' ' +
               result_key + ' ' + result_path)

    print(command)

    subprocess.call(["python", ml_directory + executable,
                     source_key, source_path,
                     weight_key, weight_path,
                     result_key, result_path])


if __name__ == "__main__":
    from waitress import serve
    serve(app, host='127.0.0.1', port=5000)
