from flask import Flask, request, jsonify
import numpy as np
import pandas as pd
import shapefile as shp
import matplotlib.pyplot as plt
import seaborn as sns
app = Flask(__name__)
sns.set(context='notebook', style='whitegrid', palette='pastel', font='sans-serif', font_scale=1, color_codes=True, rc=None)
sns.mpl.rc('figure', figsize=(10,6))
shp_path = '/home/lucky21/Music/work/map/doc2/District_Boundary.shp'
#reading the shape file by using reader function of the shape lib
sf = shp.Reader(shp_path)
sf = shp.Reader(shp_path)
def read_shapefile(sf):
    #fetching the headings from the shape file
    fields = [x[0] for x in sf.fields][1:]
#fetching the records from the shape file
    records = [list(i) for i in sf.records()]
    shps = [s.points for s in sf.shapes()]
#converting shapefile data into pandas dataframe
    df = pd.DataFrame(columns=fields, data=records)
#assigning the coordinates
    df = df.assign(coords=shps)
    return df
df=read_shapefile(sf)
def plot_shape(id, s=None):
    plt.figure()
    #plotting the graphical axes where map ploting will be done
    ax = plt.axes()
    ax.set_aspect('equal')
#storing the id number to be worked upon
    shape_ex = sf.shape(id)
#NP.ZERO initializes an array of rows and column with 0 in place of each elements 
    #an array will be generated where number of rows will be(len(shape_ex,point))and number of columns will be 1 and stored into the variable
    x_lon = np.zeros((len(shape_ex.points),1))
#an array will be generated where number of rows will be(len(shape_ex,point))and number of columns will be 1 and stored into the variable
    y_lat = np.zeros((len(shape_ex.points),1))
    for ip in range(len(shape_ex.points)):
        x_lon[ip] = shape_ex.points[ip][0]
        y_lat[ip] = shape_ex.points[ip][1]
#plotting using the derived coordinated stored in array created by numpy
    plt.plot(x_lon,y_lat) 
    x0 = np.mean(x_lon)
    y0 = np.mean(y_lat)
    plt.text(x0, y0, s, fontsize=10)
# use bbox (bounding box) to set plot limits
    plt.xlim(shape_ex.bbox[0],shape_ex.bbox[2])
    return x0, y0

@app.route('/api/', methods=["POST"])
def main_interface():
    response = request.get_json()
    DIST_NAME = 'JAIPUR'
    com_id = df[df.DIST_NAME == DIST_NAME].index.get_values()[0]
    plot_shape(com_id, DIST_NAME)
    print(com_id)
    l=[]
    for i in range (0,32): 
        r=df.iloc[i,5]
        l.append(r)
  
    return jsonify(l)
@app.after_request
def add_headers(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    return response  


if __name__ == '__main__':
    app.run(debug=True)
