# Quick Start Guide - SF Smart Mobility Assistant

## Overview

This project combines two AI-powered solutions for San Francisco:
1. **Transit Delay Prediction** - Predicts Muni bus delays using time-series regression
2. **Parking Availability Prediction** - Forecasts parking availability and suggests optimal pricing

## Initial Setup

### 1. Push to GitHub

```bash
cd SF-traffic-problem

# Add your GitHub remote
git remote add origin https://github.com/YOUR_USERNAME/SF-traffic-problem.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### 2. Set Up Development Environment

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure API Keys

```bash
# Copy example config
cp config/config.example.yaml config/config.yaml

# Edit config.yaml and add your API keys:
# - 511 SF Bay API key (get from https://511.org/open-data/token)
# - DataSF API key (optional, most endpoints are open)
```

## Next Steps with Claude Code

Once you've pushed this to GitHub, you can use Claude Code to continue development:

```bash
# Start Claude Code
claude-code

# In Claude Code, you can:
# 1. Fetch data from APIs
# 2. Build out the data pipeline
# 3. Train the ML models
# 4. Develop the FastAPI backend
# 5. Create the frontend dashboard
```

## Development Workflow

### Phase 1: Data Collection (Week 1)
- [ ] Set up 511 API data fetching
- [ ] Set up DataSF parking data fetching
- [ ] Create data cleaning pipeline
- [ ] Store raw data in `data/raw/`

### Phase 2: Feature Engineering (Week 2)
- [ ] Implement temporal features
- [ ] Create lag features
- [ ] Add location-based features
- [ ] Save processed data in `data/processed/`

### Phase 3: Model Training (Week 3)
- [ ] Train transit delay model
- [ ] Train parking availability model
- [ ] Evaluate and tune models
- [ ] Save models in `data/models/`

### Phase 4: API Development (Week 4)
- [ ] Complete FastAPI endpoints
- [ ] Add model inference
- [ ] Test API endpoints
- [ ] Add error handling

### Phase 5: Frontend (Week 5)
- [ ] Create React dashboard
- [ ] Add interactive maps
- [ ] Implement visualizations
- [ ] User testing

## Key Features to Implement

### Transit Module
- Real-time delay predictions
- Historical performance analytics
- Route comparison
- Interactive delay map

### Parking Module
- Availability heatmap
- Price recommendations
- Occupancy forecasting
- Neighborhood comparisons

### Decision Helper
- "Should I drive or take transit?" recommendation
- Combined cost analysis
- Time comparison

## Testing

```bash
# Run tests
pytest tests/

# Run with coverage
pytest --cov=src tests/
```

## API Usage Examples

### Get Transit Delay Prediction

```bash
curl -X POST "http://localhost:8000/api/v1/transit/predict" \
  -H "Content-Type: application/json" \
  -d '{"route_id": "14", "stop_id": "5184"}'
```

### Get Parking Availability

```bash
curl -X POST "http://localhost:8000/api/v1/parking/availability" \
  -H "Content-Type: application/json" \
  -d '{"neighborhood": "Mission"}'
```

## Project Structure

```
SF-traffic-problem/
├── src/
│   ├── transit/         # Transit delay prediction
│   ├── parking/         # Parking availability prediction
│   ├── api/            # FastAPI backend
│   └── frontend/       # React dashboard
├── data/
│   ├── raw/            # Raw data from APIs
│   ├── processed/      # Cleaned data
│   └── models/         # Trained ML models
├── notebooks/          # Jupyter notebooks
├── tests/             # Unit tests
└── docs/              # Documentation
```

## Important Notes

### Ethical Considerations
- Review `docs/ETHICS.md` before deployment
- Implement bias monitoring from day one
- Cap price increases at 50%
- Ensure equitable performance across neighborhoods

### Data Privacy
- Aggregate all data at block level minimum
- Implement data retention policies (90 days)
- Use encryption for sensitive data
- Follow GDPR/CCPA guidelines

### API Rate Limits
- 511 API: Check your tier limits
- DataSF: Most endpoints are open but may have limits
- Implement caching to reduce API calls

## Resources

- **511 SF Bay API**: https://511.org/open-data/token
- **DataSF Open Data**: https://datasf.org/opendata/
- **SFMTA**: https://www.sfmta.com/
- **Prophet Documentation**: https://facebook.github.io/prophet/
- **FastAPI Documentation**: https://fastapi.tiangolo.com/

## Getting Help

- Open an issue on GitHub
- Check the documentation in `docs/`
- Review the example notebooks in `notebooks/`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## License

MIT License - see LICENSE file for details
