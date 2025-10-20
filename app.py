from flask import Flask, request, render_template
import pickle
import numpy as np

app = Flask(__name__)
def prediction(list):
    filename = 'model/predictor.pickle'
    with open(filename, 'rb') as file:
        model = pickle.load(file)
    pred_vlaue = model.predict([list])
    return pred_vlaue


@app.route('/', methods=['GET', 'POST'])
def index():
    pred = 0
    if request.method == 'POST':
        # Get form data safely
        ram = request.form.get('ram')
        weight = request.form.get('weight')
        touchscreen = 1 if request.form.get('touchscreen') == 'on' else 0
        ips = 1 if request.form.get('ips') == 'on' else 0
        cpu = request.form.get('cpuname').lower()
        gpu = request.form.get('gpuname').lower()
        company = request.form.get('company').lower()
        os = request.form.get('opsys').lower()
        laptop_type = request.form.get('typename').lower()

        print(f"RAM: {ram}, Weight: {weight}, Touchscreen: {touchscreen}, IPS: {ips}, "
              f"CPU: {cpu}, GPU: {gpu}, Company: {company}, OS: {os}, Type: {laptop_type}")

        # Start building feature list
        feature_list = []

        # Add numeric features
        feature_list.append(int(ram))
        feature_list.append(float(weight))
        feature_list.append(touchscreen)
        feature_list.append(ips)

        # Define categories
        company_list = ['acer', 'apple', 'asus', 'dell', 'hp', 'lenovo', 'msi', 'other', 'toshiba']
        typename_list = ['2in1convertible', 'gaming', 'netbook', 'notebook', 'ultrabook', 'workstation']
        opsys_list = ['linux', 'mac', 'other', 'windows', 'chrome']
        cpu_list = ['amd', 'intelcorei3', 'intelcorei5', 'intelcorei7', 'other']
        gpu_list = ['amd', 'intel', 'nvidia']

        # One-hot encoding for categorical features
        for item in company_list:
            feature_list.append(1 if item == company else 0)

        for item in typename_list:
            feature_list.append(1 if item == laptop_type else 0)

        for item in opsys_list:
            feature_list.append(1 if item == os else 0)

        for item in cpu_list:
            feature_list.append(1 if item == cpu else 0)

        for item in gpu_list:
            feature_list.append(1 if item == gpu else 0)

        print(" Feature List:", feature_list)

        # Example: If you have a model uncomment below
        # prediction = model.predict([feature_list])
        # output = round(prediction[0], 2)
        # return render_template('index.html', prediction_text=f'Estimated Price: ${output}')

        pred = prediction(feature_list)*302.77
        pred = np.round(pred, 2)


    return render_template('index.html', pred = pred)


if __name__ == '__main__':
    app.run(debug=True)
