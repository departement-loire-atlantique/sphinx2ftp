import requests
from urllib.request import Request, urlopen
from urllib.error import HTTPError
import json
import ftplib
import argparse


def sphinx_login(args):
    api_auth = args.sphinx_base_url + "sphinxauth/connect/token"
    payload = {
        "username": args.sphinx_username,
        "password": args.sphinx_password,
        "lang": "FR_fr",
        "grant_type": "password",
        "client_id": args.sphinx_client_id,
    }

    try:
        auth = json.loads(requests.post(api_auth, data=payload).content)
    except ValueError:
        raise Exception("sphinx_client_id is incorrect")
    if "access_token" not in auth:
        raise Exception("sphinx_username or sphinx_password is incorrect")

    print("Sphinx authentication succeeded")
    return auth["access_token"]


def sphinx_download_survey(auth, args, localfilename="dataset.csv"):
    surveydata_url = (
        args.sphinx_base_url + "sphinxapi/api/survey/" + args.sphinx_survey_id + "/data"
    )
    req = Request(surveydata_url)
    req.add_header("Authorization", "Bearer {}".format(auth))

    try:
        response = urlopen(req)
        with open(localfilename, "wb") as data_file:
            data_file.write(response.read())
    except HTTPError as e:
        raise Exception(
            "sphinx_survey_id is incorrect or Sphinx in unavailable : {}".format(e)
        )

    print("Sphinx download survey succeeded")


def ftp_upload(args, localfilename="dataset.csv"):
    ftp = ftplib.FTP(args.ftp_url)
    print(ftp.login(args.ftp_login, args.ftp_pass))
    ftp.set_pasv(False)
    print(ftp.cwd(args.ftp_folder))
    with open(localfilename, "rb") as data_file:
        res = ftp.storlines("STOR " + args.ftp_filename, data_file)
    if not res.startswith("226"):
        print("Upload failed")
    else:
        print("Upload succeeded")
    ftp.quit()


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--sphinx_base_url",
        default="https://asp-loire-atlantique.sphinxonline.net/",
    )
    parser.add_argument("--sphinx_username", default="e-demarches")
    parser.add_argument("--sphinx_client_id", default="sphinxapiclient")
    parser.add_argument("--sphinx_password")
    parser.add_argument("--sphinx_survey_id")

    parser.add_argument("--ftp_url", default="fr.ftp.opendatasoft.com")
    parser.add_argument("--ftp_login", default="loireatlantique")
    parser.add_argument("--ftp_folder", default="shared")
    parser.add_argument("--ftp_filename")
    parser.add_argument("--ftp_pass")

    args = parser.parse_args()

    sphinx_download_survey(sphinx_login(args), args)
    ftp_upload(args)
