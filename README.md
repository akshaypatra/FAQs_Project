# FAQ project details

## 1. Setting up Django project

### Creating Django project and and starting an app

- django-admin startproject faq_project
- cd faq_project
- django-admin startapp faqs

### Installing all dependencies

- pip3 install django djangorestframework django-ckeditor-5 django-redis googletrans==4.0.0-rc1


## 2. Models Overview
The FAQ model is designed to store frequently asked questions along with their translated versions in multiple languages. It supports rich text formatting for answers using CKEditor 5.

### Key Features

- *UUID as Primary Key*:
    Each FAQ entry has a unique id generated using uuid.uuid4, ensuring globally unique identifiers.

- *Multilingual Support*:
    - The model includes a language field with predefined choices from various global languages.
    - Automatic translation for question_hi (Hindi) and question_bn (Bengali) using Google Translate.

- *Rich Text Support*:
    - The answer field uses CKEditor5Field, allowing formatted and structured content for FAQs.

- *Automatic Translation Handling*:
    - If question_hi or question_bn is missing, the translate_question() method will generate the translated      versions before saving.

- *Caching for Performance Optimization*:
    - Translated questions are cached using Django’s caching framework to reduce redundant translation API calls and improve response times.


## 3. Overview of Serializers and Views

###  3.1 Serializers

The serializers handle converting the FAQ and FAQTranslation model instances into JSON format and vice versa.

- *FAQTranslationSerializer :*
    - Serializes the FAQTranslation model.
    -Returns translated questions based on the selected language.

- *FAQSerializer :*
    - Serializes the FAQ model.
    - Includes an additional computed field translated_question using SerializerMethodField.    
    - Implements get_translated_question() to fetch the translated question based on the language parameter (lang) from the request.

### 3.2 Views

The views use Django REST Framework’s ModelViewSet to provide CRUD operations for FAQs.

- *FAQViewSet :*

    - Handles API requests related to FAQs.
    - Uses FAQSerializer for data representation.

    - Implements custom list() method :
        - Retrieves the lang query parameter from the request.
        - Serializes FAQs while passing the request context to determine the language.
    
### 3.3 Functionality :

1. Retrieve All FAQs

    - Supports language-based question translation using the lang query parameter.
    - Example:
        - GET /api/faqs/?lang=hi
    - Returns FAQs with translated questions in Hindi.

2. Retrieve a Single FAQ

    - Example:
        - GET /api/faqs/1/?lang=bn
    - Fetches FAQ with Bengali translation.