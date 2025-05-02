# Animatica-frontend

***Animatica*** is my diploma project that generates videos from text and 
images using neural networks. It automates animation creation with image generation,
image-to-video conversion, and post-processing.

## Deploying on Local

### Setting up the environment

#### Step 1: Create a virtual environment

###### *Linux/macOS:*

```bash
python3 -m venv venv
source venv/bin/activate
```

###### *Windows:*

```bash
python -m venv venv
source venv/Scripts/activate
```

#### Step 2: Install requirements

```bash
cd app
pip install -r requirements.txt
```

#### Step 3: Create env files

```bash
# env/api.env

API_URL=http://localhost:8080
TERMS_OF_SERVICE_URL=https://example.com/terms
```

#### Step 4: Run server

```bash
cd app
streamlit run src/main.py
```


## Deploying via Docker

Below are the basic commands to manage docker.

###### Build image
```bash
docker build -f app/Dockerfile -t animatica-frontend .
```

###### Run container
```bash
docker run -p 8501:8501 --name ui animatica-frontend
```
