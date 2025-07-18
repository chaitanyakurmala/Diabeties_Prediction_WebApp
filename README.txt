Run theis script in workbench
CREATE DATABASE IF NOT EXISTS diabetes_prediction;

USE diabetes_prediction;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(200) UNIQUE NOT NULL,
    password VARCHAR(200) NOT NULL,
    email VARCHAR(200) NOT NULL,
    mobile VARCHAR(15) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

//Update db username andpassword if req in app.py


install python
install pip
//Run these cmds
run this cmd for db : pip install flask flask-mysqldb mysql-connector-python scikit-learn pandas
