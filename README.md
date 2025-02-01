# FAQ project details

## 1. Setting up Django project

### Creating Django project and and starting an app

```bash
django-admin startproject faq_project
cd faq_project
django-admin startapp faqs

```

### Installing all dependencies

```bash
pip3 install django djangorestframework django-ckeditor-5 django-redis googletrans==4.0.0-rc1
```

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


## 4. Test cases

This test case is designed to validate the functionality of the FAQ model, specifically the translation feature. Here's a breakdown:

### **Test Case Class**
- **`FAQModelTest`**:
  Inherits from `django.test.TestCase`, which allows for testing Django models and functionality.

#### **setUp Method**
- **Purpose**: Sets up the initial data required for the test.
- **Implementation**:  
  Creates an instance of the `FAQ` model with the following attributes:
  - `question`: "Hello"
  - `answer`: "This is a test FAQ"
  - `language`: 'en' (English)

#### **test_translation Method**
- **Purpose**: Verifies that the translation functionality of the `FAQ` model works as expected.
- **Implementation**:
  - Calls `get_translated_question('hi')` to fetch the Hindi translation of the question.
  - Asserts that the translation is not `None` (indicating that the translation is available).

### **Test Execution**
To run the test, use the following command:

```bash
python manage.py test faqs
```

## 5 . API testing  

### 1. FAQ API Endpoints

### **GET /faqs/**
- **Description**: Fetch a list of all FAQs.
- **HTTP Method**: `GET`
- **Parameters**: 
  - `lang` (optional): The language code for the FAQ (e.g., `lang=hi` for Hindi or `lang=en` for English).
- **Response**:
  - **200 OK**: A list of all FAQs in the specified language.
  - **Example**:
    ```json
    [
      {
        "id": 1,
        "question": "What is Django?",
        "answer": "Django is a Python-based web framework.",
        "language": "en"
      },
      {
        "id": 2,
        "question": "क्या है Django?",
        "answer": "Django एक पायथन आधारित वेब फ्रेमवर्क है।",
        "language": "hi"
      }
    ]
    ```

### **GET /faqs/{id}/**
- **Description**: Fetch a specific FAQ by its ID.
- **HTTP Method**: `GET`
- **Parameters**:
  - `id`: The ID of the FAQ to fetch.
  - `lang` (optional): The language code for the FAQ response.
- **Response**:
  - **200 OK**: A specific FAQ.
  - **Example**:
    ```json
    {
      "id": 1,
      "question": "What is Django?",
      "answer": "Django is a Python-based web framework.",
      "language": "en"
    }
    ```

### **POST /faqs/**
- **Description**: Create a new FAQ.
- **HTTP Method**: `POST`
- **Request Body**:
  - `question` (string): The question for the FAQ.
  - `answer` (string): The answer for the FAQ.
  - `language` (string): The language code for the FAQ (e.g., `en`, `hi`).
- **Response**:
  - **201 Created**: The FAQ has been created successfully.
  - **Example**:
    ```json
    {
      "id": 3,
      "question": "What is Python?",
      "answer": "Python is a programming language.",
      "language": "en"
    }
    ```

### **GET /faqs/translations/{faq_id}/**
- **Description**: Retrieve translations for a specific FAQ.
- **HTTP Method**: `GET`
- **Parameters**:
  - `faq_id`: The ID of the FAQ to fetch translations for.
- **Response**:
  - **200 OK**: A list of translations for the FAQ.
  - **Example**:
    ```json
    [
      {
        "language": "hi",
        "translated_question": "Python क्या है?"
      },
      {
        "language": "fr",
        "translated_question": "Qu'est-ce que Python?"
      }
    ]
    ```

### **POST /faqs/{faq_id}/translations/**
- **Description**: Create or update a translation for a specific FAQ.
- **HTTP Method**: `POST`
- **Request Body**:
  - `language` (string): The language code for the translation (e.g., `hi`, `fr`).
  - `translated_question` (string): The translated question text.
- **Response**:
  - **200 OK**: The translation has been created or updated successfully.
  - **Example**:
    ```json
    {
      "language": "hi",
      "translated_question": "Python क्या है?"
    }
    ```

---

### 2. API URL Summary

| **Endpoint**                          | **Description**                                    | **Method**  | **Parameters**                              |
|---------------------------------------|----------------------------------------------------|-------------|---------------------------------------------|
| `/faqs/`                              | Get a list of all FAQs.                           | `GET`       | `lang` (optional)                          |
| `/faqs/{id}/`                         | Get an individual FAQ by ID.                      | `GET`       | `id` (required), `lang` (optional)         |
| `/faqs/`                              | Create a new FAQ.                                 | `POST`      | `question`, `answer`, `language` (required) |
| `/faqs/translations/{faq_id}/`        | Get translations for a specific FAQ.              | `GET`       | `faq_id` (required)                        |
| `/faqs/{faq_id}/translations/`        | Create or update translation for a FAQ.           | `POST`      | `language`, `translated_question` (required) |

---

## 3. Example URL Usage

- **To get all FAQs in English**:  
  `GET /faqs/?lang=en`

- **To get FAQ with ID `1` in Hindi**:  
  `GET /faqs/1/?lang=hi`

- **To create a new FAQ**:  
  ```json
  POST /faqs/
  {
      "question": "What is Django?",
      "answer": "Django is a Python-based web framework.",
      "language": "en"
  }


