# Simple test of Invenio records REST server

This is the simplest implementation that I've been able to create (so far) for the purpose of demonstrating getting a record via a REST API call. The code uses the following Invenio modules directly, although these modules in turn load other Invenio modules:
* Invenio-DB
* Invenio-PIDStore
* Invenio-Records
* Invenio-Records-REST

Usage is as follows:

1. Create a fresh empty Python 3.9 environment and install the dependencies:
    ```
    pyenv virtualenv test-server
    pyenv activate test-server
    python -m pip install -r requirements.txt
    ```
2. Initialize the application and datase:
    ```
    ./app-setup.sh
    ```
3. Run the server:
    ```
    ./run-server.sh
    ```
4. In another shell, run the test script:
    ```
    ./test-getting-record.sh
    ```

You should get output like the following:
```
{
    "created": "2022-08-30T01:53:33.555056+00:00",
    "id": "1",
    "links": {},
    "metadata": {
        "access": "open",
        "authors": [
            {
                "name": "Mike Hucka"
            }
        ],
        "keywords": [
            "Caltech",
            "RDM"
        ],
        "title": "This is the title of a fake record"
    },
    "updated": "2022-08-30T01:53:33.555060+00:00"
}
```
