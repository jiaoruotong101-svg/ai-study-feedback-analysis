@echo off
chcp 65001 >nul
cd /d "%~dp0.."
if not exist ".venv\Scripts\python.exe" (
  py -3.13 -m venv .venv
  if errorlevel 1 goto fail
)
".venv\Scripts\python.exe" -m pip install -r "运行指南\requirements.txt"
if errorlevel 1 goto fail
".venv\Scripts\python.exe" "运行指南\复现评测.py"
if errorlevel 1 goto fail
echo.
echo 复现完成。结果保存在“复现运行”文件夹，原实验文件未覆盖。
pause
exit /b 0
:fail
echo.
echo 运行失败，请保留上面的报错信息。确认已安装64位Python 3.13及Python Launcher，并能联网安装依赖。
pause
exit /b 1
