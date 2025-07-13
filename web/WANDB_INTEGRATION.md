# Weights & Biases (wandb.ai) Integration

This document explains the Weights & Biases integration for tracking and monitoring your Twitter scraper performance and AI reply generation.

## Overview

Weights & Biases is integrated to provide:
- **Real-time Monitoring**: Track application usage and performance
- **AI Metrics**: Monitor Claude.ai reply generation quality and usage
- **Search Analytics**: Analyze Twitter search patterns and success rates
- **Business Intelligence**: Track how business configuration affects results
- **Error Tracking**: Monitor failures and debug issues

## Setup

### 1. API Key Configuration

Your wandb API key is already configured in the system:
```
API Key: 0f7450b47352bca1e22df7df6a502a508c7de615
```

### 2. Environment Variables

Set these in your environment or `.env` file:
```bash
WANDB_API_KEY=0f7450b47352bca1e22df7df6a502a508c7de615
WANDB_PROJECT=freemasonry-twitter-scraper
WANDB_ENTITY=your_wandb_username  # Optional
```

### 3. Installation

```bash
pip install wandb>=0.15.0
```

## Tracked Metrics

### 📊 Search Operations
- `search_successful`: Successful tweet searches
- `search_failed`: Failed tweet searches
- `tweets_found`: Number of tweets returned per search
- `search_query`: Search terms used
- `search_limit`: Tweet limit per search
- `search_product`: Search type (Latest, Top, Media)

### 🤖 AI Reply Generation
- `reply_generated`: Successful reply generations
- `reply_generation_failed`: Failed reply generations
- `reply_length`: Character count of generated replies
- `business_tone`: Tone setting used (professional, friendly, etc.)
- `business_industry`: Industry setting
- `original_tweet_length`: Length of original tweet
- `claude_model`: AI model used

### 👥 Account Management
- `account_added`: New Twitter accounts added
- `account_username`: Username of added accounts
- `has_cookies`: Whether cookies were used for authentication

### ⚙️ Business Configuration
- `business_context_updated`: Configuration changes
- `company_name`: Business name
- `industry`: Business industry
- `tone`: Reply tone setting

### 📈 Session Statistics
- `total_requests`: Total API requests
- `successful_searches`: Cumulative successful searches
- `failed_searches`: Cumulative failed searches
- `accounts_added`: Total accounts added
- `replies_generated`: Total replies generated

## Dashboard Features

### Real-time Monitoring
Access your live dashboard at: https://wandb.ai/[your-username]/freemasonry-twitter-scraper

### Key Visualizations
1. **Search Performance**: Success/failure rates over time
2. **Reply Generation Metrics**: AI performance and character counts
3. **Usage Patterns**: Peak usage times and request volumes
4. **Error Analysis**: Failure patterns and error types
5. **Business Intelligence**: How configuration affects performance

### Custom Charts
Create custom visualizations for:
- Reply quality trends
- Search query analysis
- Account performance
- Business metric correlations

## API Endpoints

### Get wandb Metrics
```
GET /api/wandb/metrics
```
Returns current run information and dashboard URL.

### Enhanced Stats
```
GET /api/stats
```
Returns application statistics and logs them to wandb.

### Health Check
```
GET /api/health
```
Includes wandb initialization status.

## Best Practices

### 1. Monitor Key Metrics
- Track reply generation success rates
- Monitor search performance trends
- Watch for error patterns

### 2. Analyze Business Impact
- Correlate business settings with reply quality
- Track engagement metrics over time
- Optimize based on wandb insights

### 3. Performance Optimization
- Use wandb data to identify bottlenecks
- Monitor API usage costs
- Track system resource usage

### 4. Error Investigation
- Use wandb logs to debug failures
- Track error patterns and frequencies
- Monitor system health over time

## Troubleshooting

### Common Issues

**"wandb not initialized" Error**
1. Check API key is set correctly
2. Verify internet connection
3. Restart the application
4. Check wandb service status

**No Data in Dashboard**
1. Ensure API key is valid
2. Check project permissions
3. Verify metrics are being logged
4. Refresh the dashboard

**Performance Issues**
1. Reduce logging frequency if needed
2. Check wandb service latency
3. Monitor local resource usage

### Debug Information

Check the application logs for:
```
INFO: Weights & Biases initialized successfully
```

Verify status via health endpoint:
```bash
curl http://localhost:5000/api/health
```

## Data Privacy & Security

### Data Logged to wandb
- Application metrics and performance data
- Search queries (for analytics)
- Business configuration (company name, industry)
- Error messages and debugging information

### Data NOT Logged
- Tweet content (for privacy)
- User passwords or sensitive credentials
- Personal identifying information

### Security Measures
- API keys are handled securely
- Sensitive data is filtered before logging
- Communication uses HTTPS encryption

## Advanced Configuration

### Custom Metrics
Add custom tracking in your code:
```python
if self.wandb_initialized:
    wandb.log({
        "custom_metric": value,
        "timestamp": datetime.now().timestamp()
    })
```

### Experiment Tracking
- Tag different configurations
- Compare performance across changes
- Track A/B test results

### Integration with CI/CD
- Automate metric collection
- Track deployment performance
- Monitor production health

## Support

### Resources
- Weights & Biases Documentation: https://docs.wandb.ai/
- Community Support: https://community.wandb.ai/
- API Reference: https://docs.wandb.ai/ref/python/

### Getting Help
1. Check the wandb logs in your application
2. Verify your API key and permissions
3. Review the wandb dashboard for insights
4. Contact wandb support if needed

### Project Information
- **Project Name**: freemasonry-twitter-scraper
- **Tags**: twitter, scraping, ai-replies, freemasonry
- **Metrics**: Real-time tracking of all application operations

The wandb integration provides comprehensive monitoring and analytics for your Twitter scraper, helping you optimize performance and track business impact over time.