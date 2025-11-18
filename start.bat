@echo off
echo ========================================
echo  Blog System - Khoi dong ung dung
echo ========================================
echo.

echo [1/3] Kiem tra Python...
python --version
if %errorlevel% neq 0 (
    echo Loi: Python khong duoc cai dat!
    pause
    exit /b 1
)

echo.
echo [2/3] Cai dat dependencies...
pip install -r requirements.txt --quiet
if %errorlevel% neq 0 (
    echo Canh bao: Co loi khi cai dat packages
)

echo.
echo [3/3] Khoi dong server...
echo.
echo ========================================
echo  Server dang chay tai:
echo  http://127.0.0.1:5000
echo ========================================
echo.
echo Tai khoan admin mac dinh:
echo   Username: admin
echo   Password: admin123
echo.
echo Nhan Ctrl+C de dung server
echo ========================================
echo.

python app.py
pause
