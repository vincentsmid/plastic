# Plastic

Plastic is made to take orders for my 3D printing business.

Upon running in docker-compose you can either go to localhost:8000 to see the website or go to localhost:8000/calculator to access the calculator, where you can upload .stl files and in console you will get estimated print time, material weight and estimated price.

Dev environment completely automatised on docker. - just run 
```bash
docker-compose up
```

Development database password is adminadminadmin - user "admin"

## API documentation

### [Swagger UI](https://localhost:8000/docs)

Swagger UI is used to manually test and check API endpoints.

### [Database admin panel](http://localhost:8000/database)

Here runs piccolo admin - here you can see everything important in databases - refer to Database structure below to see what is what.


