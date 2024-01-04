=====
Usage
=====

To use PowerCred Document AI in a project with local files::

    from document_ai.document_ocr import DocumentOcr
    from document_ai.auth import Auth
    import asyncio

    from os import environ

    environ['APIKEY'] = '<YOUR_APIKEY>'
    auth = Auth(secret='<YOUR_APISECRET>')

    auth_token = asyncio.run(auth.get_session_token(user_id='test-document'))
    session_id = auth_token['id']

    do = DocumentOcr(storage_type='local')

    r = asyncio.run(do.parse_document(id=session_id, source_filepath='<YOUR FILEPATH>', document_type='invoice'))

    # Supported document_type are:
    # invoice
    # payslip
    # utility_bills
    # bank_statement
    print(r)


To use PowerCred Document AI in a project with files in google cloud bucket::

    from document_ai.document_ocr import DocumentOcr
    from document_ai.auth import Auth
    import asyncio

    from os import environ

    environ['APIKEY'] = '<YOUR_APIKEY>'
    auth = Auth(secret='<YOUR_APISECRET>')

    # Specify GCP variables
    environ['GOOGLE_APPLICATION_CREDENTIALS'] = <path/to/your/service_account.json>
    environ['BUCKET'] = <YOUR GCS BUCKET NAME>

    auth_token = asyncio.run(auth.get_session_token(user_id='test-document'))
    session_id = auth_token['id']

    do = DocumentOcr(storage_type='gcs')

    r = asyncio.run(do.parse_document(id=session_id, source_filepath='<YOUR GCS BLOB PATH>', document_type='invoice'))

    # Supported document_type are:
    # invoice
    # payslip
    # utility_bills
    # bank_statement
    print(r)

To use PowerCred Document AI in a project with files in AWS S3 bucket::

    from document_ai.document_ocr import DocumentOcr
    from document_ai.auth import Auth
    import asyncio

    from os import environ

    environ['APIKEY'] = '<YOUR_APIKEY>'
    auth = Auth(secret='<YOUR_APISECRET>')

    # Specify GCP variables
    environ['AWS_ACCESS_KEY_ID'] = <YOUR AWS ACCESS KEY ID>
    environ['AWS_SECRET_ACCESS_KEY'] = <YOUR AWS SECRET KEY>
    environ['BUCKET'] = <YOUR S3 BUCKET NAME>

    auth_token = asyncio.run(auth.get_session_token(user_id='test-document'))
    session_id = auth_token['id']

    do = DocumentOcr(storage_type='s3')

    r = asyncio.run(do.parse_document(id=session_id, source_filepath='<YOUR S3 BLOB PATH>', document_type='invoice'))

    # Supported document_type are:
    # invoice
    # payslip
    # utility_bills
    # bank_statement
    print(r)