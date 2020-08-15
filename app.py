from flask import Flask,url_for,redirect,render_template,request
import pickle
from utility import *
import smtplib

######################################  LOAD RESOURCES  #########################################
print('[STATUS] Loading data')
data = pickle.load(open('resources/Mediserve-ML-data.pickle','rb'))
print('[STATUS] Loading models')
models = pickle.load(open('resources/Mediserve-ML-models.pickle','rb'))
print('[STATUS] Loading encoders')
encoders = pickle.load(open('resources/Mediserve-ML-encoders.pickle','rb'))
print('[STATUS] Loading severity data')
sevr_dict = pickle.load(open('resources/Mediserve-ML-severity-dict.pickle','rb'))
######################################  LOAD RESOURCES  #########################################

#########################   GLOBAL VARIABLES ###########################################
selected_symptoms = ['not_needed' for x in range(17)]
server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
#########################   GLOBAL VARIABLES ###########################################


########################################### INITIALIZATIONS ########################################
group_data = {}
group_data['sym_name'] = list()
group_data['sym_options'] = list()
group_data['disp_sym'] = ['sym_'+str(x) for x in range(1,18)]
group_data['title'] = "Mediserve"

out_data = {}
mail_data = {}

for j in range(1,18):
    group_data['sym_name'].append('Select Symptom ' + str(j))
for j in range(1,18):
    group_data['sym_options'].append(sorted(set(data[1]['Symptom_'+str(j)])))

final_model = models[2][1] # DTREE
########################################### INITIALIZATIONS ########################################


########################################### WEBPAGE LOGIC ##########################################
app = Flask(__name__)

app.add_template_global(transform_string,name = 'transform_string')
app.add_template_global(str,name = 'str')

@app.route('/',methods = ['POST','GET'])
def index():
    global selected_symptoms,final_model,out_data
    if request.method == 'POST':
        for n in range(17):
            selected_symptoms[n] = inverse_transform_string(request.form['sym_'+str(n+1)])
        arr = encode_data(selected_symptoms,encoders)
        out_data['encoded'] = final_model.predict(arr)
        out_data['text'] = decode_output(out_data['encoded'],encoders)
        return redirect(url_for('predict'))
    else:
        return render_template('index.html',group_data = group_data)

@app.route('/predict',methods = ['POST','GET'])
def predict():
    global out_data,mail_data
    get_description(out_data,data[3])
    get_precautions(out_data,data[4])
    out_data['severity'] = get_severity(sevr_dict,selected_symptoms)
    if request.method == 'GET':
        print('Here')
        print(request.form)
        form_get_response(mail_data,request,out_data)
        print(mail_data)
        try:
            send_mail(mail_data,server)
            print('success')
        except Exception as e:
            print('Error in sending')
            print(e)
    return render_template('contact.html',out_data = out_data)

@app.route('/recorded')
def recorded():
    return '<h1>This is the final submissions recorded page</h1>'

@app.route('/about_us',methods = ['POST','GET'])
def about_us():
    return render_template('about_us.html')

########################################### WEBPAGE LOGIC ##########################################
if __name__ == '__main__':
    app.run(debug = True)
