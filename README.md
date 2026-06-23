# Product Chatbot Website

This is a complete beginner-friendly website for a product chatbot.

It includes:
- Product landing page
- Feature section
- FAQ section
- Floating chatbot widget
- Python Flask backend
- Editable product data file

## 1. Project files

```text
product_chatbot_website/
├── app.py
├── requirements.txt
├── data/
│   └── product_info.json
├── static/
│   ├── styles.css
│   └── script.js
└── templates/
    └── index.html
```

## 2. How to run locally

Open terminal inside this folder.

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

Install Flask:

```bash
pip install -r requirements.txt
```

Run the website:

```bash
python app.py
```

Open in browser:

```text
http://127.0.0.1:5000
```

## 3. How to customize your product

Open:

```text
data/product_info.json
```

Change:
- product_name
- tagline
- description
- price
- contact_email
- purchase_link
- features
- faqs

Example:

```json
"product_name": "Your Product Name",
"price": "₹499",
"contact_email": "your-email@gmail.com"
```

## 4. How the chatbot works

The chatbot reads your FAQs from:

```text
data/product_info.json
```

When a user asks a question, the Flask backend compares the question with your FAQ questions and keywords, then returns the best matching answer.

## 5. How to deploy online

For online hosting, upload the project to a Python hosting platform like Render, Railway, PythonAnywhere, or a VPS.

For production, use:

```bash
gunicorn app:app
```

If your hosting platform asks for a start command, use:

```bash
gunicorn app:app
```

If needed, add gunicorn to requirements.txt:

```text
gunicorn
```
