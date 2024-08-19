# get-ai API Service

This project provides a RESTful API using FastAPI to support the get-ai service. The service includes various endpoints for user management, product barcode scanning, product details retrieval, and AI-driven chat interactions.

## Features

- **User Management**: Supports user sign-up, login, and OTP-based authentication.
- **Product Barcode Scanning**: Users can upload images of barcodes, and the API extracts the barcode value.
- **Product Information Retrieval**: Allows users to retrieve detailed information and summaries for products based on scanned barcodes.
- **User History Tracking**: Tracks user product history and chat history associated with each product.
- **AI-Powered Chat**: Provides a chat interface where users can ask questions about products, and responses are generated using AI models in their preferred language.
- **Feedback System**: Allows users to submit feedback on products.
- **Product Management**: Includes endpoints for adding new products and retrieving product details from the database.

## Technologies Used

- **FastAPI**: Web framework for building the API.
- **MongoDB**: Used for user data, product data, and history storage.
- **OpenAI API**: Integrated for generating AI responses.
- **PIL**: Used for handling images, specifically barcode scanning.
- **Yagmail**: For sending OTP emails.
- **Environment Variables**: Managed using `python-dotenv`.

## Endpoints Overview

1. **User Management**
   - `POST /signup`: Register a new user.
   - `POST /send-otp`: Send OTP to the user’s email.
   - `POST /login`: Log in with email or phone number.

2. **Product Management**
   - `POST /upload-barcode`: Upload a barcode image to extract and decode the barcode.
   - `POST /get-product`: Retrieve product details using the barcode.
   - `POST /get-product-summary`: Get a summary of the product’s information.
   - `POST /add-product`: Add a new product to the database.
   - `GET /get-all-products`: Get a list of all products in the database.
   - `GET /get-barcode-not-in-db`: Retrieve barcodes that do not have product information in the database.

3. **User History**
   - `POST /get-user-product-history`: Retrieve the user’s product search history.
   - `POST /get-user-chat-history`: Retrieve the user’s chat history associated with a specific product.

4. **AI-Powered Chat**
   - `POST /chat`: Interact with the AI model for product-related queries.

5. **User Feedback**
   - `POST /give-user-feedback`: Submit feedback for a product.

6. **User Preferences**
   - `PATCH /update-preferred-language`: Update the user’s preferred language (supports EN, FR, SW).

## Environment Setup

1. **Install Dependencies**:
   ```
   pip install -r requirements.txt
   ```

2. **Set Up Environment Variables**:
   Use a `.env` file to manage environment variables:
   ```
   APP_ENV=local
   OAI_KEY=your_openai_key
   DATABASE_URI=your_mongo_db_uri
   REPLICATE_API_TOKEN=your_replicate_token
   G_APP_PASSWORD=your_email_app_password
   ```

3. **Run the Application**:
   ```
   uvicorn main:app --reload
   ```

## How to Use

- Access the API documentation at `/get-ai/dev/documentation` for local development or at `/get-ai-service/dev/documentation` for production.
- Test various endpoints using the interactive Swagger UI available in the documentation.