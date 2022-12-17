# remove conflicting library
pip3 uninstall flask-socketio -y

# start postgres service
service postgresql start

# setup and populate the testing database
su - postgres bash -c "psql < /home/workspace/backend/setup-trivia.sql"
su - postgres bash -c "psql trivia < /home/workspace/backend/trivia.psql"


# setup and populate the testing database
su - postgres bash -c "psql < /home/workspace/backend/setup-test.sql"
su - postgres bash -c "psql trivia_test < /home/workspace/backend/trivia.psql"