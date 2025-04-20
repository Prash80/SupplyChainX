# SupplyChainX

A modern supply chain management system that combines blockchain technology and AI to track shipments and predict potential delays.

## Features

- Real-time Shipment Tracking
- AI-Powered Delay Prediction
- Blockchain-Secured Transactions
- Role-Based Access Control
- Comprehensive Dashboard

## Tech Stack

- Python 3.x
- Flask 2.x
- Bootstrap 5.x
- Chart.js 3.x
- Custom Blockchain Implementation
- Custom AI Engine

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/SupplyChainX.git
cd SupplyChainX
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Initialize the data directory:
```bash
mkdir data
touch data/users.json
touch data/shipments.json
```

5. Run the application:
```bash
python app.py
```

## Project Structure

```
SupplyChainX/
├── app.py              # Main application file
├── blockchain.py       # Blockchain implementation
├── ai_engine.py        # AI prediction engine
├── data/              # Data storage
│   ├── users.json     # User credentials
│   └── shipments.json # Shipment data
├── templates/         # HTML templates
│   ├── base.html
│   ├── login.html
│   ├── dashboard.html
│   ├── shipment_detail.html
│   ├── ledger.html
│   └── about.html
└── static/           # Static files
    ├── css/
    └── js/
```

## Security Features

- Role-based access control
- Session management
- Blockchain-secured transactions
- Protected API endpoints

## Future Improvements

- Password hashing implementation
- HTTPS support
- Real-time GPS tracking
- Automated email notifications
- Cloud deployment
- CI/CD pipeline
- Mobile application

## Testing

The project includes functional testing for:
- Authentication
- Shipment Management
- Blockchain Transactions
- AI Predictions
- Role-based Access
- API Endpoints
- Data Persistence
- UI Components

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

For any questions or support, please contact the project maintainer. 