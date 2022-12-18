from flask import Flask, render_template, request
import pickle
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)
file = open('random_forest_model.pkl', 'rb')
rf_random = pickle.load(file)

@app.route('/',methods=['GET'])
def Home():
    return render_template('index.html')


standard_to = StandardScaler()
@app.route("/predict", methods=['POST'])
def predict():
    RK = 0
    if request.method == 'POST':
        square_ft = float(request.form['square_ft'])
        BHK_RK= int(request.form['BHK_RK'])
        LONGITUDE= float(request.form['LONGITUDE'])
        LATITUDE= float(request.form['LATITUDE'])
        

        BHK = request.form['BHK']
        if(BHK=='BHK TYPE'):
                 BHK=1
                 RK=0
        else:
                 RK=1
                 BHK=0
            
        RESALE = request.form['RESALE']
        if(RESALE=='YES'):
            RESALE=1
        else:
            RESALE=0
            
            
        prediction=rf_random.predict([[BHK_RK,square_ft,RESALE,BHK,RK,LONGITUDE,LATITUDE]])
        output=round(prediction[0],2)
        if output<0:
            return render_template('index.html',PREDICTION_VALUES="Sorry you cannot sell this house")
        else:
            return render_template('index.html',PREDICTION_VALUES="Your house estimate price is  ₹ {} lakhs".format(output))
    else:
        return render_template('index.html')

if __name__=="__main__":
    app.run(debug=True)