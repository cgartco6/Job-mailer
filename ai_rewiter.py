import time
from transformers import pipeline
from config import config

# Initialize AI models
try:
    paraphraser = pipeline("text2text-generation", model="t5-small")
    ner_extractor = pipeline("ner", model="dslim/bert-base-NER")
except Exception as e:
    print(f"Error loading models: {e}")
    # Fallback: define models as None? But the functions will fail. We'll handle in rewrite_cv.

def rewrite_cv(job_description):
    """AI-powered CV customization using NER and paraphrasing"""
    # Load base CV
    try:
        with open(config.BASE_CV_PATH, 'r') as f:
            base_cv = f.read()
    except Exception as e:
        print(f"Error reading base CV: {e}")
        return ""
    
    # Extract key skills from job description
    job_skills = []
    if ner_extractor:
        try:
            entities = ner_extractor(job_description)
            job_skills = [entity['word'] for entity in entities if entity['entity'] in ['B-TECH', 'I-TECH']]
        except Exception as e:
            print(f"NER extraction failed: {e}")
    else:
        print("NER model not available")
    
    # Customize CV using AI
    for attempt in range(config.RESUME_RETRY_LIMIT):
        try:
            prompt = f"Customize this resume for a job requiring: {', '.join(job_skills)}\n\n{base_cv}"
            customized_cv = paraphraser(prompt, max_length=1024)[0]['generated_text']
            return customized_cv
        except Exception as e:
            print(f"CV rewrite error (attempt {attempt+1}): {str(e)}")
            time.sleep(2)
    return base_cv  # Fallback to original

def generate_cover_letter(job_info):
    """Generate AI-powered cover letter"""
    try:
        with open(config.BASE_COVER_LETTER, 'r') as f:
            base_letter = f.read()
    except Exception as e:
        print(f"Error reading cover letter template: {e}")
        return ""
    
    for attempt in range(config.RESUME_RETRY_LIMIT):
        try:
            prompt = f"Write a cover letter for {job_info['title']} position at {job_info['company']}:\n\n{base_letter}"
            cover_letter = paraphraser(prompt, max_length=512)[0]['generated_text']
            return cover_letter
        except Exception as e:
            print(f"Cover letter generation error (attempt {attempt+1}): {str(e)}")
            time.sleep(2)
    return base_letter  # Fallback to original
