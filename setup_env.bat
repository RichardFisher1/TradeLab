@echo off
setlocal

echo Starting setup...

REM Step 1: Create a virtual environment (if it doesn't exist)
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo Failed to create virtual environment
        exit /b 1
    )
    echo Virtual environment created.
) else (
    echo Virtual environment already exists.
)

REM Step 2: Activate the virtual environment
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo Failed to activate virtual environment
    exit /b 1
)
echo Virtual environment activated.

REM Step 3: Upgrade pip
echo Upgrading pip...
call venv\Scripts\python.exe -m pip install --upgrade pip
if errorlevel 1 (
    echo Failed to upgrade pip
    exit /b 1
)

REM Step 4: Install dependencies from requirements.txt
if exist "requirements.txt" (
    echo Installing dependencies from requirements.txt...
    call venv\Scripts\python.exe -m pip install -r requirements.txt
    if errorlevel 1 (
        echo Failed to install dependencies from requirements.txt
        exit /b 1
    )
) else (
    echo No requirements.txt found. Skipping dependency installation.
)

REM Step 5: Install the entire project as an editable package
echo Installing the project as an editable package...
call venv\Scripts\python.exe -m pip install -e .
if errorlevel 1 (
    echo Failed to install project as an editable package
    exit /b 1
)

echo Setup complete. Virtual environment is ready.
