import os
import logging
from typing import Dict, Optional
from job_matcher import JobMatcher
from skill_analyzer import SkillAnalyzer

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_basic_functionality():
    """Test basic functionality without ML components"""
    try:
        # Initialize components
        job_matcher = JobMatcher()
        skill_analyzer = SkillAnalyzer()
        
        # Test data
        resume_text = """
        Senior Software Engineer with 8 years of experience in Python and web development.
        - Proficient in Python, JavaScript, React, and Node.js
        - Experience with Docker, Kubernetes, and AWS
        - Led team of 5 developers on a microservices migration project
        - Implemented CI/CD pipelines using Jenkins
        """
        
        job_description = """
        Looking for a Senior Software Engineer with:
        - Strong Python and JavaScript experience
        - Experience with React and modern frontend frameworks
        - DevOps experience with Docker and Kubernetes
        - AWS cloud experience
        - Leadership skills and experience managing teams
        """
        
        # Test job matching
        match_scores = job_matcher.calculate_match_score(resume_text, job_description)
        print("\nMatch Scores:")
        print(f"Overall Match Score: {match_scores.get('match_score')}%")
        print(f"Keyword Similarity: {match_scores.get('keyword_similarity')}%")
        print(f"Text Similarity: {match_scores.get('text_similarity')}%")
        print(f"Skill Match: {match_scores.get('skill_match')}%")
        print(f"Matched Keywords: {', '.join(match_scores.get('matched_keywords', []))}")
        
        # Test skill analysis
        skill_analysis = skill_analyzer.analyze_skills(resume_text, job_description)
        print("\nSkill Analysis:")
        if isinstance(skill_analysis, dict):
            print("\nResume Skills:")
            for category, skills in skill_analysis.get('resume_skills', {}).items():
                print(f"{category}: {', '.join(skills)}")
            
            print("\nMatched Skills:", ', '.join(skill_analysis.get('matched_skills', [])))
            print("Missing Skills:", ', '.join(skill_analysis.get('missing_skills', [])))
        
        # Enhancement suggestions
        enhancements = job_matcher.enhance_resume_with_ai(resume_text, job_description)
        print("\nEnhancement Suggestions:")
        print(enhancements.split("--- AI Enhancement Suggestions ---")[1])
        
        return True
        
    except Exception as e:
        logger.error(f"Error in basic functionality test: {str(e)}")
        return False

if __name__ == "__main__":
    print("Testing basic functionality without ML components...")
    success = test_basic_functionality()
    print(f"\nTest {'succeeded' if success else 'failed'}")