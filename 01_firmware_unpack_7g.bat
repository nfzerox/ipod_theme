@echo off

REM Change to the current script's directory
cd /d "%~dp0"
cargo r --release -- --device=nano7-refresh
pause