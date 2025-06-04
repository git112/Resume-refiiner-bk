import re
import logging
from typing import Dict, List, Set
from collections import defaultdict

logger = logging.getLogger(__name__)

class SkillAnalyzer:
    """Analyzes and categorizes skills from resumes and job descriptions"""
    
    def __init__(self):
        # Initialize skill categories and their associated keywords
        self.skill_categories = {
            'programming_languages': {
                'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'php', 'ruby', 'go',
                'rust', 'swift', 'kotlin', 'scala', 'r', 'matlab', 'sql', 'perl', 'haskell'
            },
            'web_technologies': {
                'html', 'css', 'sass', 'less', 'react', 'angular', 'vue', 'node.js', 'express',
                'django', 'flask', 'spring', 'laravel', 'jquery', 'bootstrap', 'webpack', 'gatsby'
            },
            'databases': {
                'mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch', 'oracle', 'sqlite',
                'cassandra', 'dynamodb', 'neo4j', 'mariadb', 'couchdb', 'firebase'
            },
            'cloud_devops': {
                'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins', 'gitlab', 'github actions',
                'terraform', 'ansible', 'chef', 'puppet', 'circleci', 'nginx', 'apache'
            },
            'data_science_ml': {
                'machine learning', 'deep learning', 'tensorflow', 'pytorch', 'scikit-learn',
                'pandas', 'numpy', 'matplotlib', 'keras', 'opencv', 'nlp', 'computer vision'
            },
            'soft_skills': {
                'leadership', 'communication', 'teamwork', 'problem solving', 'project management',
                'analytical', 'time management', 'creativity', 'collaboration', 'adaptability'
            }
        }
        
        # Flatten skills for quick lookup
        self.all_skills = set()
        for skills in self.skill_categories.values():
            self.all_skills.update(skills)
    
    def analyze_skills(self, resume_text: str, job_description: str = None) -> Dict[str, List[str]]:
        """Analyze and categorize skills found in the text"""
        try:
            # Normalize text
            text_lower = resume_text.lower()
            found_skills = defaultdict(list)
            
            # Find skills by category
            for category, skills in self.skill_categories.items():
                for skill in skills:
                    # Use word boundary check for more accurate matching
                    if re.search(r'\b' + re.escape(skill) + r'\b', text_lower):
                        found_skills[category].append(skill)
            
            # If job description is provided, also analyze skill matches
            if job_description:
                job_skills = defaultdict(list)
                job_lower = job_description.lower()
                
                # Find skills in job description
                for category, skills in self.skill_categories.items():
                    for skill in skills:
                        if re.search(r'\b' + re.escape(skill) + r'\b', job_lower):
                            job_skills[category].append(skill)
                
                matched_skills = []
                missing_skills = []
                
                for category, skills in job_skills.items():
                    resume_skills = set(found_skills.get(category, []))
                    job_skill_set = set(skills)
                    
                    matched = resume_skills & job_skill_set
                    missing = job_skill_set - resume_skills
                    
                    matched_skills.extend(matched)
                    missing_skills.extend(missing)
                
                # Create comprehensive analysis result
                result = {
                    'resume_skills': {
                        category: sorted(skills)
                        for category, skills in found_skills.items()
                    },
                    'job_skills': {
                        category: sorted(skills)
                        for category, skills in job_skills.items()
                    },
                    'matched_skills': sorted(matched_skills),
                    'missing_skills': sorted(missing_skills),
                    'skill_match_percentage': len(matched_skills) / max(len(set().union(*[set(skills) for skills in job_skills.values()])), 1) * 100
                }
            else:
                # If no job description, just return the skills found
                result = {
                    category: sorted(skills)
                    for category, skills in found_skills.items()
                }
            
            return result
            
        except Exception as e:
            logger.error(f"Error analyzing skills: {str(e)}")
            return {}
    
    def get_skill_gap(self, resume_text: str, job_description: str) -> Dict[str, List[str]]:
        """Identify missing skills by comparing resume with job description"""
        try:
            # Get skills from both texts
            resume_skills = self.analyze_skills(resume_text)
            job_skills = self.analyze_skills(job_description)
            
            # Find missing skills by category
            skill_gaps = {}
            
            for category in self.skill_categories.keys():
                resume_set = set(resume_skills.get(category, []))
                job_set = set(job_skills.get(category, []))
                
                missing_skills = job_set - resume_set
                if missing_skills:
                    skill_gaps[category] = sorted(missing_skills)
            
            return skill_gaps
            
        except Exception as e:
            logger.error(f"Error calculating skill gap: {str(e)}")
            return {}
    
    def get_skill_match_percentage(self, resume_skills: Dict[str, List[str]], job_skills: Dict[str, List[str]]) -> float:
        """Calculate the percentage of job skills matched in the resume"""
        try:
            total_job_skills = 0
            matched_skills = 0
            
            for category, skills in job_skills.items():
                total_job_skills += len(skills)
                if category in resume_skills:
                    resume_set = set(resume_skills[category])
                    job_set = set(skills)
                    matched_skills += len(resume_set & job_set)
            
            if total_job_skills == 0:
                return 0.0
                
            return round((matched_skills / total_job_skills) * 100, 2)
            
        except Exception as e:
            logger.error(f"Error calculating skill match percentage: {str(e)}")
            return 0.0
    
    def get_skill_suggestions(self, missing_skills: Dict[str, List[str]], num_suggestions: int = 5) -> List[str]:
        """Generate prioritized skill improvement suggestions"""
        try:
            suggestions = []
            priority_categories = ['programming_languages', 'web_technologies', 'cloud_devops', 'data_science_ml']
            
            # First add high-priority category skills
            for category in priority_categories:
                if category in missing_skills:
                    skills = missing_skills[category]
                    suggestions.extend([
                        f"Consider learning {skill} to improve your {category.replace('_', ' ')} skills"
                        for skill in skills[:2]  # Limit to top 2 from each category
                    ])
            
            # Then add remaining skills until we reach num_suggestions
            if len(suggestions) < num_suggestions:
                remaining_categories = [cat for cat in missing_skills.keys() if cat not in priority_categories]
                for category in remaining_categories:
                    if len(suggestions) >= num_suggestions:
                        break
                    skills = missing_skills[category]
                    suggestions.extend([
                        f"Consider adding {skill} to your skillset"
                        for skill in skills[:1]  # Limit to top 1 from non-priority categories
                    ])
            
            return suggestions[:num_suggestions]
            
        except Exception as e:
            logger.error(f"Error generating skill suggestions: {str(e)}")
            return []