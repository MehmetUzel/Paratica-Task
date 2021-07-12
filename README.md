# Paratica Task
 Paratica Task for job interview

Installation

first navigate to the path that includes requirements.txt file

and run this command " pip install -r requirements.txt "

Change values in line 11 with your password port and db name
<br>
postgresql://postgres:{password}@localhost:{port}/{databasename}

after changing DB_URI with your local values type python on the same path

Enter this codes with given order

from main import db
<br>
db.create_all()
<br>
exit()
<br>

this creates our table
<br>
after creating tables use sampleData.txt to populate table (via Query)

Notes: <br>
I think timestamp should be created based on database function "now". <br>
username and surname should be different columns

