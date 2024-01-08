# Inventory Management System
My project involves the design and development of a robust Inventory Management Application using the power and flexibility of Python programming. This application aims to streamline and enhance the efficiency of inventory tracking and management processes for organizations and businesses of all scales.
By leveraging Python's versatility and extensive libraries, this Inventory Management Application aims to optimize inventory control processes, reduce operational costs, and improve overall business efficiency.

# Getting started

- set your `.env` file at the root of the repository
```bash
JWT_SECRET_KEY = "ENTER YOUR VALUE HERE"
JWT_ALGORITHM = "ENTER YOUR VALUE HERE"
JWT_TIMEOUT = "ENTER YOUR VALUE"
DB_URI = "ENTER VALUE HERE"
```

- Create your virtual environment
```
python3 -m venv venv
```
> make sureyou have `python3-venv` installed, if you don't then run this command
```
sudo apt-get install -y python3-venv
```

- Activate the virtual environment and install packages to virtual environment
```
source venv/bin/activate
pip install -r requirements.txt
```

- run the file `start.sh` or you can use python3 to run the `main.py` file
__you can also use `supervisor`__ to make sure the application is always running, however this is for practice purpose so we're not using supervisor here.

> if you expericence compatibility issue between the version of pyOpenSSL library and the system's installed OpenSSL libraries. when you try to run the application, use the below instructions to resolve the issue
```
sudo apt-get update
sudo apt-get upgraade
sudo pip3 install pyopenssl --force-reinstall
```

- Run the file `main.py` or the `start.sh`
```bash
# running the main.py file
python3 main.py

# running the start.sh
./start.sh
```
