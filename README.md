# 🚀 Innovation Challenge Scorer

An automated scoring system for innovation challenge presentations that transcribes audio submissions and provides detailed scoring based on a comprehensive rubric.

## 📋 Overview

This Gradio-based web application helps us to efficiently evaluate presentations for AI Innovation Challenge. The system automatically transcribes audio recordings, corrects transcription errors using contextual information, and provides detailed scoring with specific feedback.

## ✨ Features

- **🎵 Audio Processing**: Supports M4A, MP3, and WAV audio formats
- **🎯 Smart Transcription**: Uses OpenAI's latest `gpt-4o-transcribe` model for high-accuracy transcription
- **🔧 Error Correction**: Leverages presentation titles to correct accent-related transcription errors
- **📊 Automated Scoring**: Comprehensive 16-point scoring system across 4 key criteria
- **💬 Detailed Feedback**: Specific reasoning and examples for each score
- **🌐 Web Interface**: User-friendly Gradio interface accessible via web browser

## 🎯 Scoring Criteria

The system evaluates presentations across four categories (4 points each, 16 points total):

1. **Problem Clarity & Relevance** - Is the problem well-defined and important?
2. **Solution Innovation & Feasibility** - Is the solution creative and technically possible?
3. **AI Technical Understanding** - Do they understand the AI implementation?
4. **Presentation Quality & Clarity** - Is the presentation well-organized and clear?

## 🛠️ Installation

### Prerequisites

- Python 3.8 or higher
- OpenAI API key
- Anthropic API key

### Install Dependencies

```bash
pip install gradio openai anthropic
```

### Set Environment Variables

```bash
export OPENAI_API_KEY='your_openai_api_key_here'
export ANTHROPIC_API_KEY='your_anthropic_api_key_here'
```

## 🚀 Usage

### Running the Application

```bash
python innovation_scorer.py
```

The application will launch at `http://localhost:7860`

### Using the Interface

1. **Enter Team Name**: Input the team's name or presentation title
2. **Upload Audio**: Select the M4A, MP3, or WAV audio file (recommended: 3 minutes max)
3. **Process**: Click "Process Presentation" to get transcription and scoring
4. **Review Results**: View the corrected transcript and detailed scoring feedback

### Example Workflow

```
Team Name: "Smart City Traffic Optimizer"
Audio File: team_presentation.m4a
↓
Transcription: "Our solution uses computer vision to analyze traffic patterns..."
↓
Scoring: Problem Clarity: 4/4, Solution Innovation: 3/4, etc.
```

## 📁 Project Structure

```
├── app.py    # Main application file
├── README.md              # This file
└── requirements.txt       # Python dependencies (optional)
```

## 🔧 Configuration

### Model Selection

The app uses:
- **Transcription**: `gpt-4o-transcribe` (OpenAI's latest Whisper model)
- **Scoring**: `claude-3-sonnet-20240229` (Anthropic's Claude model)

### Customization Options

You can modify the following in the code:
- **Scoring rubric**: Update the prompt in `score_presentation()` function
- **Audio formats**: Modify `file_types` in the Gradio interface
- **Model parameters**: Adjust `max_tokens` or model versions

## 📊 Scoring Rubric Details

### Problem Clarity & Relevance (0-4 points)
- **4 points**: Crystal clear problem, identifiable stakeholders, urgent need
- **3 points**: Clear and relevant problem, genuine need, minor gaps
- **2 points**: Understandable but vague, moderate relevance
- **1 point**: Poorly defined, weak relevance
- **0 points**: No clear problem or irrelevant

### Solution Innovation & Feasibility (0-4 points)
- **4 points**: Highly creative, addresses problem, technically feasible
- **3 points**: Creative solution, mostly feasible, good AI grasp
- **2 points**: Solid but not innovative, some feasibility concerns
- **1 point**: Basic solution, major feasibility issues
- **0 points**: No clear solution or completely unrealistic

### AI Technical Understanding (0-4 points)
- **4 points**: Deep understanding of AI techniques, clear implementation
- **3 points**: Good understanding, explains general approach
- **2 points**: Basic understanding, vague AI explanation
- **1 point**: Limited understanding, very vague
- **0 points**: No AI explanation or fundamental misunderstanding

### Presentation Quality & Clarity (0-4 points)
- **4 points**: Exceptional presentation, covers all elements, within time
- **3 points**: Strong presentation, clear communication, minor issues
- **2 points**: Adequate but lacks clarity, disorganized or over time
- **1 point**: Poor quality, missing elements, significantly over time
- **0 points**: Very poor, incomprehensible, missing multiple elements

## 🤝 Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

### Development Setup

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set up environment variables
4. Run the application: `python app.py`

## 🔒 Security Notes

- API keys are loaded from environment variables (never hardcode them)
- Temporary audio files are automatically cleaned up after processing
- The application doesn't store or persist audio files or transcriptions

## 📄 License

This project is open source. Please ensure you comply with OpenAI and Anthropic's API usage terms.

## 🆘 Troubleshooting

### Common Issues

**API Key Errors**
```bash
# Make sure both API keys are set
echo $OPENAI_API_KEY
echo $ANTHROPIC_API_KEY
```

**Audio Format Issues**
- Ensure audio file is in supported format (M4A, MP3, WAV)
- Check file size (very large files may cause timeout)

**Transcription Errors**
- Verify audio quality and clarity
- Ensure the team name/title is relevant to help with correction

**Port Already in Use**
```bash
# Change port in the code or kill existing process
lsof -ti:7860 | xargs kill -9
```

## 📞 Support

For issues or questions:
1. Check the troubleshooting section above
2. Review OpenAI and Anthropic API documentation
3. Submit an issue in the repository

---

**Built with ❤️ for educational innovation challenges**