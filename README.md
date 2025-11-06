# SF Smart Mobility Assistant

A proof-of-concept application utilizing AI/ML to address traffic and mobility problems in San Francisco through predictive analytics.

## Overview

This application combines two AI-powered solutions to improve urban mobility in San Francisco:

1. **Predictive Transit Performance**: Predicts Muni bus delays to help riders plan better
2. **Parking Prediction**: Forecasts parking availability and suggests optimal pricing to reduce congestion

## Problem Statement

San Francisco faces significant urban mobility challenges:
- Unpredictable Muni bus delays causing rider frustration
- Traffic congestion from drivers "cruising" for parking
- Need for data-driven decisions to improve transit reliability and parking efficiency

## ML Approaches

### 1. Transit Delay Prediction (Time-Series Regression)
- **Goal**: Predict bus delay in minutes for specific routes/stops in next 15 minutes
- **Data Source**: 511 SF Bay Transit Data APIs (GTFS Feeds)
- **Key Features**: 
  - Historical delay patterns
  - Time of day / day of week
  - Weather conditions
  - Special events

### 2. Parking Availability Prediction (Classification/Regression)
- **Goal**: Predict probability of finding parking and suggest dynamic pricing
- **Data Source**: DataSF Parking Meter Transactions/Status datasets
- **Key Features**:
  - Historical occupancy rates
  - Time-based patterns
  - Neighborhood characteristics
  - Event schedules

## Project Structure

```
SF-traffic-problem/
├── data/
│   ├── raw/              # Raw data from APIs
│   ├── processed/        # Cleaned and feature-engineered data
│   └── models/           # Trained ML models
├── src/
│   ├── transit/          # Transit prediction module
│   ├── parking/          # Parking prediction module
│   ├── api/              # FastAPI backend
│   └── frontend/         # Web interface
├── notebooks/            # Jupyter notebooks for exploration
├── tests/                # Unit and integration tests
├── docs/                 # Additional documentation
└── config/               # Configuration files
```

## Key Features

1. **Real-Time Transit Delay Map**: Interactive map showing predicted delays for Muni routes
2. **Parking Availability Heatmap**: Visual representation of parking probability by neighborhood
3. **Smart Mobility Decision Helper**: Recommends transit vs. driving based on current conditions
4. **Historical Analytics Dashboard**: Trends and insights from historical data

## Technology Stack

- **Backend**: Python 3.11+, FastAPI
- **ML/Data Science**: pandas, scikit-learn, Prophet/LSTM, XGBoost
- **Frontend**: React.js with Leaflet.js for maps
- **Database**: PostgreSQL (SQLite for development)
- **Visualization**: Plotly, Matplotlib
- **APIs**: 511 SF Bay API, DataSF Open Data API

## Getting Started

### Prerequisites

```bash
python >= 3.11
node >= 18.0
postgresql >= 14
```

### Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/SF-traffic-problem.git
cd SF-traffic-problem

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up configuration
cp config/config.example.yaml config/config.yaml
# Edit config.yaml with your API keys
```

### Running the Application

```bash
# Start the API server
python src/api/main.py

# In another terminal, start the frontend
cd src/frontend
npm install
npm start
```

## Data Requirements

### Transit Model - Critical Data Fields:
1. **vehicle_id & timestamp**: For tracking individual bus movements
2. **route_id & stop_id**: To identify specific route-stop combinations
3. **schedule_deviation**: Actual vs. scheduled arrival time (in seconds)

### Parking Model - Critical Data Fields:
1. **meter_id & timestamp**: For temporal patterns at specific locations
2. **occupancy_status**: Whether spot is occupied or available
3. **transaction_amount & duration**: For pricing optimization

## Ethical Considerations

### Potential Risks:
1. **Algorithmic Bias**: Models may perform worse in underserved neighborhoods with less data
2. **Privacy Concerns**: Location tracking could reveal sensitive movement patterns
3. **Equity Issues**: Dynamic pricing could disadvantage low-income residents

### Mitigation Strategies:
1. **Bias Monitoring**: Regular audits of model performance across neighborhoods
2. **Data Anonymization**: Aggregate data at block level, remove personal identifiers
3. **Equity Controls**: Cap maximum price increases, ensure pricing doesn't disproportionately affect certain areas
4. **Transparency**: Clear communication about how predictions are made

## Development Roadmap

- [ ] Phase 1: Data collection and exploration
- [ ] Phase 2: Transit delay model development
- [ ] Phase 3: Parking prediction model development
- [ ] Phase 4: API development
- [ ] Phase 5: Frontend dashboard
- [ ] Phase 6: Integration and testing
- [ ] Phase 7: Deployment and monitoring

## Contributing

Please read [CONTRIBUTING.md](docs/CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- 511 SF Bay for transit data APIs
- DataSF for open data access
- San Francisco Municipal Transportation Agency (SFMTA)

## Contact

For questions or feedback, please open an issue on GitHub.
