# -*- coding: utf-8 -*-
"""
Valerie DESNOUX
8 avril 2021

Testing flask script file.
"""

from flask import Flask, request, redirect, send_from_directory, Response
from werkzeug.utils import secure_filename
import os
from flask import render_template
import Solex_recon_flask as sol

UPLOAD_FOLDER='static/myupload'

app = Flask(__name__)

ALLOWED_EXTENSIONS = {'ser'}
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER
app.secret_key = 'QRVulHD192685'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/result/<basefich>')
def results(basefich):
    #basefich=session['basefich']
    print('result :', basefich)
    basefich2=basefich
    myfichtxt=os.path.join(app.config['UPLOAD_FOLDER'],basefich+'.txt')
    basefich='/'+os.path.join(app.config['UPLOAD_FOLDER'], basefich)
    list_files=[]
    list_files2=[]
    list_files.append(basefich+'_recon.fits')
    list_files.append(basefich+'_img.fits')
    list_files.append(basefich+'_mean.fits')
    list_files.append(basefich+'.txt')
    list_files2.append(basefich2+'_recon.fits')
    list_files2.append(basefich2+'_img.fits')
    list_files2.append(basefich2+'_mean.fits')
    list_files2.append(basefich2+'.txt')
    myimage=basefich+'_disk.png'
    
    with open(myfichtxt, "r") as txtf:
        log_txt=txtf.read().split(';')
    return render_template('result.html', base=basefich2+'.ser', log=log_txt,name=list_files, name2=list_files2, img=myimage)
    


@app.route('/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/',methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        print(request.method)
        print (request.files)
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        print (file)
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            serfile=os.path.join(app.config['UPLOAD_FOLDER'], filename)
            #basefich=os.path.splitext(serfile)[0]
            #print ('upload ',basefich)
            #session['basefich']=basefich
            def inner():
                sol.solex_proc_all(serfile, filename)
            return Response(sol.solex_proc_all(serfile, filename), mimetype='text/html')
            #return render_template('yield_results.html', base=filename)
            #return render_template('yield_results.html', base=filename, name=list_files, img=myimage)
            
    return render_template('upload.html')

    
if __name__== "__main__":
    app.run(debug=True)
    #app.run (host='192.168.1.27')