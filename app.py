import nltk
nltk.download('stopwords')


from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from Resume_parser import extract_skills, compare_skills, send_email, connect_to_smtp_server, extract_education, extract_certificates

app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template('home.html')


@app.route('/apply_job')
def applyjob():
    return render_template("apply_job.html")


@app.route('/aboutUs')
def aboutUs():
    return render_template("aboutUs.html")


@app.route('/fill_form')
def fillform():
    return render_template("form.html")


@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        appliedJob = request.form['job']  # get selected job from the form
        nameGiven = request.form['name']  # get name from the form
        emailGiven = request.form['email']  # get email from the form
        f = request.files['file']  # taking reume file from submitted form
        f.save(secure_filename(f.filename))
        name, email, skills = extract_skills(f.filename)
        skills_matched = compare_skills(appliedJob, skills)
        # education = extract_education(f.filename)
        # certificate = extract_certificates(f.filename)
        # print(education)
        # print(certificate)
        print(email)
        print(skills)
        print(skills_matched)
        numberOf_skills_matched=len(skills_matched)
        is_rejected = True
        if len(skills_matched) >= 2:
            print("he is eligible")
            is_rejected = False
            s=connect_to_smtp_server()
            send_email(email, name, is_rejected, appliedJob,s)
            return render_template('success.html', name=nameGiven, email=emailGiven, skills=skills_matched,count=numberOf_skills_matched)
        else:
            is_rejected = True
            print("Sorry, we can't process your candidature")
            s=connect_to_smtp_server()
            send_email(email, name, is_rejected, appliedJob,s)
            return render_template('success.html', name=nameGiven, email=emailGiven, skills=skills_matched,count=numberOf_skills_matched)
    else:
        return render_template('home.html')


@app.route('/home')
def homepage2():
    return render_template('home.html')


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=80)
