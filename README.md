# 🚀 Resume Refiner AI

A comprehensive AI-powered resume analysis and optimization platform that helps job seekers improve their resumes and increase their chances of getting hired.

## ✨ Features

- **✅ Resume–Job Match Scoring** - AI-powered matching algorithm
- **✅ ATS Resume Score Engine** - Comprehensive ATS compatibility analysis
- **✅ Resume Uploader & Text Extractor** - Support for PDF, DOCX, TXT files
- **✅ Missing Skills Highlighter** - Identify skill gaps and get recommendations
- **✅ Advanced GenAI Resume Enhancer** - LLM-powered resume improvement with detailed analysis
- **✅ Enhanced Score Matrix** - Detailed strengths, weaknesses, and action insights
- **✅ Comprehensive Scoring Reports** - Professional PDF reports with competitive analysis
- **✅ Public Deployment** - Full-stack web application

## 🏗️ Architecture

### Backend (Python/Flask)
- **Flask API Server** - RESTful API endpoints
- **Machine Learning Pipeline** - Gradient Boosting model for job-resume matching
- **ATS Score Engine** - Multi-factor scoring algorithm
- **Resume Processor** - Text extraction from multiple file formats
- **Skill Analyzer** - Comprehensive skill gap analysis
- **Report Generator** - PDF and JSON report generation

### Frontend (React/Vite)
- **Modern React Application** - Built with Vite for fast development
- **Responsive UI** - Tailwind CSS with custom styling
- **Interactive Analysis** - Real-time resume analysis interface
- **Professional Design** - Dark theme with cyan accents

### Machine Learning Model
- **Feature Engineering** - TF-IDF vectorization, skill matching, semantic embeddings
- **Model Training** - Gradient Boosting Regressor with 99.97% R² score
- **Prediction Pipeline** - Real-time job-resume compatibility scoring

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup

1. **Navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Start the server**
   ```bash
   python run.py
   ```

   The API server will start at `http://localhost:5000`

### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start development server**
   ```bash
   npm run dev
   ```

   The frontend will start at `http://localhost:5173`

## 📊 Model Performance

Our machine learning model achieves excellent performance:

- **R² Score**: 99.97%
- **RMSE**: 0.0010
- **MAE**: 0.0002

### Model Features
- Jaccard similarity between skill sets
- Common skills count
- Skill vector similarity (cosine)
- Skill count difference and ratio
- Skills density in resume

## 🔧 API Endpoints

### POST `/api/analyze-resume`
Analyze resume against job description
- **Input**: Resume file/text + job description
- **Output**: ATS score, match score, skill analysis, recommendations

### POST `/api/generate-report`
Generate PDF report
- **Input**: Analysis results
- **Output**: Base64 encoded PDF

### POST `/api/enhance-resume`
AI-powered resume enhancement
- **Input**: Resume text + job description
- **Output**: Enhanced resume with suggestions

### GET `/health`
Health check endpoint

## 📁 Project Structure

```
resume-refiner-ai/
├── backend/
│   ├── app.py                 # Flask application
│   ├── ats_score_engine.py    # ATS scoring algorithms
│   ├── resume_processor.py    # File processing and text extraction
│   ├── job_matcher.py         # Job-resume matching logic
│   ├── skill_analyzer.py      # Skill gap analysis
│   ├── report_generator.py    # PDF report generation
│   ├── requirements.txt       # Python dependencies
│   ├── run.py                 # Server startup script
│   └── notebooks/
│       ├── 5phases.ipynb      # ML model training notebook
│       ├── *.pkl              # Trained models and scalers
│       └── *.csv              # Training datasets
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── HomePage.jsx   # Landing page
│   │   │   ├── AnalyzerPage.jsx # Resume analysis interface
│   │   │   └── ui/            # Reusable UI components
│   │   ├── App.jsx            # Main application
│   │   └── main.jsx           # Entry point
│   ├── package.json           # Node.js dependencies
│   └── vite.config.js         # Vite configuration
└── README.md
```

## 🧠 How It Works

### 1. Resume Processing
- Extract text from PDF, DOCX, or TXT files
- Clean and normalize text content
- Extract contact information and sections

### 2. Job Analysis
- Parse job description for requirements
- Extract technical skills and keywords
- Categorize skills by type (programming, frameworks, etc.)

### 3. Matching Algorithm
- Calculate multiple similarity metrics:
  - Keyword overlap (Jaccard similarity)
  - Text similarity (TF-IDF cosine similarity)
  - Skill vector matching
  - Contextual relevance scoring

### 4. ATS Scoring
- Section structure analysis
- Keyword density and relevance
- Formatting quality assessment
- Contact information completeness

### 5. Skill Gap Analysis
- Identify missing skills by category
- Prioritize critical skills
- Generate learning recommendations
- Suggest relevant courses

## 🎯 Key Algorithms

### ATS Score Calculation
```python
final_score = (
    section_score * 0.25 + 
    keyword_score * 0.35 + 
    format_score * 0.20 + 
    context_score * 0.20
)
```

### Job Match Score
```python
match_score = (
    jaccard_similarity * 0.4 +
    text_similarity * 0.35 +
    skill_match * 0.25
)
```

## 🔮 Future Enhancements

- **LLM Integration** - OpenAI/Anthropic API for advanced resume enhancement
- **Real-time Collaboration** - Multi-user resume editing
- **Industry-Specific Models** - Specialized scoring for different sectors
- **Chrome Extension** - Browser-based resume analysis
- **Mobile App** - React Native mobile application
- **Advanced Analytics** - Detailed performance metrics and insights

## 🧪 Testing

### Backend Testing
```bash
cd backend
python test_api.py
```

### Manual Testing
1. Start backend: `python run.py`
2. Start frontend: `npm run dev`
3. Visit `http://localhost:5173`
4. Upload a resume and job description
5. Analyze and download report

## 🚀 Deployment

### Docker Deployment
```bash
# Build and run with Docker Compose
docker-compose up --build

# Access the application
# Frontend: http://localhost:3000
# Backend API: http://localhost:5000
```

### Manual Deployment
```bash
# Backend
cd backend
pip install -r requirements.txt
python run.py

# Frontend
cd frontend
npm install
npm run build
npm run preview
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Datasets**: IT Job Roles & Skills, Updated Resume Dataset
- **Libraries**: scikit-learn, sentence-transformers, Flask, React
- **UI**: Tailwind CSS, Lucide React icons

---

**Built with ❤️ for job seekers worldwide**

## 🧠 Advanced Gen AI Features

The Resume Refiner AI now includes powerful generative AI capabilities that deliver more comprehensive analysis and better recommendations:

### Enhanced Score Matrix

- **Detailed Strengths Analysis** - AI identifies your resume's strongest points relative to the job
- **Weakness Identification** - Pinpoints specific areas where your resume falls short
- **Action Insights** - Provides specific, actionable steps to improve your resume
- **Competitive Analysis** - Shows how your resume compares to typical competition

### Advanced Resume Enhancement

- **AI-Powered Rewriting** - Smart suggestions to improve wording and presentation
- **Keyword Optimization** - Strategic placement of job-relevant keywords
- **Achievement Highlighting** - Transforms experience bullets into impressive achievements
- **Format Improvements** - Makes your resume more readable and ATS-friendly

### Getting Started with Gen AI Features

1. Copy `.env.example` to `.env` in the backend directory
2. Add your OpenAI or Anthropic API key to the `.env` file
3. Uncomment the preferred API provider in `requirements.txt` and install it
4. Restart the application

```bash
cd backend
cp .env.example .env
# Edit .env to add your API key
pip install openai==1.13.3  # or anthropic==0.8.1
python run.py
```
