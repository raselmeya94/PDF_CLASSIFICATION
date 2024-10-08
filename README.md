# Project Deployment (Certificate Classification with Info Extractor)

## Prerequisites

### Python 3.10 or Above:
This guide assumes you have Python 3.10 or a later version installed. If not, refer to the official documentation for your operating system (OS) on how to install Python. Package manager commands like `sudo apt` (Ubuntu), `curl` (generic), or `brew` (macOS) might be used.

### Package Manager (Pip):
Verify that you have either `pip` (the default package manager for Python) or `con installed. If not, installation instructions are usually available online for your specific OS.



## Creating a Project Directory and Virtual Environment


### Create a Project Directory:

1. Open your terminal or command prompt.
2. Use the `mkdir` command to create a directory for your project. For example:

    ```bash
   mkdir my_django_project
    ```
3. Navigate into the project directory:
    ```bash
   cd my_django_project
    ```

### Clone Git repository:

```bash
    git clone https://github.com/raselmeya94/llm_web_application_project.git
```



### Create a Virtual Environment:

1. Use the `python -m venv` command to create a virtual environment named `cert_classify_env` (replace with your desired name):

    ```bash
   python -m venv cert_classify_env
    ```
Directory Structure:
- my_django_project (local directory)
    - cert_classify_env
    - PDF_CLASSIFICATION (git repository)
      - pdf_classification 
      - pdf_classification_app
      - manage.py
      - README.md
      - requirements.txt
### Activating the Virtual Environment:

#### macOS/Linux:
source llm_environment/bin/activate
Inside the project directory where located `cert_classify_env` and run the following command
    
```bash
source cert_classify_env/bin/activate
```   


Your terminal prompt will change to indicate that you're working within the virtual environment.


### Dependencies Installation:
Change directory and go to `PDF_CLASSIFICATION` Navigate into the project directory:

```bash
   cd PDF_CLASSIFICATION
```
 and run requirements.txt for installation dependencies.
```bash
    pip install -r requirements.txt
```

### Run PDF_CLASSIFICATION:
Run the following commands
```bash
python manage.py runserver 0.0.0.0:8000
```

The server will typically listen on the default port 8000. You can access your application by opening http://localhost:8000/ in your web browser.


