# Real-Time Market Intelligence Dashboard

A full-stack Python Flask web application designed to consume public REST API structures asynchronously, process deep nested JSON payloads natively, and dynamically parse financial market performance metrics into a clean frontend view state.

## 🚀 Architectural Network Pipeline
* **Asynchronous Client Queries:** Interfaces with open Yahoo Finance chart nodes via the `requests` library utilizing built-in timeout boundaries to handle data streams efficiently.
* **Payload Deserialization & Normalization:** Implements robust error-handling wrappers to intercept incoming byte streams, converting deep-nested array properties safely into clean, floating-point numeric keys without risking runtime app crashes.
* **Server-Side Template Engine:** Utilizes Flask's `render_template_string` logic to conditionally render active asset prices, net session deviations, and percentage delta swings based on user form selections.

## 🛠️ Software Stack
* **Language Environment:** Python 3.x
* **Core Subsystems:** Flask Microframework, Requests Connection Suite, Jinja HTML Template Engine
