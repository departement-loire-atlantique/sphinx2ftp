Sphinx2FTP
===========

Ce script permet de récupérer tous les enregistrements d'un formulaire SPHINX (via son API) et les exporter au format CSV vers un dépôt FTP.

Installation
------------

```
pip install -r requirements.txt
```

Execution
---------

```
survey.py --sphinx_password xxx --sphinx_survey_id xxx --ftp_filename xxx --ftp_pass xxx
```