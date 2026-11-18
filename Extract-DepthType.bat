@"
@echo off
echo Combining DepthType archive parts...
copy /b DepthType-Windows-x64.zip.part* DepthType-Windows-x64.zip >nul
if %errorlevel% neq 0 (
    echo Error: Make sure all .part files are in the same folder.
    pause
    exit /b 1
)
echo Extracting DepthType...
powershell -NoProfile -Command "Expand-Archive -Path 'DepthType-Windows-x64.zip' -DestinationPath 'DepthType' -Force"
echo Done! Open the DepthType folder and run DepthType.exe.
pause
"@ | Set-Content -Path "Extract-DepthType.bat" -Encoding ASCII