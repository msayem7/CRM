@echo off
call .venv\Scripts\activate.bat
cd /d "C:\My Files\Sayem\MySoft\MHM\crm\backend"
python manage.py runserver
pause

