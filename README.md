# Project-2

#1. CodeCollab - Real-Time Collaborative Code Editor (Python Backend)

CodeCollab is a web application that demonstrates real-time collaboration, allowing multiple users to write and edit code in a shared environment simultaneously. Built with a **Python (Flask)** backend and a modern frontend, it uses **WebSockets** for instantaneous, bi-directional communication.

This project showcases a deep understanding of asynchronous, event-driven architecture and the complexities of managing shared state between multiple clients.

---

### Key Features

-   **Real-Time Text Sync:** Changes made by one user are instantly broadcast to all connected clients using WebSockets.
-   **Live User Presence:** A live counter displays the number of users currently active in the session.
-   **State Synchronization:** New users joining a session receive the complete, up-to-date content of the editor.
-   **Modern Frontend:** A clean, responsive user interface built with Tailwind CSS.

---

### Skills & Concepts Demonstrated

-   **Backend Development:** Building a robust server with **Python** and the **Flask** micro-framework.
-   **Real-Time Communication:** Expertise in using **WebSockets** (via Flask-SocketIO) to handle persistent, low-latency connections.
-   **Concurrency & State Management:** Managing a shared state (the editor content) and handling simultaneous connections and events without conflicts.
-   **Asynchronous Programming:** A core understanding of event-driven architecture required for real-time applications.
-   **Full-Stack Integration:** Seamlessly connecting a JavaScript frontend to a Python backend.

---

### How to Run

1.  **Prerequisites:** Python 3.x installed.
2.  **Set Up Environment:** Create and activate a virtual environment, then install dependencies.
    ```bash
    # Create a virtual environment
    python -m venv venv
    # Activate it (source venv/bin/activate on Mac/Linux or venv\Scripts\activate on Windows)

    # Install requirements
    pip install -r requirements.txt
    ```
3.  **Run the Server:**
    ```bash
    python app.py
    ```
4.  **Open in Browser:** Navigate to `http://localhost:3000`. Open multiple browser tabs to simulate different users and see the real-time collaboration in action.

#2. API Rate Limiter Middleware (Token Bucket Algorithm)

This project is a Python implementation of a sophisticated **API Rate Limiter** using the **Token Bucket algorithm**. It's designed as a middleware that can be integrated into any web framework (like Flask or FastAPI) to protect API endpoints from overuse, ensure fair usage, and enhance service reliability.

This is a crucial system design component for building robust, production-ready backend services.

---

### Key Features

-   **Token Bucket Algorithm:** Implements the efficient and flexible Token Bucket algorithm to handle bursts of traffic smoothly.
-   **Configurable Limits:** Easily configure the bucket size (burst capacity) and refill rate (sustained requests per second).
-   **Per-Client Limiting:** Tracks and applies limits on a per-user basis (e.g., by IP address or API key).
-   **Standard-Compliant:** Returns the standard `HTTP 429 Too Many Requests` status code when a user exceeds their limit.
-   **Middleware Architecture:** Designed to be seamlessly integrated as a decorator or middleware in a web application.

---

### Skills & Concepts Demonstrated

-   **System Design:** A fundamental understanding of designing for API security, scalability, and reliability.
-   **Algorithm Implementation:** Translating a classic computer science algorithm (Token Bucket) into practical, working code.
-   **Middleware & Decorators:** Advanced Python knowledge, showing how to write reusable code that can wrap and enhance API endpoints.
-   **Concurrency:** The internal state (each user's token bucket) is managed in a way that is safe for concurrent requests.
-   **API Security:** A practical application of defensive programming to prevent Denial-of-Service (DoS) attacks and API abuse.



#3. Distributed Task Scheduler with Celery and RabbitMQ

This project is a powerful backend system that demonstrates how to build a **distributed task scheduler** for handling long-running, asynchronous jobs. It uses **Celery** as the task queue framework and **RabbitMQ** as the message broker, a standard and robust architecture for building scalable microservices.

This system is designed to offload intensive tasks (like video processing, report generation, or sending bulk emails) from the main application, ensuring the user-facing API remains fast and responsive.

---

### Architecture Overview

1.  **Producer (Web App):** A Flask application that receives requests from a user and adds a "task" message to the RabbitMQ queue. It immediately returns a response to the user without waiting for the task to finish.
2.  **Message Broker (RabbitMQ):** A central message queue that receives tasks from the producer and holds them until a worker is available. It ensures task persistence and reliable delivery.
3.  **Consumers (Celery Workers):** Independent Python processes that are constantly listening to the queue. When a task appears, a worker picks it up, executes the job (e.g., processes a file), and marks the task as complete.

---

### Skills & Concepts Demonstrated

-   **Distributed Systems Architecture:** A deep and practical understanding of designing and building scalable, fault-tolerant backend systems. This is a highly advanced and sought-after skill.
-   **Microservices:** Demonstrates the principle of breaking down a monolithic application into smaller, independent services that communicate asynchronously.
-   **Asynchronous Processing & Message Queues:** Expertise in using message brokers (RabbitMQ) and task queues (Celery) to build non-blocking, high-performance applications.
-   **Scalability & Fault Tolerance:** The architecture allows for horizontal scaling by simply adding more worker nodes. The message broker ensures that tasks are not lost if a worker crashes.
-   **Backend Engineering:** A comprehensive showcase of advanced backend development beyond simple CRUD APIs.

---

### How to Run

1.  **Prerequisites:**
    -   Python 3.x
    -   Docker and Docker Compose (for easily running RabbitMQ).

2.  **Start RabbitMQ:**
    Use Docker Compose to start the message broker service.
    ```bash
    docker-compose up -d
    ```

3.  **Install Dependencies & Set Up Environment:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Start Celery Worker(s):**
    Open a new terminal and run the Celery worker. You can run this command in multiple terminals to simulate multiple workers.
    ```bash
    celery -A tasks.celery_app worker --loglevel=info
    ```

5.  **Start the Producer (Flask App):**
    In another terminal, run the main web application.
    ```bash
    python app.py
    ```

6.  **Trigger a Task:**
    Send a request to the appropriate endpoint in the Flask app (e.g., `POST /process-video`) to add a new job to the queue and watch the Celery workers pick it up.
