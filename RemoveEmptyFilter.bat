::@echo off
for /f "tokens=*" %%a in ('dir /b /ad /s^|sort /r') do rd "%%a" 2>nul