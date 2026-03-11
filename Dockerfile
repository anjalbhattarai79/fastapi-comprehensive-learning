FROM python:3.11
# allows us to use relative paths in the rest of the Dockerfile commands.
WORKDIR /usr/src/app 

# Copy requirements.txt separetely to leverage Docker cache for dependencies.
# In future, if we change the source code but not the dependencies, Docker will use the cached layer for installing dependencies, 
#which speeds up the build process.
COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the container.
COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
