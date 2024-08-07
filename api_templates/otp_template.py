html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>OTP Verification</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                color: #333;
                padding: 20px;
                text-align: center;
            }
            .container {
                max-width: 600px;
                margin: 0 auto;
                background-color: #ffffff;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }
            .header {
                font-size: 24px;
                font-weight: bold;
                color: #4CAF50;
            }
            .otp {
                font-size: 36px;
                font-weight: bold;
                margin: 20px 0;
                color: #FF5722;
            }
            .message {
                font-size: 16px;
                margin-bottom: 20px;
            }
            .footer {
                font-size: 12px;
                color: #888;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">OTP Verification</div>
            <div class="message">Your One-Time Password (OTP) is:</div>
            <div class="otp">{{ otp }}</div>
            <div class="message">Please use this OTP to complete your verification. This OTP is valid for the next 10 minutes.</div>
            <div class="footer">If you did not request this OTP, please ignore this email.</div>
        </div>
    </body>
    </html>
    """