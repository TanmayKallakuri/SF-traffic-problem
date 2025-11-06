# SF Smart Mobility Assistant - Project Summary

## Project Overview

**Name**: SF Smart Mobility Assistant  
**Type**: Proof-of-Concept AI/ML Application  
**Status**: Initial Structure Complete  
**Created**: November 2024

## Deliverables Completed

### 1. ✅ Concept Selection

**Chosen Concepts**: 
- **Primary**: Predictive Transit Performance (Concept 1)
- **Secondary**: Parking Prediction and Pricing Optimization (Concept 3)

**Rationale**: Combining both concepts creates a comprehensive mobility solution that helps users make informed decisions about transit vs. driving.

### 2. ✅ Model Justification

#### Transit Delay Model (Time-Series Regression)
**Why this approach**:
- **Historical Patterns**: Bus delays follow predictable patterns based on time of day, day of week, and route
- **Real-time Integration**: Can incorporate live vehicle positions and recent delays
- **Interpretable**: Easy to explain predictions to users ("Bus will be 5 minutes late based on current traffic")
- **Proven Success**: Time-series methods like ARIMA, Prophet, and LSTM excel at this type of sequential data

**ML Task**: Regression to predict delay in minutes (continuous value)

#### Parking Availability Model (Classification + Regression)
**Why this approach**:
- **Dual Output**: Classification for availability categories (high/medium/low) + regression for exact occupancy rate
- **Pattern Recognition**: Parking occupancy has strong temporal and spatial patterns
- **Dynamic Pricing**: Regression output enables optimization algorithms for pricing recommendations
- **Actionable**: Users get both probability of finding parking AND price recommendations

**ML Tasks**: 
- Classification for availability probability
- Regression for occupancy rate (0-1)
- Optimization for pricing recommendations

### 3. ✅ Key Features

1. **Real-Time Transit Delay Map**
   - Interactive map showing current and predicted delays for all Muni routes
   - Color-coded by severity (green: on-time, yellow: 5-10 min delay, red: >10 min delay)
   - Click any route/stop for detailed 15-minute predictions

2. **Parking Availability Heatmap**
   - Neighborhood-level visualization of parking availability
   - Probability scores and recommended pricing
   - Historical trends and peak hours

3. **Smart Mobility Decision Helper**
   - Compares transit vs. driving options
   - Factors: predicted delay, parking availability, cost, time
   - Personalized recommendations based on origin/destination
   - "Take the bus - 8 min faster and $5 cheaper considering parking"

### 4. ✅ Critical Data Fields

#### Transit Data (511 SF Bay API)
1. **vehicle_id & timestamp**: Track individual bus movements over time for pattern analysis
2. **route_id & stop_id**: Identify specific route-stop combinations with unique delay characteristics
3. **schedule_deviation** (seconds): The target variable - actual vs. scheduled arrival time

#### Parking Data (DataSF API)
1. **meter_id & timestamp**: Temporal patterns at specific locations (morning vs. evening occupancy)
2. **occupancy_status**: Binary indicator of whether spot is occupied (for classification)
3. **transaction_amount & duration**: Calculate occupancy rates and price elasticity for dynamic pricing

### 5. ✅ Ethical Consideration

**Primary Risk**: **Algorithmic Bias Against Underserved Neighborhoods**

**Description**: 
Machine learning models may perform significantly worse in low-income or minority neighborhoods due to:
- Less historical data collection in these areas
- Different transit usage patterns that are underrepresented in training data
- Systematic infrastructure underfunding creating noisier, less predictable patterns
- Result: Less accurate predictions → worse user experience → reinforced inequity

**Mitigation Strategy**:

1. **Performance Monitoring by Geography**
   - Track model accuracy (MAE, RMSE) separately for each neighborhood
   - Flag neighborhoods where performance falls >20% below city average
   - Monthly audit reports with geographic breakdown

2. **Fairness Constraints**
   - Set minimum acceptable performance thresholds for all areas
   - Retrain models with weighted sampling to boost underrepresented neighborhoods
   - Use ensemble methods that combine global and local models

3. **Equitable Data Collection**
   - Prioritize sensor deployment and data collection in underserved areas
   - Partner with community organizations to gather qualitative feedback
   - Active learning to identify and fill data gaps

4. **Transparency & Accountability**
   - Public dashboard showing model performance by neighborhood
   - Community input mechanisms for reporting bias
   - Independent quarterly audits
   - Clear escalation path for addressing disparities

**Implementation**:
```python
def ensure_fairness(predictions, neighborhoods):
    performance_by_area = audit_model_fairness(predictions, neighborhoods)
    
    for area, metrics in performance_by_area.items():
        if metrics['mae'] > CITY_AVERAGE * 1.2:
            # Flag for retraining with boosted sampling
            trigger_model_update(area, boost_factor=2.0)
            log_bias_alert(area, metrics)
```

## Technology Stack

### Backend
- **Language**: Python 3.11+
- **Web Framework**: FastAPI
- **ML Libraries**: scikit-learn, XGBoost, Prophet
- **Data**: pandas, numpy
- **Database**: PostgreSQL (SQLite for development)

### Frontend
- **Framework**: React.js
- **Maps**: Leaflet.js
- **Charts**: Plotly
- **State Management**: React Hooks

### Data Sources
- **Transit**: 511 SF Bay API (GTFS Real-time)
- **Parking**: DataSF Open Data Portal
- **Weather** (optional): OpenWeather API
- **Events** (optional): SF Recreation & Parks

## Project Structure

```
SF-traffic-problem/
├── src/
│   ├── transit/              # Transit delay prediction module
│   │   ├── data_fetcher.py   # 511 API integration
│   │   ├── feature_engineering.py
│   │   └── model.py          # Time-series regression
│   ├── parking/              # Parking prediction module
│   │   ├── data_fetcher.py   # DataSF API integration
│   │   ├── feature_engineering.py
│   │   └── model.py          # Classification + regression
│   └── api/                  # FastAPI backend
│       └── main.py
├── notebooks/                # Jupyter notebooks for exploration
├── tests/                    # Unit and integration tests
├── docs/                     # Documentation including ETHICS.md
└── config/                   # Configuration files
```

## Development Roadmap

### Phase 1: Foundation (Week 1-2)
- ✅ Project structure created
- ✅ Documentation written
- ✅ Git repository initialized
- ⏳ Set up 511 and DataSF API access
- ⏳ Create data collection pipeline

### Phase 2: Data & Features (Week 3-4)
- ⏳ Collect historical transit data
- ⏳ Collect parking transaction data
- ⏳ Implement feature engineering
- ⏳ Exploratory data analysis

### Phase 3: Model Development (Week 5-6)
- ⏳ Train transit delay model
- ⏳ Train parking availability model
- ⏳ Model evaluation and tuning
- ⏳ Bias testing and mitigation

### Phase 4: API & Integration (Week 7-8)
- ⏳ Complete FastAPI endpoints
- ⏳ Add model inference
- ⏳ API testing
- ⏳ Documentation

### Phase 5: Frontend (Week 9-10)
- ⏳ Build React dashboard
- ⏳ Implement maps and visualizations
- ⏳ User testing
- ⏳ Deployment

## Key Files

- **README.md**: Comprehensive project documentation
- **QUICKSTART.md**: Step-by-step setup guide
- **docs/ETHICS.md**: Detailed ethical considerations and mitigation strategies
- **config/config.example.yaml**: Configuration template with API keys
- **requirements.txt**: All Python dependencies
- **tests/test_transit.py**: Example unit tests

## Next Steps

1. **Push to GitHub**: Follow instructions in QUICKSTART.md
2. **Get API Keys**: Register for 511 SF Bay and DataSF accounts
3. **Data Collection**: Start fetching historical data
4. **Use Claude Code**: Continue development with Claude Code for:
   - Data pipeline implementation
   - Model training and tuning
   - API development
   - Frontend creation

## Success Metrics

### Technical Metrics
- Transit delay prediction MAE < 3 minutes
- Parking availability accuracy > 80%
- API response time < 500ms
- Model performance variance across neighborhoods < 20%

### Impact Metrics
- User adoption rate
- Reduction in "cruising for parking" time
- Improved transit reliability perception
- Community satisfaction surveys

## Resources

- **511 Developer Portal**: https://511.org/open-data/token
- **DataSF**: https://datasf.org/opendata/
- **Project Repository**: (to be added after GitHub push)

## Contact & Support

For questions or contributions, please open an issue on GitHub or refer to the documentation.

---

**Note**: This is a proof-of-concept application. Production deployment would require additional security hardening, performance optimization, and compliance review.
