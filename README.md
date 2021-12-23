# welcometo
A system for running the shared part of a game of Welcome To in a browser

Installation instructions I used on Ubuntu on Windows
1. Install and setup Ubuntu on Windows: https://ubuntu.com/tutorials/ubuntu-on-windows
2. Install python3 and some other packages: sudo apt-get install python3 python3-venv unzip
3. Download this git repo: wget https://github.com/avandever/welcometo/archive/refs/heads/main.zip
4. Unzip the repo: unzip main.zip
5. cd welcometo-main
6. Set up the virtual environment: python3 -m venv venv
7. Activate the virtual environment: source venv/bin/activate
8. Install flask: pip3 install flask
9. Set the flask app: export FLASK_APP=welcometo
10. flask run
