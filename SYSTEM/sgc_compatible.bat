@echo off
setlocal

echo For this to work, you need to run this program as admin (Don't worry, it gets rid of the admin when it's done :3) We promise you that we are doing nothing bad to your device! All this does is give you the right support to SigmaGreg :3


pause

openfiles >nul 2>nul
if %errorlevel% neq 0 (
    powershell -Command "Start-Process cmd -ArgumentList '/c %~0' -Verb RunAs"
    exit /b
)

set /p exe_path="Enter the path to the executable (.exe): "
set /p ico_path="Enter the path to the icon (.ico): "

assoc .sgc=SigmaGregFile
ftype SigmaGregFile="%exe_path%" "%%1"
echo File association created for .sgc with %exe_path%!

reg add "HKCR\SigmaGregFile\DefaultIcon" /ve /t REG_SZ /d "%ico_path%" /f
echo Icon set for .sgc files!

echo All operations completed successfully! Enjoy your new support for SGC files :3
pause
endlocal
