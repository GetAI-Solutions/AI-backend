/app
├── /routes
│   └── product_routes.py
│   └── user_routes.py
│   └── common_routes.py
├── /domain
│   
├── /application
│   ├── product_service.py
│   └── barcode_service.py
│   └── bot_service.py
│   └── userservice.py
├── /infrastructure
│   ├── /database
│   │   └── db.py
│   └── /external
│       └── perplexity_source.py
├── /interface
│   └── product_controller.py
│   └── user_controller.py
│   └── common_controller.py
├── /schema_template
│   └── otp_template.py
│   └── template.py
│ 
├── main.py
├── config.py
│
│
├── Dockerfile                # Docker configuration
├── .env                      # Environment variables
├── requirements.txt          # Python dependencies
└── README.md                 # Project documentation
