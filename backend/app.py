from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sys
import traceback
import logging
from werkzeug.utils import secure_filename
import tempfile
import json
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file (for API keys)
load_dotenv()

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import our modules
from resume_processor import ResumeProcessor
from job_matcher import JobMatcher
from skill_analyzer import SkillAnalyzer
from report_generator import ReportGenerator
# from scoring_api import scoring_api  # Import our new scoring API blueprint
from hybrid_score_engine import HybridScoreEngine  # Import hybrid scoring engine

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/resume_refiner_app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Register blueprints
# app.register_blueprint(scoring_api, url_prefix='/api')

# Configuration
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'txt', 'docx', 'doc'}

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize processors
resume_processor = ResumeProcessor()
job_matcher = JobMatcher()
skill_analyzer = SkillAnalyzer()
report_generator = ReportGenerator()

# Initialize hybrid scoring engine
score_engine = HybridScoreEngine(os.getenv("GROQ_API_KEY"))

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })

def get_enhanced_llm_analysis(resume_text, job_description, ats_score, match_score, skill_analysis):
    """Get enhanced LLM analysis with fallback for rate limits"""
    try:
        llm_analysis = llm_engine.analyze_resume(resume_text, job_description)
        
        # Generate enhanced score matrix
        score_matrix = llm_engine.analyze_score_matrix(
            resume_text, 
            job_description, 
            ats_score,
            match_score,
            skill_analysis
        )
        return llm_analysis, score_matrix, None
    except ValueError as ve:
        # Check if it's a rate limit error
        if "Rate limit exceeded" in str(ve):
            logger.warning("Rate limit error detected, providing basic analysis without enhanced LLM features")
            # Provide a simplified version without failing the entire request
            llm_analysis = {
                "strengths": ["Processed without enhanced AI analysis due to rate limiting"],
                "improvement_areas": ["Consider trying again later for enhanced analysis"],
                "action_insights": ["Continue with basic analysis for now"],
                "overall_impression": "Analysis completed with limited AI enhancement due to service limitations",
                "match_score": ats_score
            }
            
            # Create a basic score matrix
            score_matrix = {
                "score_matrix": {
                    "overall_score": {
                        "score": (ats_score + match_score) / 2,
                        "analysis": "Basic scoring without enhanced AI analysis"
                    }
                },
                "key_strengths": ["Basic analysis due to rate limiting"],
                "improvement_opportunities": ["Try again later for enhanced analysis"],
                "action_insights": ["Continue with basic analysis"]
            }
            return llm_analysis, score_matrix, "Rate limit exceeded. Using basic analysis."
        else:
            # For other value errors, return the error
            return None, None, str(ve)
    except Exception as e:
        # Log the error
        logger.error(f"LLM analysis error: {str(e)}")
        return None, None, str(e)

@app.route('/api/analyze-resume', methods=['POST'])
def analyze_resume():
    """Main endpoint for resume analysis with intelligent fallback"""
    try:
        # Extract resume text from file or form
        resume_text = None
        job_description = request.form.get('job_description', '')
        
        if 'resume_file' in request.files:
            file = request.files['resume_file']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                resume_text = resume_processor.process_resume(filepath)
                os.remove(filepath)  # Clean up
            else:
                return jsonify({'error': 'Invalid file format'}), 400
        elif 'resume_text' in request.form:
            resume_text = request.form.get('resume_text')
        else:
            return jsonify({'error': 'No resume provided'}), 400
        
        # Validate inputs
        if not resume_text or not resume_text.strip():
            return jsonify({'error': 'Resume text is empty'}), 400
        if not job_description or not job_description.strip():
            return jsonify({'error': 'Job description is required'}), 400
        
        # Extract keywords and analyze skills
        job_keywords = job_matcher.extract_keywords(job_description)
        skill_analysis = skill_analyzer.analyze_skills(resume_text, job_description)
        
        # Perform analysis using hybrid engine
        analysis_results = score_engine.analyze_resume(resume_text, job_keywords)
        
        # Log analysis method for monitoring
        logger.info(f"Analysis completed using {analysis_results['analysis_method']} method")
        
        # Generate comprehensive recommendations
        recommendations = generate_recommendations(
            skill_analysis, 
            analysis_results['rule_based_score'],
            analysis_results.get('llm_analysis', {}).get('improvement_areas', [])
        )
        
        # Prepare unified response
        response = {
            'ats_score': analysis_results['rule_based_score'],
            'match_score': analysis_results['score'],
            'skill_analysis': skill_analysis,
            'job_keywords': job_keywords,
            'llm_analysis': analysis_results.get('llm_analysis', {}),
            'score_matrix': {
                'score_matrix': {
                    'ats_score': {
                        'score': analysis_results['rule_based_score'],
                        'analysis': "Based on ATS compatibility analysis",
                        'strengths': recommendations.get('strengths', []),
                        'weaknesses': recommendations.get('weaknesses', []),
                        'action_items': recommendations.get('action_items', [])
                    },
                    'match_score': {
                        'score': analysis_results['score'],
                        'analysis': f"Based on {analysis_results['analysis_method']} analysis",
                        'strengths': analysis_results.get('llm_analysis', {}).get('strengths', []),
                        'improvement_areas': analysis_results.get('llm_analysis', {}).get('improvement_areas', []),
                        'action_insights': analysis_results.get('llm_analysis', {}).get('action_insights', [])
                    }
                }
            },
            'analysis_method': analysis_results['analysis_method'],
            'analysis_timestamp': datetime.now().isoformat()
        }
        
        return jsonify(response)
    except Exception as e:
        logger.error(f"Error in analyze_resume: {str(e)}", exc_info=True)
        return jsonify({
            'error': 'Resume analysis failed. Please try again.',
            'details': str(e) if app.debug else None
        }), 500

@app.route('/api/generate-report', methods=['POST'])
def generate_report():
    """Generate PDF report"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Generate PDF report
        report_path = report_generator.generate_pdf_report(data)
        
        # Return file path or base64 encoded content
        with open(report_path, 'rb') as f:
            import base64
            pdf_content = base64.b64encode(f.read()).decode('utf-8')
        
        # Clean up temporary file
        os.remove(report_path)
        
        return jsonify({
            'pdf_content': pdf_content,
            'filename': f"resume_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        })
        
    except Exception as e:
        logger.error(f"Error in generate_report: {str(e)}")
        return jsonify({'error': 'Failed to generate report'}), 500

@app.route('/api/enhance-resume', methods=['POST'])
def enhance_resume():
    """AI-powered resume enhancement"""
    try:
        data = request.get_json()
        resume_text = data.get('resume_text', '')
        job_description = data.get('job_description', '')
        
        if not resume_text or not job_description:
            return jsonify({'error': 'Resume text and job description required'}), 400
        
        # Extract job keywords
        job_keywords = job_matcher.extract_keywords(job_description)
        
        # Use hybrid scoring engine for analysis
        analysis_results = score_engine.analyze_resume(resume_text, job_keywords)
        
        if analysis_results.get('llm_analysis'):
            # If LLM analysis is available, use it for enhancement suggestions
            enhanced_text = analysis_results['llm_analysis'].get('enhanced_resume', resume_text)
            notes = analysis_results['llm_analysis'].get('improvements', [])
        else:
            # Fallback to basic enhancement
            enhanced_text = resume_text
            notes = ["Using basic enhancement due to LLM service limitations"]
            
            # Apply basic formatting improvements
            if any(keyword not in resume_text.lower() for keyword in job_keywords):
                notes.append("Consider adding more relevant keywords from the job description")
            
            # Add other basic enhancement suggestions
            notes.extend([
                "Use clear section headers (Experience, Education, Skills)",
                "Include quantifiable achievements",
                "Add contact information and professional links"
            ])
        
        response = {
            'enhanced_resume': enhanced_text,
            'enhancement_notes': notes,
            'analysis_method': analysis_results['analysis_method'],
            'enhancement_timestamp': datetime.now().isoformat()
        }
        
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Error in enhance_resume: {str(e)}", exc_info=True)
        return jsonify({'error': 'Resume enhancement failed. Please try again.'}), 500

def generate_recommendations(skill_analysis, ats_score, llm_improvements=None):
    """Generate improvement recommendations integrating LLM insights"""
    recommendations = {
        'strengths': [],
        'weaknesses': [],
        'action_items': []
    }
    
    # ATS Score analysis
    if ats_score >= 80:
        recommendations['strengths'].append("Strong ATS compatibility")
    elif ats_score >= 60:
        recommendations['strengths'].append("Good basic ATS formatting")
        recommendations['action_items'].extend([
            "Add more industry-specific keywords",
            "Enhance section headers for better visibility"
        ])
    else:
        recommendations['weaknesses'].append("Needs ATS optimization")
        recommendations['action_items'].extend([
            "Add relevant keywords from the job description",
            "Improve section headers (Experience, Education, Skills)",
            "Use bullet points for better readability",
            "Include contact information and professional links"
        ])
    
    # Skill analysis
    if skill_analysis:
        matched_skills = skill_analysis.get('matched_skills', [])
        missing_skills = skill_analysis.get('missing_skills', [])
        
        if matched_skills:
            recommendations['strengths'].append(f"Strong match in {len(matched_skills)} key skills")
        
        if missing_skills:
            recommendations['weaknesses'].append(f"Missing {len(missing_skills)} relevant skills")
            recommendations['action_items'].extend([
                f"Consider developing: {', '.join(missing_skills[:3])}",
                "Focus on acquiring the missing technical skills",
                "Highlight transferable skills that compensate for gaps"
            ])
    
    # Integrate LLM improvements if available
    if llm_improvements:
        for improvement in llm_improvements:
            if any(improvement.lower() in item.lower() for item in recommendations['action_items']):
                continue  # Skip duplicate suggestions
            recommendations['action_items'].append(improvement)
    
    # Format recommendations
    if ats_score < 80:
        format_recommendations = [
            "Use consistent date formats",
            "Add more bullet points for achievements",
            "Include clear section headers",
            "Add quantifiable achievements"
        ]
        # Only add format recommendations that aren't duplicates of LLM suggestions
        for rec in format_recommendations:
            if not any(rec.lower() in item.lower() for item in recommendations['action_items']):
                recommendations['action_items'].append(rec)
    
    return recommendations
    
    return recommendations

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
