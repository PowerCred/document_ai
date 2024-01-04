from .utils import Manager, CommonLogger
from .filesystem import Gcs, S3, URL

from PIL import Image
from os import path

class DocumentOcr(Manager):

    def __init__(self, storage_type: str = 'local'):
        super().__init__()
        storage_type = storage_type.lower()
        self.storage_type = storage_type
        if storage_type not in ['local', 'gcs', 's3', 'url']:
            raise TypeError(f"Storage type should be one of ['local', 'gcs', 's3', 'url']")

        self.__document_types = [
            'invoice', 'payslip', 'insurance', 'employment', 'utility_bills', 'bank_statement' 
        ]

    async def parse_document(self, id: str, source_filepath: str, document_type: str):
        try:
            local_path = await self.get_temp_dir(id=id)
            if document_type not in self.__document_types:
                raise ValueError(f'Unsupported document type {document_type}')
            storage_classes = {
                'gcs': Gcs,
                's3': S3,
                'url': URL  # Assuming URLDownloader is the class for 'url'
            }

            if self.storage_type in storage_classes:
                storage = storage_classes[self.storage_type]()
                status, outpath = await storage.download_file(source_filepath, local_path)
            elif self.storage_type == 'local':
                outpath = source_filepath
                status = True
            else:
                raise ValueError(f"Unsupported storage type: {self.storage_type}")
            
            if not bool(status):
                raise ValueError(outpath)
            
            if document_type != 'bank_statement':
                document_type = document_type.split('_')[0]
                url = f'{self.url}/document/{document_type}/extract'
                params = {'id': id}
                print("OUTPATH", f'{document_type}_file', outpath)
                req_body = {f'{document_type}_file': open(outpath, 'rb')}
                response, status = await self.url_requests(url=url, method='post', data=req_body, params=params)
                if status != 200:
                    print("RESPONSE", response, status)
                    raise Exception(response)
                else:
                    url = f'{self.url}/document/{document_type}/get'
                    params = {'id': id}
                    response, status = await self.url_requests(url=url, method='get', params=params)
                    return response
            elif document_type == 'bank_statement':
                mimetype = self.get_mime_type_with_mimetypes(outpath)
                if mimetype == 'application/pdf':
                    url = f'{self.url}/parse/bank/async'
                    params = {'id': id}
                    req_body = {'file': open(outpath, 'rb')}
                    response, status = await self.url_requests(url=url, method='post', data=req_body, params=params)
                    if status == 200:
                        return True, response
                    return False, response
                elif mimetype in ['image/png', 'image/jpg']:
                    print("IMAGE MIMETYPE Found")
                    image1 = Image.open(outpath)
                    outpath = path.join(local_path, f'{path.basename(outpath)}.pdf')
                    image1.convert('RGB').save(outpath, save_all=True)
                    url = f'{self.url}/parse/bank'
                    params = {'id': id}
                    req_body = {'file': open(outpath, 'rb')}
                    response, status = await self.url_requests(url=url, method='post', data=req_body, params=params)
                    if status == 200:
                        return True, response
                    return False, response
                else:
                    raise TypeError(f'Unsupported file format {mimetype}')
        except Exception as e:
            raise e


