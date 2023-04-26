# BCDA - Breast Cancer Digital Assistant
## BCDA is a project aimed at helping patients and healthcare providers manage breast cancer diagnosis and treatment. The project is divided into four modules:

#### Clinic Management System: This module allows patients to book appointments with doctors who have brought their clinics online on our system. It is built using Django.

#### Machine Learning Tumor Prediction: This module uses machine learning to predict the type of breast cancer tumor using FNA analysis. It is built using Flask to create the API.

#### Drug Guide: This module provides patients with information about all available medications for breast cancer, including their requirements and side effects. The information is scraped from the National Cancer Institute using Beautiful Soup.

#### Consultations: This module provides a platform for patients and doctors to hold conversations and consultations. It is built using Django.

## Requirements
##### Python 3.7 or higher
##### Django 3.0 or higher
##### Flask 1.1.1 or higher
##### Beautiful Soup 4.9.3 or higher

## Installation
##### Clone the repository:
`git clone https://github.com/ZeyadTareq224/Final-Year-Graduation-Project.git`
`cd Final-Year-Graduation-Project/main project/src`

##### Install the requirements:
`pip install -r requirements.txt`

##### Run the migrations:
`python manage.py migrate`

##### Start the development server:
`python manage.py runserver`

##### Visit http://localhost:8000 in your browser to access the application.


## Contributing

If you'd like to contribute to BCDA, please fork the repository and create a pull request. We welcome contributions in the form of bug fixes, new features, and documentation improvements.

## License
BCDA is licensed under the MIT License. See LICENSE for more information.
