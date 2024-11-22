
python increment_version.py
python -m build
pause
twine upload dist/* --repository instrumentlab
pause