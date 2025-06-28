import requests
import time
from bs4 import BeautifulSoup
from config import config

def get_job_description(job_url):
    """Extract full job description from detail page"""
    try:
        response = requests.get(job_url, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        job_description = soup.select_one('#jobDescriptionText')
        return job_description.text.strip() if job_description else ""
    except Exception as e:
        print(f"Error getting job description: {e}")
        return ""

def scrape_indeed_jobs():
    """Scrape Indeed jobs using BeautifulSoup"""
    jobs = []
    try:
        base_url = "https://www.indeed.com/jobs"
        params = {
            'q': ' '.join(config.TARGET_JOBS),
            'l': config.LOCATION,
        }
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
        
        response = requests.get(base_url, params=params, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        job_cards = soup.select('.jobsearch-SerpJobCard')
        for job_card in job_cards:
            title_elem = job_card.select_one('.title a')
            title = title_elem.text.strip() if title_elem else ""
            company_elem = job_card.select_one('.company')
            company = company_elem.text.strip() if company_elem else ""
            job_url = "https://www.indeed.com" + title_elem['href'] if title_elem else ""
            
            if not job_url:
                continue
                
            # Get job description
            time.sleep(config.SCRAPE_DELAY)  # Be polite
            description = get_job_description(job_url)
            
            jobs.append({
                "title": title,
                "company": company,
                "url": job_url,
                "description": description
            })
    except Exception as e:
        print(f"Scraping error: {str(e)}")
    return jobs

# Note: Indeed might block scrapers. Consider using proxies or alternative sources in production.
