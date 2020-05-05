Building and running the application
------------------------------------

Base Image
----------
- The dockerfile is located in ../todobackend-base
- Build it any time there is a change in the OS dependencies (apt-get for example)

Dev Image (for testing and build wheels)
----------------
- The dockerfile is located in ./Docker/dev/
- Build the dev image
- Run the docker-compose in parts:
    * docker-compose build
        - If there are any src changes, they will get copied to the image at this step.
    * docker-compose up agent
    * docker-compose up test
    * docker-compose up builder
- The last step builds the wheel that will be used for the release image

Release Image
-------------
- The dockerfile is located in ./Docker/release/
- Build the release image (copies and install the wheels)
- collect static files:
    * docker-compose run --rm app manage.py collectstatic --no-input
- run migrations:
    * docker-compose run --rm app manage.py migrate --no-input
- Run the docker-compose 
- Run acceptance tests (node mocha tests)
    * docker-compose up test
    






