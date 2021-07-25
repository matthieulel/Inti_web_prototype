# -*- coding: utf-8 -*-
"""
Valerie DESNOUX
8 avril 2021

Testing flask script file.
"""

from flask import Flask, request, redirect, send_from_directory, Response, jsonify
# from flask.wrappers import JSONMixin
from werkzeug.utils import secure_filename
import os
from flask import render_template
import Solex_recon_flask as sol
import threading, queue
from shutil import copyfile
import os
import glob
from zipfile import ZipFile
import sunpro

#Ajout à réfléchir
from PIL import Image
import PIL.ImageOps



import watchdog.events 
#import watchdog.observers 
from watchdog.observers  import Observer
import time 


UPLOAD_FOLDER='static/uploads'

app = Flask(__name__)

ALLOWED_EXTENSIONS = {'ser'}
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER
app.secret_key = 'QRVulHD192685'

workspace_in_progress = ''

#init watchdog thread ref
observer =''
watching_folder = ''























def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# nettoyage du dossier uploads
def remove_uploads_files():

    files = glob.glob(UPLOAD_FOLDER + '/*')

    for f in files:
        print(f)
        try:
            os.remove(f)
        except OSError as e:
            print("Error: %s : %s" % (f, e.strerror))



def process(serfile, filename):
    sol.solex_proc_all(serfile, filename)

def processthreaded(serfile, filename):
    sol.solex_proc_all(serfile, filename)
    #q.put(1)
    



def create_zip(directory_path, zip_filename):

    print('PATH', directory_path)
    print('Name', zip_filename)


    # create a ZipFile object
    zipObj = ZipFile(directory_path+ '/' + zip_filename+'.zip', 'w')
    # Add multiple files to the zip
    zipObj.write(directory_path+ '/' + zip_filename + '_disk.png')
    zipObj.write(directory_path+ '/' + zip_filename +  '_disk_invert.png')
    zipObj.write(directory_path+ '/' + zip_filename +  '.txt')
    zipObj.write(directory_path+ '/' + zip_filename +  '_circle.fits')
    zipObj.write(directory_path+ '/' + zip_filename +  '_corr.fits')
    zipObj.write(directory_path+ '/' + zip_filename +  '_flat.fits')
    zipObj.write(directory_path+ '/' + zip_filename +  '_img.fits')
    zipObj.write(directory_path+ '/' + zip_filename +  '_mean.fits')
    zipObj.write(directory_path+ '/' + zip_filename +  '_recon.fits')

    # close the Zip File
    zipObj.close()

    copyfile(directory_path+ '/' + zip_filename + '.zip' , 'static/uploads/'+ zip_filename + '.zip')

    return 'static/uploads/'+ zip_filename + '.zip'



@app.route('/', methods=['GET', 'POST'])
def single():

    if request.method == "POST":
        #value=request.json['data']
        dir_to_process = request.get_json()
        print(dir_to_process['folder'])
        print(dir_to_process['ser'])

        #launch process
        sol.solex_proc_all(dir_to_process['folder'] + '/' + dir_to_process['ser'], dir_to_process['ser'])


        # set file name and copy all files in static for sent to the view and manipulations
        file = dir_to_process['ser'].split('.')
        copyfile(dir_to_process['folder']+ '/' + file[0] + '_disk.png' , 'static/uploads/'+ file[0] + '_disk.png')
        copyfile(dir_to_process['folder']+ '/' + file[0] + '_disk_invert.png' , 'static/uploads/'+ file[0] + '_disk_invert.png')
        copyfile(dir_to_process['folder']+ '/' + file[0] + '.txt' , 'static/uploads/'+ file[0] + '.txt')
        copyfile(dir_to_process['folder']+ '/' + file[0] + '_circle.fits' , 'static/uploads/'+ file[0] + '_circle.fits')
        copyfile(dir_to_process['folder']+ '/' + file[0] + '_corr.fits' , 'static/uploads/'+ file[0] + '_corr.fits')
        copyfile(dir_to_process['folder']+ '/' + file[0] + '_flat.fits' , 'static/uploads/'+ file[0] + '_flat.fits')
        copyfile(dir_to_process['folder']+ '/' + file[0] + '_img.fits' , 'static/uploads/'+ file[0] + '_img.fits')
        copyfile(dir_to_process['folder']+ '/' + file[0] + '_mean.fits' , 'static/uploads/'+ file[0] + '_mean.fits')
        copyfile(dir_to_process['folder']+ '/' + file[0] + '_recon.fits' , 'static/uploads/'+ file[0] + '_recon.fits')




        # creation du fichier zip contenant tous les fichiers
        zip_path = create_zip(dir_to_process['folder'], str(file[0]))


        jsonReturn  = {
            'imgsrc' : 'static/uploads/'+ file[0]  + '_disk.png',
            'invert_imgsrc' : 'static/uploads/'+ file[0]  + '_disk_invert.png',
            'imgser' :  dir_to_process['ser'],
            'zip_path' : zip_path
        }


        #parse txt file for sent to the view
        with open('static/uploads/'+ file[0] + '.txt','r') as f:
            for line in f:
                for word in line.split(';'):
                    #print(word)    
                    items = word.split(':')
                    item = items[0]
                    try :
                        value= items[1]
                    except :
                        value= ''
                    #value = items[1]
                    jsonReturn[item] = value
                    print(jsonReturn)

    

        # Si SDO actif -> récupèration des chemin des deux fichiers
        if(dir_to_process['sdo'] == 1):

            year, month, day = dir_to_process['sdo_date'].split('-')
            hour, min = dir_to_process['sdo_time'].split(':')
            hmib, hmiif = sunpro.get_sun_from_date(year+'/'+ month +'/'+ day +'_'+ hour , 'static/uploads')
            #'2021/07/12_07',

            # ajout au json
            jsonReturn['hmib'] = hmib
            jsonReturn['hmiif'] = hmiif


        return jsonify(jsonReturn)
        #return jsonify('static/uploads/'+ file[0] + '_disk.png')



    # si des fichiers existent dans uploads -> nettoyage au lancement de l'application (dossier non accessible en mode applicaiton docker ou apps)
    if os.listdir(UPLOAD_FOLDER) == []:
        print("No files found in the directory.")
    else:
        print("Files found - Cleaning...")
        remove_uploads_files()

    # retourne le template initial
    return render_template('single.html')




@app.route('/valid-path')
def valid_path():
    print('OK PATH')
    return 'ok'



@app.route('/nbserfiles', methods=['POST'])
def count_ser_files():

    if request.method == "POST":
         #value=request.json['data']
        dir_in_progress = request.get_json()
        print(dir_in_progress)
        print(dir_in_progress['folder'])

         # Get the nb of ser files in folder (for check if all thread are finished) => Not very clean TODO: Optimize 
        #print(len(         [        name for name in os.listdir(dir_to_process['folder']) if      (os.path.isfile(os.path.join(dir_to_process['folder'], name))  &    name.endswith(".ser")  )     ]                    ))
        nb_ser_files = len(         [        name for name in os.listdir(dir_in_progress['folder']) if      (os.path.isfile(os.path.join(dir_in_progress['folder'], name))  &    name.endswith(".ser")  )     ]                    )
        print(nb_ser_files)
        return jsonify(nb_ser_files)









@app.route('/massprocess', methods=['GET','POST'])
def mass_process():
    
    if request.method == "POST":

        #value=request.json['data']
        dir_to_process = request.get_json()
        print(dir_to_process)
        print(dir_to_process['folder'])


        # Get the nb of ser files in folder (for check if all thread are finished) => Not very clean TODO: Optimize 
        print(len(         [        name for name in os.listdir(dir_to_process['folder']) if      (os.path.isfile(os.path.join(dir_to_process['folder'], name))  &    name.endswith(".ser")  )     ]                    ))
        nb__multi_files = len(         [        name for name in os.listdir(dir_to_process['folder']) if      (os.path.isfile(os.path.join(dir_to_process['folder'], name))  &    name.endswith(".ser")  )     ]                    )

        # prepare queue for theads
        q = queue.Queue()
        # count files processed
        ser_num = 0
        list_of_ser_filenames = []
        list_of_thread = []


        for filename in os.listdir(dir_to_process['folder']):
            if filename.endswith(".ser") :

                print(os.path.join(dir_to_process['folder'], filename))
                # démarrage d'un nouveau thread pour chaque fichier ser
                x = threading.Thread(target=processthreaded, args=(os.path.join(dir_to_process['folder'], filename),filename))
                #x.start()
                list_of_ser_filenames.append(filename)
                list_of_thread.append(x)

                '''      print(f'NUMB OF CORE : {os.cpu_count()}')

                try:
                    if os.cpu_count() % ser_num : 
                        print(f'Pause in progress : {ser_num}')
                        ser_num += q.get()
                except :
                    print(f'First element not analysed (0 division)')

                #si dernier fichier --> on attend le retour
                if ser_num == nb__multi_files - 1 :
                    ser_num += q.get()
                    print(f'Batch processed. Last item : {ser_num}')

                ser_num+=1

                '''
                
                #x.setDaemon(True)
                x.start()


            else:
                continue

        #main_thread = threading.current_thread()

        for t in list_of_thread:
            #if t is main_thread:
            #    continue
            print('Name 1 : ', t.getName())

            t.join()
            print('joining %s', t.getName(), t.is_alive())


        print('process mass OK')


        # Threads finished -> copy in uploads + prepare return to client

        jsonReturn = []

        for ser_file in list_of_ser_filenames:
            # set file name and copy all files in static for sent to the view and manipulations
            file = ser_file.split('.')
            copyfile(dir_to_process['folder']+ '/' + file[0] + '_disk.png' , 'static/uploads/'+ file[0] + '_disk.png')
            copyfile(dir_to_process['folder']+ '/' + file[0] + '_disk_invert.png' , 'static/uploads/'+ file[0] + '_disk_invert.png')
            copyfile(dir_to_process['folder']+ '/' + file[0] + '.txt' , 'static/uploads/'+ file[0] + '.txt')
            copyfile(dir_to_process['folder']+ '/' + file[0] + '_circle.fits' , 'static/uploads/'+ file[0] + '_circle.fits')
            copyfile(dir_to_process['folder']+ '/' + file[0] + '_corr.fits' , 'static/uploads/'+ file[0] + '_corr.fits')
            copyfile(dir_to_process['folder']+ '/' + file[0] + '_flat.fits' , 'static/uploads/'+ file[0] + '_flat.fits')
            copyfile(dir_to_process['folder']+ '/' + file[0] + '_img.fits' , 'static/uploads/'+ file[0] + '_img.fits')
            copyfile(dir_to_process['folder']+ '/' + file[0] + '_mean.fits' , 'static/uploads/'+ file[0] + '_mean.fits')
            copyfile(dir_to_process['folder']+ '/' + file[0] + '_recon.fits' , 'static/uploads/'+ file[0] + '_recon.fits')




            # creation du fichier zip contenant tous les fichiers
            ## IF NEEDED FOR EACH FILE -----> zip_path = create_zip(dir_to_process['folder'], str(file[0]))


    
            jsonReturn.append({
                'imgsrc' :  file[0]  + '_disk.png',
                'invert_imgsrc' : file[0]  + '_disk_invert.png',
                'imgser' :  dir_to_process['ser']
                
            })


        return jsonify(jsonReturn)

    # si GET -> page web 
    return render_template('mass.html')







@app.route('/upload',methods=['GET', 'POST'])
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
            #filename = secure_filename(file.filename)
            filename = file.filename
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







@app.route('/monitor', methods=['GET', 'POST'])
def monitor():
  
    global observer

    if request.method == "POST":
        data_received = request.get_json()
        path_observed = data_received['folder']


        if get_monitor_state(path_observed)[2] == False :


            global observer

            observer = Observer() 


            event_handler = Handler() 

            #init observer
            #observer = watchdog.observers.Observer() #possibilité de faire un init seulement de Observer() avec les import corrects -->  a changer

            

            #set handler (--> ?),  path to check,
            observer.schedule(event_handler, path=path_observed, recursive=True) 

            #demarrage du thread
            observer.start() 
            #try: 
            #    while True: 
            #        time.sleep(1) 

            #si touche clavier -> fin d'alg o
            #except KeyboardInterrupt: 
            #    observer.stop() 
            #observer.join() 
            state = 'on'
        else :
            observer.stop()
            state = 'off'
        
        return jsonify(state)

    else :
        return render_template('monitor.html')



#@app.route('/getmonitorstate', methods=['GET', 'POST'])
def get_monitor_state(folder_name):

         #value=request.json['data']
        #---dir_in_progress = request.get_json()
        #---print(dir_in_progress)
        #----print(dir_in_progress['folder']
    

         # Get the nb of ser files in folder (for check if all thread are finished) => Not very clean TODO: Optimize 
        #print(len(         [        name for name in os.listdir(dir_to_process['folder']) if      (os.path.isfile(os.path.join(dir_to_process['folder'], name))  &    name.endswith(".ser")  )     ]                    ))
        nb_ser_files = len(         [        name for name in os.listdir(folder_name) if      (os.path.isfile(os.path.join(folder_name, name))  &    name.endswith(".ser")  )     ]                    )

        nb_png_files = len(         [        name for name in os.listdir(folder_name) if      (os.path.isfile(os.path.join(folder_name, name))  &    name.endswith(".png")  )     ]                    )

        try:
            alive = observer.is_alive()
        except:
            alive = False

        print(nb_png_files, nb_ser_files, alive)

        return nb_ser_files, nb_png_files, alive








@app.route('/getmonitorstate', methods=['GET', 'POST'])
def monitoring_state():
    state =''

    if request.method == "POST":
        data = request.get_json()
        state = get_monitor_state(data['folder'])
    elif request.method == "GET":
        state = get_monitor_state('foldertest')


    return jsonify(state)









class Handler(watchdog.events.PatternMatchingEventHandler): 
    def __init__(self): 
        # Set the patterns for PatternMatchingEventHandler 
        watchdog.events.PatternMatchingEventHandler.__init__(self, patterns=['*.ser'],  ignore_patterns=[],
                                                             ignore_directories=True, case_sensitive=True) 



    #------def processthreaded(serfile, filename):
    #----    sol.solex_proc_all(serfile, filename)
        #q.put(1)
    

    def on_created(self, event): 
        print("Watchdog received created event - % s" % event.src_path)
        print("Full Event : ", event) 

        new_file = event.src_path.split("/")
        file = new_file[-1:][0]
        file2 = f'/{new_file[-2:][0]}'

        # Launch new thread with processing ser (/!\ this thread can't be stopped by the user at this time)
        x = threading.Thread(target=processthreaded, args=(os.path.join(file2, file), file))
        x.start()
       
        #log
        print(new_file[-1:][0])

        
        # Event is created, you can process it now 
  
    
    def on_modified(self, event): 


        new_file = event.src_path.split("/")
        file = new_file[-1:][0]
        #file2 = f'/{new_file[-2:][0]}'
        file2 = new_file[-2:][0] #dev version

        # Launch new thread with processing ser (/!\ this thread can't be stopped by the user at this time)
        x = threading.Thread(target=processthreaded, args=(os.path.join(file2, file), file))
        x.start()


        print("Watchdog received modified event - % s" % event.src_path) 
        # Event is modified, you can process it now 











if __name__== "__main__":
    app.run(debug=False, threaded=True)
    #app.run (host='192.168.1.27')


