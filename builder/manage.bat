
@if  "%1"=="" goto do_help
@..\Python25\python.exe manage.py %*
@goto end

:do_help
@echo.
@echo Topo Builder Manage
@echo usage: manage [help^|compilemessages^|makemessages^|migrate^|schemamigration]
@echo.
@echo        compilemessages               : build the message file po to mo
@echo        makemessages -a               : extract messages from source to po
@echo        migrate [--list]              : migrate the database 
@echo        schemamigration jobmng --auto : extract new schema from source
@goto end


:end