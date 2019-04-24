
import os
from pyvoce import SpeechInterface, SourceSeparation
from flask import Flask, flash, jsonify, redirect, render_template, request, send_from_directory, url_for
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '.\\audio\\input'
OUTPUT_FOLDER = '.\\audio\\output'
ALLOWED_EXTENSIONS = set(['wav', 'mp3'])
SEPARATION_METHODS = set(['repet', 'repet_sim', 'hpss', 'nmf_mfcc'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
model = None

interface = SpeechInterface()
separator = SourceSeparation()


def initialize():
	interface.init('libraries\\voce-0.9.1\\lib', True, False, '', '')

def synthesize_text(text):
	global interface
	interface.synthesize(text)

def destroy():
	interface.destroy()

# @app.route("/synthesize", methods=["POST"])
@app.route("/synthesize/<text>/")
def synthesize(text):
	synthesize_text(text)
	return "Successfully synthesised \"%s\"" % text

@app.route("/")
def index():
	initialize()
	input_files = list()
	output_files = list()
	for a,b,f in os.walk(app.config['UPLOAD_FOLDER']):
		input_files = f
	for a,b,f in os.walk(app.config['OUTPUT_FOLDER']):
		output_files = f
	print input_files
	return render_template('home.html', input_files=input_files, separation_methods=SEPARATION_METHODS)

@app.route("/files/")
def files():
	input_files = list()
	output_files = list()
	for a,b,f in os.walk(app.config['UPLOAD_FOLDER']):
		input_files = f
	for a,b,f in os.walk(app.config['OUTPUT_FOLDER']):
		output_files = f
	return render_template('files.html', input_files=input_files, output_files=output_files)

def allowed_file(filename):
	return '.' in filename and \
		filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/upload/", methods=['POST'])
def upload_file():
	if request.method == 'POST':
		if 'file_upload' not in request.files:
			flash('no file part')
			return redirect(request.referrer)

		file = request.files['file_upload']

		if file.filename == '':
			flash('no selected file')
			return redirect(request.referrer)

		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
	return redirect(request.referrer)

@app.route("/get-file/")
def get_file():
	filename = request.args.get('filename', '')
	filetype = request.args.get('filetype', 'input')
	if filetype == "output":
		return send_from_directory(app.config['OUTPUT_FOLDER'], filename=filename, as_attachment=True, attachment_filename=filename)
	else:
		return send_from_directory(app.config['UPLOAD_FOLDER'], filename=filename, as_attachment=True, attachment_filename=filename)


@app.route("/delete-file/", methods=['POST'])
def delete_file():
	#implement delete file
	filename = request.form['filename']
	filetype = request.form['filetype']
	if filetype == "input":
		print os.path.join(app.config['UPLOAD_FOLDER'], filename)
		os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
	else:
		os.remove(os.path.join(app.config['OUTPUT_FOLDER'], filename))
	return "Deleted"

def separate(source_file, method):
	print("Source Separation.\nFile: %s. Method: %s" % (source_file, method))
	separator.set_file(source_file)
	f_name, f_ext = source_file.rsplit(".", 1)
	f_name = f_name.rsplit("\\", 1)[1]
	separator.plot(0, True, f_name, os.path.join(app.config['OUTPUT_FOLDER'], f_name))
	if method == "repet_sim":
		return separator.repet_sim()
	elif method == "hpss":
		return separator.hpss()
	elif method == "nmf_mfcc":
		return separator.nmf_mfcc()
	else:
		return separator.repet()

@app.route("/separate/", methods=['POST'])
def do_separation():
	filename = request.form['filename']
	method = request.form['method']
	background, foreground = separate(os.path.join(app.config['UPLOAD_FOLDER'], filename), method)
	f_name, f_ext = filename.rsplit(".", 1)
	bg_name = f_name + "-" + method + "-bg." + f_ext
	fg_name = f_name + "-" + method + "-fg." + f_ext
	background.write_audio_to_file(os.path.join(app.config['OUTPUT_FOLDER'], bg_name))
	foreground.write_audio_to_file(os.path.join(app.config['OUTPUT_FOLDER'], fg_name))
	# create plots
	print("plotting")
	bg_img_name = f_name + "-" + method + "-bg"
	fg_img_name = f_name + "-" + method + "-fg"
	foreground.plot_time_domain(0, True, fg_name, os.path.join(app.config['OUTPUT_FOLDER'], fg_img_name))
	background.plot_time_domain(0, True, bg_name, os.path.join(app.config['OUTPUT_FOLDER'], bg_img_name))
	print("completed")
	return jsonify(input_file=filename, method=method, bg_file=bg_name, fg_file=fg_name, bg_img=bg_img_name+".png", fg_img=fg_img_name+".png", original_img=f_name+".png")

if __name__ == "__main__":
	print("Initialising SpeechInterface... starting server")
	app.run(debug=True)
