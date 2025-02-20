# FastAPI, Streamlit, pydantic example

## Overview

This project is a QA Session API built using FastAPI for the backend and Streamlit for the frontend. The application allows users to create sessions, answer questions, and review their answers. The backend handles session management and data validation, while the frontend provides an interactive interface for users.

## Components

### pydantic
Pydantic is used for data validation and settings management using Python type annotations. It ensures that the data structures used in the application are correctly typed and validated.

### streamlit
Streamlit is a framework for creating interactive web applications in Python. It is used for the frontend of this project, providing an easy way to build and deploy the user interface.

### FastAPI
FastAPI is a modern, fast (high-performance) web framework for building APIs with Python 3.7+ based on standard Python type hints. It is used for the backend of this project, handling API requests and responses.

## API Endpoints

### `app.get("/new_session", response_model=SessionData)`
This endpoint creates a new session with a unique session ID and populates it with default questions. The `response_model` parameter ensures that the response is validated against the `SessionData` model.

### `session_data = SessionData.model_validate(resp.json())`
This line of code validates the JSON response from the server against the `SessionData` model. It ensures that the data received from the server conforms to the expected structure.

## File Structure

### `question_answer_pair.py`
This file defines the data models used in the application. It includes the `AnswerPair`, `QASet`, and `SessionData` classes, which represent the structure of the data used in the application.

### `@model_serializer`
The `@model_serializer` decorator is used to customize the serialization of the data models. It ensures that the data is serialized correctly when converting between Python objects and JSON.

## Sequence Diagram

![Sequence Diagram](sequence_diagram.png)

## Running the Application

### Prerequisites

Make sure you have the following installed:
- Python 3.7+
- pip (Python package installer)

### Setup

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/fastapi_streamlit_example.git
    cd fastapi_streamlit_example
    ```

2. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

### Running the FastAPI Server

1. Navigate to the `app` directory:
    ```sh
    cd app
    ```

2. Start the FastAPI server:
    ```sh
    uvicorn fastapi-server:app --reload
    ```

3. The FastAPI server will be running at `http://127.0.0.1:8000`. You can access the API documentation at `http://127.0.0.1:8000/docs`.

### Running the Streamlit Application

1. In a new terminal, navigate to the `app` directory:
    ```sh
    cd app
    ```

2. Start the Streamlit application:
    ```sh
    streamlit run streamlit_app.py
    ```

3. The Streamlit application will be running at `http://localhost:8501`.

### Accessing the Applications

- FastAPI: `http://127.0.0.1:8000`
- Streamlit: `http://localhost:8501`

## Docker and Deployment Instructions

### Dockerfile

Two `Dockerfile`s are already present in the root of your project directory:

- `Dockerfile.fastapi` for the FastAPI application
- `Dockerfile.streamlit` for the Streamlit application

### Building and Running the Docker Containers

1. **Build the Docker image for FastAPI:**

    ```sh
    docker build -t fastapi-app -f Dockerfile.fastapi .
    ```

2. **Build the Docker image for Streamlit:**

    ```sh
    docker build -t streamlit-app -f Dockerfile.streamlit .
    ```

3. **Run the Docker container for FastAPI:**

    ```sh
    docker run -d -p 8000:8000 fastapi-app
    ```

4. **Run the Docker container for Streamlit:**

    ```sh
    docker run -d -p 8501:8501 streamlit-app
    ```

### Deployment

To deploy the application, you can use a cloud service like AWS, Google Cloud, or Azure. Here are the general steps:

1. **Push the Docker images to a container registry:**

    ```sh
    docker tag fastapi-app <your_registry>/fastapi-app
    docker push <your_registry>/fastapi-app

    docker tag streamlit-app <your_registry>/streamlit-app
    docker push <your_registry>/streamlit-app
    ```

2. **Deploy the Docker containers on a cloud service:**

    - **AWS:** Use Amazon ECS or EKS.
    - **Google Cloud:** Use Google Kubernetes Engine (GKE) or Cloud Run.
    - **Azure:** Use Azure Kubernetes Service (AKS) or Azure App Service.

3. **Configure the service to expose the necessary ports and set up any necessary environment variables.**

4. **Access the application via the provided URL from the cloud service.**

### Kubernetes Deployment with Rolling Updates

1. **Apply the Kubernetes deployment configuration:**

    ```sh
    kubectl apply -f deployment.yaml
    ```

2. **Check the status of the deployments:**

    ```sh
    kubectl get deployments
    ```

3. **Perform a rolling update for the FastAPI deployment:**

    ```sh
    kubectl set image deployment/fastapi-app fastapi-app=<your_registry>/fastapi-app:<new_tag>
    ```

4. **Perform a rolling update for the Streamlit deployment:**

    ```sh
    kubectl set image deployment/streamlit-client streamlit-client=<your_registry>/streamlit-client:<new_tag>
    ```

5. **Monitor the rolling update status:**

    ```sh
    kubectl rollout status deployment/fastapi-app
    kubectl rollout status deployment/streamlit-client
    ```

## Conclusion

This project demonstrates how to build a full-stack application using FastAPI, Streamlit, and Pydantic. Each component plays a crucial role in ensuring the application is robust, interactive, and easy to maintain.