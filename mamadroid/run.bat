@echo off
echo Dang cai thu vien can thiet...
python -m pip install -r requirements.txt

echo.
echo Dang chay demo MAMADROID simplified...
python mamadroid_experiment.py

echo.
pause