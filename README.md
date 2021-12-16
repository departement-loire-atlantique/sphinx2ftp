Sphinx2FTP
===========

Ce script permet de récupérer tous les enregistrements d'un formulaire SPHINX (via son API) et les exporter au format CSV vers un dépôt FTP.

Installation
------------

Ce script nécessite Python 3. Testé avec la version 3.4.4. Aucun module python additionel n'est nécessaire.

Execution
---------

```
python3 sphinx2ftp.py --sphinx_password xxx --sphinx_survey_id xxx --ftp_filename xxx --ftp_pass xxx
```