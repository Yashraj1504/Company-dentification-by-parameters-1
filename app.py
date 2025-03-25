from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Load company data from Excel file
def load_data():
    df = pd.read_excel("static/company_data.xlsx")
    return df

@app.route('/', methods=['GET', 'POST'])
def index():
    company_details = None
    not_found = False
    df = load_data()
    
    if request.method == 'POST':
        industry = request.form.get("industry", "").strip()
        location = request.form.get("location", "").strip()
        founded_year = request.form.get("founded_year", "").strip()
        
        # df = load_data()
        
        # Convert founded_year to int if it's numeric
        if founded_year.isdigit():
            founded_year = int(founded_year)
        
        # Searching for company details with multiple filters
        result = df[(df["Industry"].str.lower() == industry.lower()) & 
                    (df["Headquarters Location"].str.lower() == location.lower()) & 
                    (df["Founded Year"] == founded_year)]
        
        if not result.empty:
            company_details = result.to_dict(orient='records')
        else:
            not_found = True

    return render_template('index2.html', company_details=company_details, not_found=not_found, industries=df["Industry"], locations=df["Headquarters Location"], founded_years=df["Founded Year"])

if __name__ == '__main__':
    app.run(debug=True)
