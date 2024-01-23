### How to set up the application:

Step 1: Install Python of 3.11 version: https://www.python.org/downloads/
 
***Important to use lower version of Python, as some dash components haven't migrated to new Python version yet.***

Step 2: Set up default env variables:
* for Windows:
  * `set PYTHONPATH=%PYTHONPATH%;.`
  * `set BASE_EXOCODE_PATH=path\to\repository`
  * `set JUPYTER_NOTEBOOK_PORT=9999`
  * `set DASH_APP_PORT=1111`
* for Unix 
  * `export PYTHONPATH="${PYTHONPATH}:."`
  * `export BASE_EXOCODE_PATH="path\to\repository"`
  * `export JUPYTER_NOTEBOOK_PORT="9999"`
  * `export DASH_APP_PORT="1111"`

***Please change path\to\repository to the actual path***

Step 3: Create a Virtual Environment in the repo's root:
`path\to\python.exe -m venv myvenv`

Step 4: Activate Virtual Environment: `%BASE_EXOCODE_PATH%\myvenv\Scripts\activate`

Step 5: Install required libraries: `pip install -r requirements.txt`

Step 6: Create a database: `python %BASE_EXOCODE_PATH%\data_access\db_creation.py`

Step 7: Run Jupyter Notebook server in minimized mode: `start /min jupyter notebook --port=%JUPYTER_NOTEBOOK_PORT%`

Step 8: Run Dash App:
`python %BASE_EXOCODE_PATH%\ui\app.py`

Step 9: Open http://localhost:1111/ and start exploring the stars