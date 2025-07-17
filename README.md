# Project Setup and Launch 🚀

This README outlines the steps to set up and launch both the **frontend (Vite Vue)** and **backend (Flask)** components of this project.

---

## Frontend Setup (Vite Vue)

To get the frontend up and running, follow these simple steps:

### 1. Install Dependencies
First, **navigate to the root directory** of your project where the `package.json` file is located. Then, install the necessary Node.js packages using npm:

```bash
npm i
```
This command downloads and installs all the dependencies listed in your package.json file.

2. Launch Development Server
Once the dependencies are installed, you can launch the Vite development server:

```bash
npm run dev
```
This will typically start the Vue application on http://localhost:5173 (or another port if 5173 is in use). You can then view the frontend in your web browser.

Backend Setup (Flask)
The backend is a Flask application that requires a Python virtual environment.

1. Create and Activate Virtual Environment
From the root directory of your project, create a virtual environment. It's good practice to name it venv:

```bash
python -m venv venv
```
After creating the virtual environment, activate it. The command varies slightly depending on your operating system:

macOS/Linux:


```bash
source venv/bin/activate
```
Windows (Command Prompt):

```bash
venv\Scripts\activate.bat
```
Windows (PowerShell):


```bash
venv\Scripts\Activate.ps1
```
2. Navigate to Backend Directory
Once your virtual environment is active, change your directory to the flask_backend folder:

```bash
cd flask_backend
```
3. Install Backend Dependencies
With the virtual environment active and inside the flask_backend directory, install the Python dependencies:

```bash
pip install -r requirements.txt
```
Note: Ensure you have a requirements.txt file in your flask_backend directory listing all the necessary Python packages for your Flask application. If you don't have one, you can create it by running pip freeze > requirements.txt after installing your desired packages.

4. Run the Flask Application
Finally, run the Flask application:

```bash
python main.py
```
This will start the Flask server, usually on http://127.0.0.1:5000 (or another port if configured differently in main.py). Your backend API will then be accessible.