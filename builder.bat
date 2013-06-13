@REM detect SVN version,need SVN 1.6+
svn --version >nul 2>nul
@if %ERRORLEVEL% EQU 0 goto OK_SVN
@echo.
@echo Topo Builder need SVN 1.6+, please install SVN command line client and run builder again.
@pause
@goto END

:OK_SVN
cd builder
@set PORT=8000
@if NOT (%1)==() set port=%1
@if NOT EXIST builder.db copy sample.db builder.db

@REM check for db compatiable
@..\Python25\python.exe manage.py migrate --list | find "( )"
@if NOT %ERRORLEVEL% EQU 0 goto OK_DB
@echo.
@echo WARNING: Database version mismatch, you need migrate your db using
@echo manage.bat migrate, then restart builder.
@pause
@goto END

:OK_DB
start "Topo Builder" ..\python25\python manage.py runserver --noreload 0.0.0.0:%PORT%


:END