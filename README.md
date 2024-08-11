# get-ai Backend README

## Overview

This project provides the backend for the `get-ai` service, a FastAPI-based application that facilitates user interactions with AI-powered services. The backend includes user authentication, product management, and barcode scanning functionalities, integrated with MongoDB for data storage.

## Features

- **User Authentication:** Supports user signup and login with email or phone number.
- **OTP Sending:** Generates and sends OTPs via email for verification.
- **Product Management:** Allows uploading, retrieving, and summarizing product details based on barcode data.
- **User History Management:** Tracks user product history and chat interactions.
- **Barcode Scanning:** Extracts barcode data from images.

## Technologies Used

- **Python**: The primary programming language.
- **FastAPI**: Web framework for building APIs.
- **MongoDB**: NoSQL database for storing user and product data.
- **PIL**: Python Imaging Library for image processing.
- **OpenAI API**: For generating AI-driven responses and summaries.
- **Yagmail**: For sending emails with OTPs.
- **CORS Middleware**: To handle Cross-Origin Resource Sharing.

## Project Structure

```plaintext
.
├── api_templates/
│   └── templates.py          # Data models for API requests
├── helpers/
│   └── helper.py             # Helper functions for barcode scanning, AI response, etc.
├── main.py                   # Main application code (provided above)
├── .env                      # Environment variables (not included in version control)
└── README.md                 # This file
```

## Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/your-repo/get-ai-backend.git
    cd get-ai-backend
    ```

2. **Create a virtual environment and activate it:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Set up environment variables:**
    - Create a `.env` file in the root directory.
    - Add the following environment variables:

    ```plaintext
    APP_ENV=local
    OAI_KEY=your_openai_api_key
    DATABASE_URI=your_mongodb_connection_string
    REPLICATE_API_TOKEN=your_replicate_api_token
    G_APP_PASSWORD=your_email_app_password
    ```

## Running the Application

Start the FastAPI application:

```bash
uvicorn main:app --reload
```

This will start the server locally, accessible at `http://127.0.0.1:8000`. The documentation will be available at `http://127.0.0.1:8000/get-ai/dev/documentation`.

## API Endpoints

### **Root Endpoint**

- **`GET /get-ai/`**
  - Returns a welcome message.

### **User Signup**

- **`POST /get-ai/signup`**
  - Signs up a new user.
  - **Payload:** `SignUp` (email, password, etc.)

### **Send OTP**

- **`POST /get-ai/send-otp`**
  - Sends an OTP to the user's email.
  - **Form:** `email`

### **User Login**

- **`POST /get-ai/login`**
  - Logs in an existing user.
  - **Payload:** `LogIN` (email or phone number, password)

### **Upload Barcode Image**

- **`POST /get-ai/upload-barcode`**
  - Uploads an image containing a barcode and extracts the barcode data.
  - **Form:** `file`, `id`

### **Get Product Details**

- **`POST /get-ai/get-product`**
  - Retrieves product details based on a barcode.
  - **Form:** `bar_code`, `user_id`

### **Get Product Summary**

- **`POST /get-ai/get-product-summary`**
  - Retrieves an AI-generated summary of the product details.
  - **Form:** `bar_code`

### **Add New Product**

- **`POST /get-ai/add-product`**
  - Adds a new product to the database.
  - **Form:** `file`, `product_code`, `product_name`

### **Get User Product History**

- **`POST /get-ai/get-user-product-history`**
  - Retrieves the product history for a specific user.
  - **Form:** `ID`

### **Get User Chat History**

- **`POST /get-ai/get-user-chat-history`**
  - Retrieves the chat history for a specific user and product.
  - **Form:** `ID`, `barcode`

## Environment Variables

- **`APP_ENV`**: Defines the environment the app is running in (e.g., `local`, `production`).
- **`OAI_KEY`**: API key for OpenAI.
- **`DATABASE_URI`**: MongoDB connection string.
- **`REPLICATE_API_TOKEN`**: Token for image processing service.
- **`G_APP_PASSWORD`**: App password for sending emails via Gmail.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue for any improvements or bug fixes.

---


# To run locally
uvicorn --host 0.0.0.0 --port 4500 --reload main:app
