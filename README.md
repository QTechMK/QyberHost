# QyberHost

QyberHost is a Django-based hosting theme project adapted from the original Hostie template.

This repository currently contains the initial frontend baseline:

- Homepage based on `index-six`
- Shared top header, header, and footer across active pages
- QyberHost branding updates
- Initial template cleanup for unused home variants and sections

## Requirements

- Python 3.12+
- pip

## Installation

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Project Status

This is the initial baseline version prepared before Turkish localization, dashboard development, and third-party service integrations.
