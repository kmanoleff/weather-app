# Weather API

Simple API for gathering weather data based on user-input location.  The technologies used include

- [Docker](https://palletsprojects.com/p/flask/) for containerization
- [flask](https://palletsprojects.com/p/flask/) framework
- [flasgger](https://github.com/flasgger/flasgger) to generate the swagger documentation
- [flask-marshmallow](https://flask-marshmallow.readthedocs.io/en/latest/) for serialization
- [apispec](https://apispec.readthedocs.io/en/latest/) for the integration between flasgger and marshmallow

### Docker Setup

In order to run this project containerized you'll need Docker installed.

* [Windows](https://docs.docker.com/windows/started)
* [OS X](https://docs.docker.com/mac/started/)
* [Linux](https://docs.docker.com/linux/started/)

Once Docker is installed:

1.  Checkout the code to your local machine.
2.  From terminal `cd` to the project directory root.
3.  Simply run `docker-compose -f docker-compose.dev.yml up --build`.  
    
With the `build` command in the `docker-compose.dev.yml` file, the above command uses the `Dockerfile` to assemble 
the image with the proper configuration (using Flask, requirements in the `requirements.txt` file, etc).  This would be
useful to ensure that all configurations are consistent across any shared instance of this project.

### Unit Tests

The `Dockerfile` also contains `RUN python -m unittest test/*` command which runs the unit tests defined in the 
`/test` directory.  The current unit test checks the weather for a *know location* and ensures the status code of `200`.
If this check fails, the Docker build would fail.  This would be useful to check an expected action before deployment 
pipeline; troubleshoot fail.

### Swagger Documentation

This API is self documenting using Swagger.  For example, taking a look at the `/weather` endpoint in the `weather_route` 
we can define and document that endpoint using the `@swag_from` annotation.  This generates Swagger documentation from the code
(`weather_model`, `weather_schema`).  This would be useful because if any code changes are made the documentation would be
reflected with those changes.

Open browser and navigate to [http://localhost:8080/apidocs/](http://localhost:8080/apidocs/) to view the interactive docs.

From here you can view information such as endpoint routes, required parameters, and data models.  This would be useful
in providing to clients to make integration and testing easier.  Testing can be done through Swagger using the "Try it 
out" functionality, or you could use your favorite API testing suite like [Postman](https://www.postman.com/).

### Function Code

The goal of this API is to retrieve weather data for a given location.  To retrieve weather the location must be
geocoded (lat/lon) coordinates.  The user input will be a city, state, country so the `weather_service` first geocodes
the user input and then returns the weather data for that location using the `WeatherModel` object.  Any errors are 
built as an `ErrorModel` and returned in the response. 

### Cleaning Up

Simply run `Ctrl+C` from the terminal to shut down the Docker container.


