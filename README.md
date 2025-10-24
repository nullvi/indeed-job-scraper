# Indeed Job Listings Scraper

A professional, production-ready web scraper built with Python and Selenium that automatically extracts job listing data from Indeed.com with advanced anti-bot detection features.

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Selenium](https://img.shields.io/badge/Selenium-4.15.2-green.svg)](https://www.selenium.dev/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## Project Overview

This scraper was developed to demonstrate advanced web scraping capabilities, including:
- Automated pagination across multiple pages
- Anti-bot detection mechanisms to bypass Cloudflare and other protections
- Human-like behavior simulation with random delays and scrolling
- Robust error handling and data extraction with multiple fallback methods
- Clean, well-documented, and maintainable code

**Perfect for:** Job market research, competitor analysis, recruitment data collection, and job aggregation platforms.

---

## Key Features

### Data Extraction
- **Job Title** - Complete position name
- **Company Name** - Hiring organization
- **Location** - Job location/remote status
- **Job URL** - Direct link to full job posting

### Advanced Capabilities
- **Anti-Bot Detection** - Bypasses Cloudflare, CORS, and bot protection systems
- **Automatic Pagination** - Seamlessly navigates through multiple result pages
- **Configurable Limits** - Easily control the number of pages to scrape
- **Human Behavior Simulation** - Random delays, scrolling, and realistic user patterns
- **Robust Error Handling** - Multiple fallback methods for reliable data extraction
- **JSON Export** - Clean, structured data output ready for analysis
- **Zero Manual Setup** - Selenium Manager handles WebDriver automatically

---

## Technology Stack

- **Python 3.8+** - Core programming language
- **Selenium 4.15.2** - Browser automation framework
- **Chrome WebDriver** - Automated via Selenium Manager (no manual installation needed)
- **Random Module** - For human-like behavior simulation
- **JSON** - Data storage and export

---

## Installation

### Prerequisites
- Python 3.8 or higher
- Google Chrome browser

### Setup

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/indeed-job-scraper.git
cd indeed-job-scraper
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

**That's it!** Selenium 4.15.2 includes Selenium Manager which automatically downloads and manages Chrome WebDriver. No manual driver installation needed!

---

## Usage

### Basic Usage

Simply run the script:
```bash
python main.py
```

### Configuration

Configure the scraper by editing the `MAX_PAGES` variable at the top of `main.py`:

```python
# Scrape first 10 pages (default)
MAX_PAGES = 10

# Scrape first 5 pages
MAX_PAGES = 5

# Scrape ALL available pages (no limit)
MAX_PAGES = None
```

### Custom Search URL

Modify the URL in `main.py` to search for different positions or locations:

```python
# Example URLs:
url = "https://www.indeed.com/jobs?q=data+scientist&l=New+York"
url = "https://www.indeed.com/jobs?q=python+developer&l=Remote"
url = "https://www.indeed.com/jobs?q=software+engineer&l=San+Francisco"
```

---

## Output

The scraper generates a `job_listings.json` file with structured data:

```json
[
  {
    "title": "Senior Software Engineer",
    "company": "Tech Company Inc.",
    "location": "San Francisco, CA",
    "link": "https://www.indeed.com/viewjob?jk=..."
  },
  {
    "title": "Data Scientist",
    "company": "Analytics Corp",
    "location": "Remote",
    "link": "https://www.indeed.com/viewjob?jk=..."
  }
]
```

**Data is ready for:**
- Data analysis and visualization
- Database import
- API integration
- Machine learning models
- Market research reports

---

## Anti-Bot Detection Features

This scraper includes professional-grade anti-detection mechanisms:

| Feature | Description |
|---------|-------------|
| **Hidden WebDriver Property** | Makes browser undetectable to JavaScript checks |
| **Realistic User-Agent** | Mimics genuine Chrome browser requests |
| **Random Delays** | Variable wait times (6-9 seconds) between page loads |
| **Human-like Scrolling** | Simulates natural reading behavior |
| **Extended Timeouts** | Allows Cloudflare verification (8+ seconds) |
| **CORS Bypass** | Handles cross-origin request restrictions |

### Handling Rate Limits

If you encounter Cloudflare or CORS issues:

1. **Increase wait times** (line 81 in `main.py`):
```python
time.sleep(15)  # Increase from 8 to 15 seconds
```

2. **Reduce pages per session**:
```python
MAX_PAGES = 5  # Scrape fewer pages
```

3. **Run during off-peak hours** for better success rates

---

## How It Works

### Workflow

```
1. Initialize Chrome with anti-detection settings
2. Navigate to Indeed search URL
3. Wait for Cloudflare verification
4. Simulate human behavior (scrolling)
5. Extract job listings from current page
6. Click "Next Page" button
7. Repeat until page limit reached or last page
8. Save all data to JSON file
```

### Data Extraction Methods

The scraper uses a **cascade approach** with multiple fallback methods:

1. **Primary**: `data-testid` attributes (most reliable)
2. **Secondary**: CSS selectors
3. **Tertiary**: XPath queries
4. **Quaternary**: JavaScript DOM queries
5. **Fallback**: Element iteration and filtering

This ensures **maximum reliability** even when Indeed updates their HTML structure.

---

## Use Cases

This scraper is ideal for:

- **Job Market Research** - Analyze hiring trends and salary data
- **Recruitment Analytics** - Track competitor hiring patterns
- **Resume Optimization** - Identify common skill requirements
- **Job Aggregation** - Build job board platforms
- **Market Intelligence** - Monitor industry demand
- **Job Alert Systems** - Create custom notification services

---

## Important Notes

- Respect Indeed's [Terms of Service](https://www.indeed.com/legal)
- Use reasonable scraping intervals to avoid overloading servers
- This tool is for educational and research purposes
- Consider Indeed's [API](https://www.indeed.com/publisher) for commercial use
- Implement proper data storage and privacy measures for production use

---

## Skills Demonstrated

This project showcases:
- Advanced web scraping techniques
- Anti-bot detection bypass strategies
- Browser automation with Selenium
- Error handling and fault tolerance
- Clean code architecture and documentation
- Data extraction and JSON serialization
- Pagination and dynamic content handling
- Configuration management

---

## Future Enhancements

Potential improvements for production use:
- [ ] Database integration (PostgreSQL, MongoDB)
- [ ] Multi-threading for faster scraping
- [ ] Proxy rotation for IP management
- [ ] Email notifications for completed scrapes
- [ ] RESTful API wrapper
- [ ] Docker containerization
- [ ] Scheduled scraping with cron jobs
- [ ] Data deduplication and validation
- [ ] Support for multiple job sites (LinkedIn, Glassdoor)

---

## Contact

For custom scraping solutions, data collection projects, or automation development:

- **Upwork**: https://www.upwork.com/freelancers/~01932d17f8a62f3413?viewMode=1
- **Email**: drmzulvi@gmail.com
- **LinkedIn**: https://www.linkedin.com/in/ulvi-durmaz-119814303/
- **GitHub**: https://github.com/nullvi

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- Built with [Selenium](https://www.selenium.dev/)
- Inspired by real-world data collection challenges
- Developed as a portfolio demonstration project

---

**If you find this project useful, please consider giving it a star!**

*Note: This scraper is for educational and portfolio demonstration purposes. Always ensure compliance with website terms of service and applicable laws when scraping data.*
