# HIS
## Table of Contents

* [About the Project](#about-the-project)
* [Toolbox](#toolbox)
* [Setting Up the Environment](#setting-up-the-environment)
* [Our Team](#our-team)
* [About](#about)

## About The Project
PlaceHolder

## Toolbox

* HTML
* CSS
* JavaScript
* Bootstrap
* Flask
    * Flask WTF
    * Flask SQLAlchemy
    * Flask Mail
    * Flask Bcrypt
    * Flask LoginManger

## Setting Up the Environment
1. Clone the repo
    - HTTPS
        ```sh
        git clone https://github.com/RamadanIbrahem98/HIS.git
        ```
    - SSH
        ```sh
        git clone git@github.com:RamadanIbrahem98/HIS.git
        ```
1. Create a Virtual Environment (Optional)
    ```sh
    python -m venv .HIS
    ```
1. Activate the virtual environment 
    - using CMD
        ```sh
        .\.HIS\Scripts\activate
        ```
    - using PowerShell
        ```sh
        .\.HIS\Scripts\Activate.ps1
        ```

1. Install the requirements and dependancies
    ```sh
    pip install -r requirements.txt
    ```
1. Set Up the Environment Variables in the **HIS/main/config.py** file with your own.
    * SECRET_KEY: Is a random secret key used to log sessions.
    * SQLALCHEMY_DATABASE_URI: Is the URI of your database
    * MAIL_USERNAME: Your gmail account.
    * MAIL_PASSWORD: This is an app password assigend from google. you can get one from [Here!](https://security.google.com/settings/security/apppasswords)

1. Run the application
    ```sh
    python run.py
    ```
1. View the application on localhost
    ```
    http://localhost:5000/
    ```

## Our Team

- Ramadan Ibrahem
- Muhammad Seyam
- Muhammad Abd-ElAziz
- Moamen Gamal
- Haithem Emad
- Qurban Ali

## About
This project is a part of the SBE306 course (Computer Systems 3) in the [Systems and Biomedical Engineering Department - Cairo University](http://bmes.cufe.edu.eg/)\
Dr.Ahmed Kandil\
TA. Ayman Anwar
