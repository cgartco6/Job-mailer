import time
from job_scraper import scrape_indeed_jobs
from ai_rewriter import rewrite_cv, generate_cover_letter
from email_sender import send_application
from config import config
from utils import setup_logger

logger = setup_logger()

def main():
    """Main automation workflow"""
    logger.info("Starting job search automation")
    
    # Step 1: Scrape jobs
    logger.info(f"Scraping jobs for: {config.TARGET_JOBS} in {config.LOCATION}")
    jobs = scrape_indeed_jobs()
    logger.info(f"Found {len(jobs)} jobs")
    
    for job in jobs:
        logger.info(f"Processing: {job['title']} at {job['company']}")
        
        # Step 2: AI customization
        logger.info("Rewriting CV...")
        custom_cv = rewrite_cv(job['description'])
        
        logger.info("Generating cover letter...")
        cover_letter = generate_cover_letter(job)
        
        # Step 3: Send application
        # Note: We don't have the email in the job info from scraping. 
        # In a real system, we would need to extract it or use an application form.
        # For now, we skip sending. We can print to console.
        logger.info("Skipping email send (email extraction not implemented).")
        # Uncomment below when you have the email
        # if send_application(job, custom_cv, cover_letter):
        #     logger.info("Application successful")
        # else:
        #     logger.warning("Application failed")
        
        # Be polite between job applications
        time.sleep(config.SCRAPE_DELAY)
    
    logger.info("Job automation completed")

if __name__ == "__main__":
    main()
