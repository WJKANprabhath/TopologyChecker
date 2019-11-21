@echo OFF
:: For copying from one drive to another -xyz.txt from D:\ to E:\
mkdir "%USERPROFILE%\.qgis2\python\plugins\TopologyChecker"
xcopy /s "%CD%" "%USERPROFILE%\.qgis2\python\plugins\TopologyChecker" 