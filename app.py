from flask import Flask, render_template, request, redirect, url_for, flash
import plotly.graph_objects as go
import pandas as pd
import io
import base64

app = Flask(__name__)

app.secret_key = 'CS-210'

@app.route("/")
def home():
    alert_message = "This website is just an introduction for the team and project. If you want to analyze the all datasets, download and run XAMPP, start Apache and MySQL services, go to phpmyadmin page for MySQL, and then visit: 'https://github.com/kutluhaan/Analyze-Turkey.git' to download the files. Run all ipynb files and finally run 'page-control.py'."
    return render_template("index.html", alert_message=alert_message)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/data_analysis", methods =["GET", "POST"])
def analysis():
    data = ""
    header= ""
    description = ""
    plot_div = None
    if request.method == "POST":
        topic = request.form.get('topic').lower().replace(' ', '_')
        sub_topic = request.form.get('sub-topic').lower().replace(' ', '_')
        year = request.form.get('year').lower()
        
        df = None
        if topic != 'poorness_based_on_education':
            df = pd.read_excel(f"db/{topic}/{sub_topic}_{year}.xlsx")
        else:
            df = pd.read_excel(f"db/{topic}/{sub_topic}.xlsx")
            df.index = df['Unnamed: 0']
            df = df.drop("Unnamed: 0", axis=1)
            # Remove the first row
            df = df.drop(df.index[0])
        header = f"{topic.capitalize()} - {sub_topic.capitalize().replace('_', ' ')}"
        
        if request.form.get('visualize'):
            # Create 3D plot
            fig = go.Figure(data=[go.Surface(z=df.values, x=df.columns, y=df.iloc[:, 0].values)])
            fig.update_layout(title='3D Plot', scene=dict( aspectmode='cube', camera=dict(eye=dict(x=1.5, y=1.5, z=1.5))), width=1000, height=800)
            plot_div = fig.to_html(full_html=False)
        
        if request.form.get('describe'):
            description = df.describe()
            description = description.to_html()
        df = df.to_html()
        data = df
        
        flash("Success", "success")
    return render_template("data_analysis.html", data=data, data_description=description, plot_div=plot_div, header=header)

@app.route("/contact", methods =["GET", "POST"])
def contact():
    if request.method == "POST":
        full_name = request.form.get('fullname')
        email = request.form.get('email')
        message  = request.form.get('message')
        print(f"Your name is {str(full_name)} {str(message)} {str(email)}")
        flash("Success", "success")
        name = "{0} {1}".format(full_name)
        return redirect(url_for("home"))
    else:
        return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True)
