@echo off
echo ========================================
echo  Reset Database
echo ========================================
echo.
echo Canh bao: Thao tac nay se XOA tat ca du lieu!
echo.
set /p confirm="Ban co chac chan muon reset database? (Y/N): "
if /i not "%confirm%"=="Y" (
    echo Da huy thao tac.
    pause
    exit /b 0
)

echo.
echo Dang xoa database cu...
if exist database.db (
    del database.db
    echo Da xoa database.db
) else (
    echo Database.db khong ton tai
)

echo.
echo Dang xoa anh upload...
if exist static\uploads (
    rmdir /s /q static\uploads
    echo Da xoa thu muc uploads
)

echo.
echo Khoi dong lai app de tao database moi...
python app.py

echo.
echo ========================================
echo Database da duoc reset!
echo Tai khoan admin mac dinh:
echo   Username: admin
echo   Password: admin123
echo ========================================
pause
