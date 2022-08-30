import os

from flask import Flask, Blueprint

from invenio_db import InvenioDB
from invenio_pidstore import InvenioPIDStore
from invenio_records import InvenioRecords
from invenio_records_rest import InvenioRecordsREST

#
# Create the basic application using off-the-shelf Invenio modules.
#

app = Flask('My Test App')

# Before invoking the module extension classes, we have to set certain
# configuration variables.
app.config.update(
    # TESTING is a Flask variable. It changes some FLask behaviors; notably,
    # exceptions are propagated rather than handled by the the app’s handlers.
    TESTING=True,

    # This next variable tells Flask the location of the database to use.
    SQLALCHEMY_DATABASE_URI=os.environ.get(
        "SQLALCHEMY_DATABASE_URI", "sqlite:///app.db"
    ),

    # The next ones are used by InvenioRecordsREST
    RECORDS_REST_DEFAULT_CREATE_PERMISSION_FACTORY=None,
    RECORDS_REST_DEFAULT_DELETE_PERMISSION_FACTORY=None,
    RECORDS_REST_DEFAULT_READ_PERMISSION_FACTORY=None,
    RECORDS_REST_DEFAULT_UPDATE_PERMISSION_FACTORY=None,
)

InvenioDB(app)
InvenioPIDStore(app)
InvenioRecords(app)
InvenioRecordsREST(app)

#
# Define the route /myrecords
#

# The part of InvenioRecordsREST and InvenioREST that looks up records wants
# persistent id's, but what we hand to the route is a record id.  The lookup
# code needs a converter. This is hooked in via the Flask url_map variable.
from invenio_records_rest.utils import PIDConverter
app.url_map.converters["pid"] = PIDConverter

# Next, define the route for /myrecords
from invenio_records_rest.schemas import RecordSchemaJSONV1
from invenio_records_rest.serializers.json import JSONSerializer
from invenio_records_rest.utils import allow_all
from invenio_records_rest.views import RecordResource
from invenio_records_rest.serializers.response import record_responsify

# Construct a function that we'll use to serialize responses.
json_v1 = JSONSerializer(RecordSchemaJSONV1)

# Create a blank Flask blueprint structure. This won't have any routes yet.
blueprint = Blueprint("testapp_blueprint", 'testapp')

# Add a REST end point to the blueprint. The route pattern specification for
# Flask inside the angle brackets means this:
#
#  - the name of the variable passed to the function is pid_value
#  - the data type passed to the function is pid
#  - the incoming value is of type recid
#  - the values are mapped using the pid converter hooked into url_map above

blueprint.add_url_rule(
    "/myrecords/<pid(recid):pid_value>",
    view_func=RecordResource.as_view(
        "myrecid_item",
        serializers={
            "application/json": record_responsify(json_v1, "application/json")
        },
        default_media_type="application/json",
        read_permission_factory=allow_all,
        update_permission_factory=allow_all,
        delete_permission_factory=allow_all,
    ),
)

# Register the Blueprint we just created. In Flask's scheme of things, this
# will result in the blueprint getting an entry point named like this:
#    testapp_blueprint.myrecid_item
# The "testapp_blueprint" part comes from the name given to the Blueprint
# constructor call earlier, and the "myrecid_item" is in the view_func
# definition above.

app.register_blueprint(blueprint)

# For debugging: print to stdout a list of the routes we have so far.
# This is commented out.  Uncomment the lines below to see the output.
#
# app_routes = app.url_map.iter_rules()
# while (route := next(app_routes, None)):
#     print('Route defined: ', route)


#
# Add a sample record.
#

from flask import cli
from invenio_db import db
from invenio_pidstore.models import PersistentIdentifier, PIDStatus
from invenio_records.api import Record


# This define a Flask fixture that we use in a separate command (in
# app-setup.sh) to load a record into the database.  The code below does not
# actually add the record when this file is executed by Flask; it only
# defines a command that we have to call separately from the outside.
#
# I've tried many ways to put this into a separate file or to run it here
# without using the Flask fixture mechanism, but failed. Running the code
# here (even inside an app context or test app context) fails with errors
# that I don't fully understand; conversely, putting this fixture code in a
# separate file seems to be hard because there's no way to tell flask they're
# in a separate file, which means *this* file has to import the fixtures
# file, which leads to circular imports, and anyway, where's the modularity
# in that?  So I'm leaving it here.

@app.cli.group()
def fixtures():
    """Command for working with test data."""


@fixtures.command()
@cli.with_appcontext
def create_sample_record():
    """Create a sample record in the database.
    Note: Flask fixtures turn underscores in function names to dashes,
    so invoke this function using "flask fixtures create-sample-record".
    """

    db.create_all()

    rec1_uuid = "abcdabcd-1234-5678-abcd-b100dc0ffee5"

    with db.session.begin_nested():
        PersistentIdentifier.create(
            "recid",
            "1",
            object_type="rec",
            object_uuid=rec1_uuid,
            status=PIDStatus.REGISTERED,
        )

        Record.create(
            {
                "title": "This is the title of a fake record",
                "authors": [
                    {"name": "Mike Hucka"},
                ],
                "access": "open",
                "keywords": ["Caltech", "RDM"],
            },
            id_=rec1_uuid,
        )

    db.session.commit()
