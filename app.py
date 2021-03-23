import flask, os, sqlite3
from flask import render_template, request
from flask import send_from_directory
from werkzeug.utils import secure_filename

if not os.path.isfile('db.sqlite3'): #if no such database exists
    db = sqlite3.connect('db.sqlite3')
    db.execute('CREATE TABLE photos(photo TEXT)')
    db.commit()
    db.close()
    
app = flask.Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST' and \
        request.files and 'photo' in request.files:
        print(request.files)     #a dictionary of file upload names & associated FileStorage objects
        # Save file
        photo = request.files['photo'] #key of dictionary is 'photo'
        print(photo)             #get value of key:'photo', which is the FileStorage object
        filename = secure_filename(photo.filename)
        print(filename)          #replaces all whitespaces of filename with underscores
##        if filename.split('.')[-1].lower() != 'jpeg' and filename.split('.')[-1].lower() != 'jpg' \
##        and filename.split('.')[-1].lower() != 'png' and filename.split('.')[-1].lower() != 'gif':
##            print("goodbye")
##            return render_template('form_with_file_upload.html')
        path = os.path.join('uploads', filename)
        print(path)              #form the path for the storage of photo
        photo.save(path)         #save the file in path
        # Add filename to database
        db = sqlite3.connect('db.sqlite3')
        db.execute('INSERT INTO photos(photo) VALUES(?)',
            (filename,))  #insert filename into table photo in database
        db.commit()
        db.close()
    return render_template('form_with_file_upload.html')

@app.route('/view')
def view():
    db = sqlite3.connect('db.sqlite3')
    cur = db.execute('SELECT photo FROM photos')
    photos = []     #read the filename from table photo in database
    for row in cur:
        photos.append(row[0])
    db.close()
    print(photos) #list of filenames of photos
    return render_template('view_file_uploads.html',
        photos=photos)

@app.route('/photos/<filename>')
def get_file(filename):
    #send file from upload directory with associated filename
    return send_from_directory('uploads', filename)


if __name__ == '__main__':
    app.run()
