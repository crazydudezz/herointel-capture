@echo off
echo Installing dependencies...
pip install -r requirements.txt || goto :error

echo.
echo Generating _constants.py and icon.png...
python generate_constants.py || goto :error

echo.
echo Building HeroIntelCapture.exe...
pyinstaller --noconfirm HeroIntelCapture.spec || goto :error

echo.
echo Done! Find HeroIntelCapture.exe in the dist\ folder.
pause
exit /b 0

:error
echo.
echo Build failed.
pause
exit /b 1
