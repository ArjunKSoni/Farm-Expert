from flask import Flask,render_template,flash,redirect,request
app = Flask(__name__)
import soil
import search_crop as sc
import crop_json as cj
import crop
model_soi,ind,df1=soil.model()
model_cr,inde2=crop.model()
model_soil=model_soi
index=ind
df=df1
model_crop=model_cr
index2=inde2

@app.route('/', methods=['GET', 'POST'])
def mainpage():
    return render_template('Mainpage.html')

@app.route('/nav', methods=['POST'])
def nav():
    crop=request.form['search']
    p=sc.search(crop)
    if p==-1:
        return render_template('not_found.html')
    k=df[df['label']==p[0]]['Sno'].values
    crop_detail=[]
    crop_img=[]
    crop_name=[]
    pi=[]
    for i in range(4):
        crop_detail.append(cj.find(p[i]))
        crop_img.append(crop_detail[i]["img"])
        crop_name.append(crop_detail[i]["name"].upper())
    crop_desc=crop_detail[0]["desc"]
    pi=df[df['Sno']==k[0]].values[0]
    return render_template('crop.html',crop=pi,ci=crop_img,cn=crop_name,cd=crop_desc)


@app.route('/get_soil_info', methods=['GET', 'POST'])
def get_soil_info():
    if request.method == 'POST':
        N=int(request.form['N'])
        P=int(request.form['P'])
        K=int(request.form['K'])
        temperature=int(request.form['temperature'])
        humidity=int(request.form['humidity'])
        ph=int(request.form['ph'])
        rainfall=int(request.form['rainfall'])
        label=(request.form['label'])
        val=[N,P,K,temperature,humidity,ph,rainfall]
        p=sc.search(label)
        if p==-1:
            return render_template('not_found.html')
        global inde
        for i in index:
            if(i[0]==p[0]):
                val.append(i[1])
                break
        predicted=soil.predict(val,model_soil,index)

        
        crop_detail=[]
        crop_img=[]
        crop_name=[]
        for i in range(4):
            crop_detail.append(cj.find(p[i]))
            crop_img.append(crop_detail[i]["img"])
            crop_name.append(crop_detail[i]["name"].upper())
        crop_desc=crop_detail[0]["desc"]

        return render_template('crop.html',crop=predicted,ci=crop_img,cn=crop_name,cd=crop_desc)
    else:
        return render_template("form.html")

@app.route('/get_crop_info', methods=['GET', 'POST'])
def get_crop_info():
    if request.method == 'POST':
        N=int(request.form['N'])
        P=int(request.form['P'])
        K=int(request.form['K'])
        temperature=int(request.form['temperature'])
        humidity=int(request.form['humidity'])
        ph=int(request.form['ph'])
        rainfall=int(request.form['rainfall'])
        val=[N,P,K,temperature,humidity,ph,rainfall]
        predicted=crop.predict(val,model_crop,index2)
        # crops=[]
        p=sc.search(predicted[8])
        if p==-1:
            return render_template('not_found.html')
        crop_detail=[]
        crop_img=[]
        crop_name=[]
        for i in range(4):
            crop_detail.append(cj.find(p[i]))
            crop_img.append(crop_detail[i]["img"])
            crop_name.append(crop_detail[i]["name"].upper())
        crop_desc=crop_detail[0]["desc"]

        return render_template('crop.html',crop=predicted,ci=crop_img,cn=crop_name,cd=crop_desc)
    else:
        return render_template("form2.html")


app.run(debug=True)