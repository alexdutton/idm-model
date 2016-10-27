if [ ! -d env ] ; then
    python3 -m venv env
    . env/bin/activate
    pip install -r requirements.txt
else
    . env/bin/activate
fi

django-admin.py graph_models -a -o models.png --settings=idm_model.settings --pythonpath=. --layout=fdp
django-admin.py graph_models -a -o models.dot --settings=idm_model.settings --pythonpath=. --layout=fdp
