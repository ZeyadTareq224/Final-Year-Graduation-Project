from pathlib import Path
import os
import pandas as pd
from flask import Flask, request, jsonify

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = os.path.join(BASE_DIR, 'BCXGBoost.pickle')
MODEL2_PATH = os.path.join(BASE_DIR, 'LRM.pickle')
app = Flask(__name__)



@app.route('/predict1',methods=['POST'])
def index():
	body = request.get_json()
	radius_mean = float(body.get('radius_mean', None))
	texture_mean = float(body.get('texture_mean', None))
	perimeter_mean = float(body.get('perimeter_mean', None))
	area_mean = float(body.get('area_mean', None))
	smoothness_mean = float(body.get('smoothness_mean', None))
	compactness_mean = float(body.get('compactness_mean', None))
	concavity_mean = float(body.get('concavity_mean', None))
	concave_points_mean = float(body.get('concave_points_mean', None))
	symmetry_mean = float(body.get('symmetry_mean', None))
	fractal_dimension_mean = float(body.get('fractal_dimension_mean', None))

	model = pd.read_pickle(MODEL_PATH)
	x_new = [[
		radius_mean,
		texture_mean,
		perimeter_mean,
		area_mean,
		smoothness_mean,
		compactness_mean,
		concavity_mean,
		concave_points_mean,
		symmetry_mean,
		fractal_dimension_mean
		]]
	x_new_columns = [
		'radius_mean',
		'texture_mean',
		'perimeter_mean',
		'area_mean',
		'smoothness_mean',
		'compactness_mean',
		'concavity_mean',
		'concave points_mean',
		'symmetry_mean',
		'fractal_dimension_mean'
		]	
	x_new_final = pd.DataFrame(x_new, columns=x_new_columns)	

	result = model[4].predict(x_new_final)

	classification = int(result[0])
	
	response = {
		'classification': classification,
	}
	return jsonify(response)



@app.route('/predict2',methods=['POST'])
def friendlyModel():
	body = request.get_json()

	Clump_Thickness = int(body.get('Clump_Thickness', None))
	Uniformity_of_Cell_Size = int(body.get('Uniformity_of_Cell_Size', None))
	Uniformity_of_Cell_Shape = int(body.get('Uniformity_of_Cell_Shape', None))
	Marginal_Adhesion = int(body.get('Marginal_Adhesion', None))
	Single_Epithelial_Cell_Size = int(body.get('Single_Epithelial_Cell_Size', None))
	Bare_Nuclei = int(body.get('Bare_Nuclei', None))
	Bland_Chromatin = int(body.get('Bland_Chromatin', None))
	Normal_Nucleoli = int(body.get('Normal_Nucleoli', None))
	Mitoses = int(body.get('Mitoses', None))

	
	lrm = pd.read_pickle(MODEL2_PATH)
	
	x_new = [[
		Clump_Thickness,
		Uniformity_of_Cell_Size,
		Uniformity_of_Cell_Shape,
		Marginal_Adhesion,
		Single_Epithelial_Cell_Size,
		Bare_Nuclei,
		Bland_Chromatin,
		Normal_Nucleoli,
		Mitoses
		]]

	x_new_columns = [
		'Clump Thickness',
		'Uniformity of Cell Size',
		'Uniformity of Cell Shape',
	    'Marginal Adhesion', 
	    'Single Epithelial Cell Size', 
	    'Bare Nuclei', 
	    'Bland Chromatin',
	    'Normal Nucleoli', 
	    'Mitoses'
    ]	
	x_new_final = pd.DataFrame(x_new, columns=x_new_columns)

	result = lrm.predict(x_new_final)[0]
	print(result)
	
	response = {
		'classification': int(result),
	}
	return jsonify(response)
	