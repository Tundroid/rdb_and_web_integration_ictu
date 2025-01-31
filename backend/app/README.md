# Shopend v0.1

Welcome to the **Shopend**! This RESTful API is built with Flask and SQLAlchemy, designed for managing a retail or wholesale shop’s core inventory and sales operations. It includes depot management, inventory tracking, and transaction logging.

## Table of Contents
- [Features](#features)
- [Architecture](#architecture)
- [Technologies Used](#technologies-used)
- [Setup](#setup)
- [Environment Variables](#environment-variables)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [License](#license)

## Features
- Central depot management
- Warehouse and shop inventory tracking
- Transaction logging and audit trails
- JSON-based payloads for all database insertions
- HTTP response status reporting

## Architecture
The API is deployed with the following components:
1. **Flask + Gunicorn**: Manages request handling and routing.
2. **Nginx**: Acts as a reverse proxy to handle HTTPS connections and load balancing.
3. **MySQL Database**: Stores inventory, user accounts, and transaction records.
4. **UFW Firewall**: Protects the server by managing network access.

![Architecture Diagram](imgs/architecture.png)

## Technologies Used
- **Backend**: Flask, SQLAlchemy
- **Database**: MySQL
- **Server**: Gunicorn (application server) + Nginx (web server)
- **Security**: UFW firewall, HTTPS

## Infrastructure

![Infrastructure Diagram](imgs/infrastructure.png)

## Setup

### Prerequisites
- **Python 3.8+**
- **MySQL**
- **Virtual environment tool** (recommended)
- **Nginx**
- **Gunicorn**

### Installation
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Tundroid/shopend.git
   cd shopend
