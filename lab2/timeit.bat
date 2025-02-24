@echo off
setlocal enabledelayedexpansion

:: Get start time in milliseconds
for /F "tokens=1-4 delims=:." %%a in ("%TIME%") do (
    set /A "start_ms=(((%%a*60+%%b)*60+%%c)*1000+%%d)"
)

:: Command to measure
rem timeout /t 3 >nul
%*

:: Get end time in milliseconds
for /F "tokens=1-4 delims=:." %%a in ("%TIME%") do (
    set /A "end_ms=(((%%a*60+%%b)*60+%%c)*1000+%%d)"
)

:: Compute elapsed time (handle midnight rollover)
if %end_ms% LSS %start_ms% set /A end_ms+=86400000
set /A elapsed_ms=end_ms-start_ms

:: Display results
echo Elapsed time: %elapsed_ms% milliseconds
endlocal
