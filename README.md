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
