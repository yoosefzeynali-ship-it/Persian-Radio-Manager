@echo off

echo Building PersianRadioManager...

pyinstaller --clean --noconfirm --onefile --windowed --icon=assets\logo.ico --add-data "assets;assets" --name PersianRadioManager src\main.py

echo.

echo Build Finished.

pause
