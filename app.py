from flask import Flask, render_template, request, send_file
from geopy.geocoders import ArcGIS
import pandas, datetime



app=Flask(__name__)

# app.config['UPLOAD_FOLDER']='/uploads'
# app.config['MAX_CONTENT_PATH']=10000000 # 10MB in bytes


@app.route("/")
def index():
    return render_template("index.html")

@app.route('/success-table', methods=['POST']) #By default, the Flask route responds to GET requests.However, you can change this preference by providing method parameters for the route () decorator.
def success_table():
    global filename #to access in both funkcions 
    if request.method=="POST":
        file=request.files['file']
        try:
            df=pandas.read_csv(file)
            gc=ArcGIS(scheme='https')
            df["coordinates"]=df["Address"].apply(gc.geocode)
            df["Latitude"] = df["coordinates"].apply(lambda x: x.latitude if x != None else None)
            df["Longitude"] = df["coordinates"].apply(lambda x: x.longitude if x != None else None)
            df=df.drop("coordinates",1)
            filename=datetime.datetime.now().strftime("uploads/%Y-%m-%d-%H-%M-%S-%f"+".csv")
            df.to_csv(filename, index=None)
            return render_template("index.html", text=df.to_html(), btn="download.html")
        except Exception as e:
            return render_template("index.html", text=str(e))
@app.route("/download-file/")
def download():
    return send_file(filename, attachment_filename='yourfile.csv', as_attachment=True)

if __name__=='__main__':
    app.debug= True
    app.run()