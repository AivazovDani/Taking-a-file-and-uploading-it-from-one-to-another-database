import tempfile
from pyairtable import Api
import requests
import os

# Airtable Credentials
UPLOAD_URL = 'https://i.textyou.online/campaign/login/signin'
AIRTABLE_API_KEY = "pat5CgRLCXHna9XPq.9ea1c27ae2822b58ab92bb30dfcc34f19b12c5d35475e762bbac1cc2c94aadb4"
AIRTABLE_BASE_ID = "appP0F84sv2q9AR5P"
AIRTABLE_TABLE_NAME = "DATA_IMPORTS"


class PhoneBook:
    def __init__(self):
        self.tmp_path = None
        self.original_filename = None
        self.phonebook_id = None
        self.file_id = None
        self.file_name = None
        self.headers = self.generate_heders()

    def generate_heders(self):
        headers = {
            "accept": "application/json, text/plain, */*",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "en-GB,en-US;q=0.9,en;q=0.8,bg;q=0.7",
            "authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjp7Im1vZGUiOjAsInVzZXJfaWQiOjEwNCwidXNlcl9uYW1lIjoiQ2xpY2tsYWIiLCJjdXN0b21lcl9pZCI6ODgsImN1c3RvbWVyX25hbWUiOiJNT0JJVVM6IENsaWNrbGFiIn0sImV4cCI6MTc3NDY4OTIwMH0.BKhEYtIOClbO5dLK1GR1in0zNFBKZYAnoYlrF37rfKG3qhxyGBAg4T2FDPD1xraXSrQuah_UBS7OFpOfnAts9xShDThoDxjV5ybqraX62rtiq7529VypgCYYvVP_BAE8g49KlKiy_vmTM4mXc_Y-Aw__woVWyKibiBDF-bpQYBqd0I9U0YhLvUVcUxOoH54TdFXNQ7ZHAdyHQtya6Yn6PN7-FNK98QcBDOaHiI4q7wQkfSck98505CAJn4EJdkDzENtYaCobCrT5NObJrhSba9UF8hVR_oSlBuFVYQKdSFg9wHOz2JsHfQnAKBv2Nc1dwuTsUSWTIq6EgQ_nhYZYSpBzVbUtGqREoR7EOhE3bbOfatoIwbjn4Tnm-5SNhCFQyQ58YWTMLUT6xDI9G3r-KBPnV96Dhzk8cMGi1d6NIo4dStbhYEBCtEU-iiYpBgMr52LcJVsjwu15qYEZs_Truyx50JUEO6TyruVw3MtwSwRjZOy7c-TRcwt2Kw3dyHdhq_Vr_MpRTqyBQJBsnyivd4OvDP93A1_vmhdg0KdWO-TgPvz18bGndQxM4hNk5JXQNHLE8RoqoIpQWJKJMdGjnpb1E7_LEqgns3AGVYjmtfKSbq87Gp8QZGRUcbyE65Ww_X_3MwOmANRRUhCMEiM-a-k6UE37j-tcS1zDzC4t31E",
            "content-length": "890",
            "content-type": "application/json",
            "cookie": "_campaign_ga=GA1.3.968041463.1774012251; _ym_uid=1774012251531946369; _ym_d=1774012251; _hjSessionUser_3212636=eyJpZCI6IjA4MjhhMDBhLWMwYzQtNTZlMC1hMzkxLWI1MDRhMGExNTE4NCIsImNyZWF0ZWQiOjE3NzQwMTIyNTA2MzUsImV4aXN0aW5nIjp0cnVlfQ==; _ym_isad=2; _campaign_ga_JVF3EL28Q6=GS2.3.s1774433141$o11$g0$t1774433141$j60$l0$h0; _hjSession_3212636=eyJpZCI6IjNlZjhmYTcwLTA2NzItNDQwMi04OGJjLTNjYmM1MDJmZmFlYyIsImMiOjE3NzQ0MzMxNDEzNTksInMiOjEsInIiOjEsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MX0=; _ym_visorc=w; ityo_session=eyJpdiI6Ik5IS3g2bDRGVE8xaE5jU0ZTL2Q5NkE9PSIsInZhbHVlIjoiMkNNT3I3SURLeFZNTDNTNG1wYjRLaEhYU2d6Q3VZRmNqdXBlWVhmMWVndlNKM3lPTFdvZlZPczNEUkJTOExsTi9OZTFLY2Q4RStKemZVQ2NpZ21VSWtpWXNhMG5ERHJrTjBlV2p2NVphcGptK2oyak9sVU1NSWRxLzVlbDJVcmYiLCJtYWMiOiIzMWZjODI0OGY2MWYwZDlmNzZhZDNmYWM4MGQzM2E0NWJkN2IzZGQzYmVmZmRlNDhhNzhmN2MwMzEyNGRiYjcwIiwidGFnIjoiIn0%3D",
            "origin": "https://i.textyou.online",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36"
        }

        return headers

    def proceed_files(self):

        # ---------------------------------------------------
        # ---------- Get attachments from airtable ----------
        # ---------------------------------------------------

        api = Api(AIRTABLE_API_KEY)
        table = api.table(AIRTABLE_BASE_ID, AIRTABLE_TABLE_NAME)

        records = table.all(formula="NOT({Processed})")

        for record in records:

            attachments = record["fields"]["Attachments"]

            for file in attachments:
                url = file["url"]
                filename = file["filename"]

                response = requests.get(url)

                with tempfile.NamedTemporaryFile(delete=False, suffix=f"_{filename}") as tmp:
                    tmp.write(response.content)
                    self.tmp_path = tmp.name
                    self.file_name = os.path.splitext(filename)[0]

                    print(f"{self.tmp_path} and the filename is {self.file_name}")

                # ----------------------------------------
                # ---------- Generate PhoneBook ----------
                # ----------------------------------------

                phonebook_url = 'https://i.textyou.online/campaign//api/web2/phone-book'

                data = {
                    "country_id": 233,
                    "phone_book_name": f"{self.file_name}",
                    "folder_id": None
                }

                r = requests.post(phonebook_url, headers=self.headers, json=data)

                print(r.text)

                self.phonebook_id = r.json()['phone_book_id']
                print(self.phonebook_id)

                # -------------------------------
                # ------- Upload files ----------
                # -------------------------------

                url_upload = 'https://i.textyou.online/campaign//api/web2/import/upload'

                headers = {
                    'accept': 'application/json, text/plain, */*',
                    'authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjp7Im1vZGUiOjAsInVzZXJfaWQiOjEwNCwidXNlcl9uYW1lIjoiQ2xpY2tsYWIiLCJjdXN0b21lcl9pZCI6ODgsImN1c3RvbWVyX25hbWUiOiJNT0JJVVM6IENsaWNrbGFiIn0sImV4cCI6MTc3NDY4OTIwMH0.BKhEYtIOClbO5dLK1GR1in0zNFBKZYAnoYlrF37rfKG3qhxyGBAg4T2FDPD1xraXSrQuah_UBS7OFpOfnAts9xShDThoDxjV5ybqraX62rtiq7529VypgCYYvVP_BAE8g49KlKiy_vmTM4mXc_Y-Aw__woVWyKibiBDF-bpQYBqd0I9U0YhLvUVcUxOoH54TdFXNQ7ZHAdyHQtya6Yn6PN7-FNK98QcBDOaHiI4q7wQkfSck98505CAJn4EJdkDzENtYaCobCrT5NObJrhSba9UF8hVR_oSlBuFVYQKdSFg9wHOz2JsHfQnAKBv2Nc1dwuTsUSWTIq6EgQ_nhYZYSpBzVbUtGqREoR7EOhE3bbOfatoIwbjn4Tnm-5SNhCFQyQ58YWTMLUT6xDI9G3r-KBPnV96Dhzk8cMGi1d6NIo4dStbhYEBCtEU-iiYpBgMr52LcJVsjwu15qYEZs_Truyx50JUEO6TyruVw3MtwSwRjZOy7c-TRcwt2Kw3dyHdhq_Vr_MpRTqyBQJBsnyivd4OvDP93A1_vmhdg0KdWO-TgPvz18bGndQxM4hNk5JXQNHLE8RoqoIpQWJKJMdGjnpb1E7_LEqgns3AGVYjmtfKSbq87Gp8QZGRUcbyE65Ww_X_3MwOmANRRUhCMEiM-a-k6UE37j-tcS1zDzC4t31E',
                    'referer': 'https://i.textyou.online/campaign/phone-book/null/44241/import',
                    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36',
                }

                with open(self.tmp_path, "rb") as f:
                    files = {
                        "file": (self.file_name, f, "text/csv")
                    }

                    data = {
                        "source_type": "source-file"
                    }

                    r = requests.post(url_upload, headers=headers, files=files, data=data)

                    self.file_id = r.json()['file_id']
                    self.original_filename = r.json()['original_file_name']

                    print(f"My file id is {self.file_id}")
                    print(self.file_name)

                # ------------------------------
                # -------- Import Files --------
                # ------------------------------

                import_url = f'https://i.textyou.online/campaign//api/web2/phone-book/{self.phonebook_id}/import'

                data = {
                    "phone_book_id": self.phonebook_id,
                    "phone_book_folder_id": "null",
                    "source_type": "source-file",
                    "guess_state": True,
                    "guess_timezone": True,
                    "guess_gender": True,
                    "cancellation": "import phones",
                    "error": "",
                    "sheets": None,
                    "mapping": {
                        "phone_number": 1,
                        "first_name": 0
                    },
                    "file_type": "csv",
                    "delimiter": ",",
                    "file_id": self.file_id,
                    "original_file_name": self.original_filename,
                    "birthday_format": None,
                    "data_count": None
                }

                r = requests.post(import_url, headers=self.headers, json=data)

                print(r.text)
                print(r.status_code)

                #--------- Mark as imorted ----------
                table.update(record["id"], {"Processed": True})
                table.update(record["id"], {"Name": self.file_name})
                table.update(record["id"], {"Phonebook ID": self.phonebook_id})
                
                # ----- Remove files from my OS temp -----
                os.remove(self.tmp_path)


if __name__ == "__main__":
    dan = PhoneBook()
    dan.proceed_files()
    