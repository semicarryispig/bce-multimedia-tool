httpie-media-auth

Bce Multimedia auth plugin for HTTPie.

Installation

$ pip install --upgrade httpie-media-auth

Usage

Credentials on the CLI

The syntax and behavior is the same as with the basic auth.

Specify both access key ID and secret

http --auth-type media -a ACCESSKEYXXX:SECRETKEYXXX http://localhost:80/test
Specify only the key

There'll be a password prompt:

$ http -A media -a ACCESSKEYXXX http://localhost:80/test
http: password for ACCESSKEYXXX@localhost: <enter secret key>
Auth via the Media_* environment variables

