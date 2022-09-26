# EC463 SW Mini-Project

### Project Structure

---

<pre>
.
├─── .gitignore
├─── .gitmodules
├─── botometerTest.py
├─── firebaseTest.py
├─── get_followers.py
├─── naturalLanguageTest.py
├─── README.md --> This file
├─── requirements.txt
├─── rev_1.py
├─── test.py
│
└─── templates
     └─── index.html
</pre>

### Install Requirements

---

*Tested on Python 3.10.2. Ensure Python is added to PATH*

python -m pip install -r requirements.txt

*or*

pip install -r requirements.txt

### Setup Environment

---

Our demo requires you to have separate files that store the Rapid API key for Botometer (.key file), Twitter v2 api keys (.env file) for Twarc, Firebase admin credentials (.json file), and Google Cloud credentials (.json file). A tutorial to set up the Botometer API and its Rapid API key can be found in the [github repo](https://github.com/IUNetSci/botometer-python/blob/master/README.md). The Twitter v2 api keys can be generated from your Twitter developer account. Copy and paste them into a text file like so:

<pre>
BEARER_TOKEN=[YOUR BEARER TOKEN] 
CONSUMER_KEY=[YOUR CONSUMER KEY] 
CONSUMER_SECRET=[YOUR CONSUMER SECRET] 
ACCESS_TOKEN=[YOUR ACCESS TOKEN] 
ACCESS_TOKEN_SECRET=[YOUR ACCESS TOKEN SECRET]
</pre>

<br>

The Firebase credentials can be generated as a .json after creating a Firebase project. Similarly, you can generate Google Cloud credentials by signing up for a Google Cloud [account](https://cloud.google.com/natural-language) and generating credentials as a .json file.

*Note: you need at least an "elevated" twitter developer account in order to run this demo*

### How to Run

---

1. Run the Flask server with Python
python rev_1.py -p [HOST PORT] -i [HOST IP] -fb [PATH TO FIREBASE ADMIN JSON] -tw [PATH TO TWITTER .ENV] -rk [PATH TO RAPID API .KEY] -go [PATH TO GOOGLE CLOUD JSON]

2. Go to a http://[HOST IP]:[HOST PORT] in a browser

3. In the textbox located in the top left corner, enter a username and press the return key or the 'user' button.

4. If the query is sucessful the user button will become enabled again and the textbox below the user submission will say 'done'. Check your Firebase account to view the written data. If the query is unsuccessful, please reload the page and enter a differen username.

