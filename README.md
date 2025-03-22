# Animatica-frontend

## Table of Contents

- [Overview](#overview)
- [Requirements](#requirements)
- [Deploying on Local](#deploying-on-local)
- [Deploying via Docker](#deploying-via-docker)


## Overview

***Animatica*** is my diploma project that generates videos from text and 
images using neural networks. It automates animation creation with image generation,
image-to-video conversion, and post-processing.


## Requirements⚠️

- Python 3.8+
- PyTorch
- Streamlit
- Docker (for deployment through containers)


## Deploying on Local

**Step 1.**

Create a virtual environment.

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

**Step 2.**

```bash
pip install -r requirements.txt
```

**Step 3.**

```bash
streamlit run main.py
```


## Deploying via Docker

Below are the basic commands to manage docker.

###### Image creating

```bash
docker build . --tag animatica
docker run -p 8080:8080 animatica
```

###### Docker-compose

```bash
docker-compose up --build
docker-compsose down
```
