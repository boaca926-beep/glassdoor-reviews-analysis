# Glassdoor Reviews Dataset Analysis

## 📊 Overview
This project analyzes Glassdoor employee review data from the Bright Data sample dataset.

## Data Source
- **Provider**: Fetch free sample dataset of Glassdoor from Bright Data

- **File**: 'glassdoor-companies-reviews.csv'

- **Records**: 1,000+ company reviews

Step 1: Navigate to the GitHub Repository

    Open your web browser

    Go to: https://github.com/luminati-io/Glassdoor-dataset-samples

    This is the official repository for Bright Data's free dataset samples

Step 2: Locate the Dataset File

    On the repository page, you'll see a file listing. Look for: glassdoor-companies-reviews.csv

This is the sample dataset file containing over 1,000 company reviews

## 📈 Analysis Goals
1. What are the most common pros and cons mentioned in Glassdoor reviews?

2. Do former employees rate companies lower than current employees?

3. Is there a correlation between employee tenure and overall rating?

4. Which factors (work-life balance, culture, compensation) most strongly predict overall satisfaction?

5. How does review length relate to helpfulness votes?

## 🔧 Setup

### Prerequisites
- Python 3.8+
- pandas
- uv (package manager)

### Installation
```bash
# Clone the repository
git clone https://github.com/luminati-io/Glassdoor-dataset-samples.git

# Install dependencies
A text file: requiremnts.txt includes all dependiceis. To download the dependencies
uv add -r requirements.txt
```

Example requirements.txt
txt

pandas
numpy

## 🚀 Usage
Convert CSV to JSON
```python
import pandas as pd

# Load the CSV
df = pd.read_csv('glassdoor-companies-reviews.csv')

# Convert to JSON
df.to_json('glassdoor_reviews.json', orient='records', indent=2)

print("✅ Conversion complete!")
```

## 📊 Dataset Fields

The CSV file contains the following fields:

| Field Name | Description | Data Type |
| :--- | :--- | :--- |
| `timestamp` | When the data was collected | DateTime |
| `overview_id` | Internal company identifier | Integer |
| `review_id` | Unique identifier for each review | Integer |
| `review_url` | Direct link to the review on Glassdoor | Text |
| `rating_date` | Date when the review was posted | DateTime |
| `count_helpful` | Number of people who found the review helpful | Integer |
| `count_unhelpful` | Number who found the review unhelpful | Integer |
| `employee_job_end_year` | Year employee left (if former) | Integer |
| `employee_length` | Years employed at the company | Float |
| `employee_status` | Employment status (REGULAR, etc.) | Text |
| `employee_type` | Current/Former employee with tenure | Text |
| `company_name` | Name of the company being reviewed | Text |
| `summary` | Review title/summary | Text |k
| `review_pros` | Positive aspects mentioned | Text |
| `review_cons` | Negative aspects mentioned | Text |
| `review_advice` | Advice given to the company | Text |
| `advice_to_management` | Advice for management | Text |
| `rating_overall` | Overall company rating (1-5) | Float |
| `rating_culture_values` | Culture and values rating | Float |
| `rating_work_life` | Work-life balance rating | Float |
| `rating_compensation_benefits` | Compensation and benefits rating | Float |
| `rating_senior_leadership` | Senior leadership rating | Float |
| `rating_career_opportunities` | Career opportunities rating | Float |
| `flags_ceo_approval` | Whether employee approves of CEO | Text |
| `flags_recommend_frend` | Whether employee would recommend to friend | Text |
| `employee_location` | Employee's location | Text |
| `employee_job_title` | Employee's job title | Text |

## Docker Deployment
### 1. Install Python and uv
```bash
# Download Docker Desktop from:
# https://www.docker.com/products/docker-desktop/
```

### 2. Import the code
```bash
# Clone your repository
git clone https://github.com/boaca926-beep/job-agent.git
cd job-agent
```

## 🚀 Deployment

### Option 1: Local Python (Recommended)
```bash
# 1. Setup Python environment
./setup.sh

# 2. Install Ollama from https://ollama.com

# 3. Pull the LLM model
ollama pull llama3.2

# 4. Run the app
./run.sh
```

### Option 2: Docker
```bash
# 1. Install Docker Desktop

# 2. Deploy with Docker
./deploy.sh

# 3. Run the app inside container
docker-compose exec app python main.py
```

### Option 3: Quick Start
```bash
# Setup and run in one go
uv sync && ollama pull llama3.2 && uv run python main.py
```

