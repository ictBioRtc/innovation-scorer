import gradio as gr
from openai import OpenAI
import anthropic
import tempfile
import os
from typing import Tuple

# Initialize the clients
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
anthropic_client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def transcribe_and_correct(audio_path: str, title: str) -> str:
    """
    Transcribe audio using OpenAI Whisper API and use the title to help correct potential transcription errors
    """
    try:
        # Transcribe the audio using OpenAI Whisper API
        with open(audio_path, "rb") as audio_file:
            transcription = openai_client.audio.transcriptions.create(
                model="gpt-4o-transcribe",  # Using the newer, more accurate model
                file=audio_file,
                response_format="text"
            )
        
        raw_transcript = transcription if isinstance(transcription, str) else transcription.text
        
        # Use Claude to help correct transcription errors based on the title
        correction_prompt = f"""
        The following is a transcription of a presentation titled "{title}" for an AI Innovation Challenge. 
        The transcription may contain errors due to accents or unclear speech. 
        Please review and correct any obvious transcription errors, keeping the original meaning intact.
        Only fix clear errors - don't rewrite or improve the content.
        
        Original transcription:
        {raw_transcript}
        
        Please provide the corrected transcription:
        """
        
        correction_response = anthropic_client.messages.create(
            model="claude-3-5-sonnet-20241022", # claude-sonnet-4-20250514
            max_tokens=2000,
            messages=[{"role": "user", "content": correction_prompt}]
        )
        corrected_transcript = correction_response.content[0].text.strip()
        return corrected_transcript
        
    except Exception as e:
        print(f"Error in transcription or correction: {e}")
        return f"Error in transcription: {str(e)}"

def score_presentation(team_name: str, transcript: str) -> str:
    """
    Score the presentation using Claude based on the provided rubric
    """
    scoring_prompt = f"""
You are an expert AI judge evaluating student presentations for an AI Innovation Challenge. Your role is to objectively score each team's presentation based on a detailed rubric.

Context:
Students have learned about AI applications over 2 days including document processing, image analysis, text classification, and meeting transcription. Each team had 15 minutes to brainstorm and 3 minutes to present their innovative AI solution.

Your Task:
Evaluate the transcript of {team_name}'s presentation and assign scores for each of the 4 criteria using the detailed rubric below. Provide specific reasoning for each score.

Scoring Rubric (0-4 points per category, 16 points total)

1. Problem Clarity & Relevance (0-4 points)
What to look for: Is the problem clearly defined? Does it affect real people/organizations? Is there genuine need?
- 4 points: Problem is crystal clear, well-articulated, affects identifiable stakeholders (specific people, organizations, industries), demonstrates urgent/important need, presenter explains WHO faces this problem and WHY it matters
- 3 points: Problem is clearly stated and relevant, affects real people/organizations, shows genuine need, minor gaps in explaining impact or stakeholders
- 2 points: Problem is understandable but somewhat vague, limited specificity about who is affected, moderate relevance but not compelling
- 1 point: Problem is poorly defined, vague stakeholders, weak relevance, unclear why this matters
- 0 points: No clear problem stated, irrelevant problem, or problem section missing entirely

2. Solution Innovation & Feasibility (0-4 points)
What to look for: Is the solution creative/innovative? Is it technically possible with current AI? Does it address the stated problem?
- 4 points: Highly creative and original solution, clearly addresses the stated problem, technically feasible with current AI technology, shows understanding of what's possible today
- 3 points: Creative solution with good originality, addresses the problem well, mostly feasible with minor technical concerns, demonstrates good grasp of AI capabilities
- 2 points: Solid but not particularly innovative solution, addresses problem adequately, some feasibility concerns or unclear technical aspects
- 1 point: Basic or unoriginal solution, partially addresses problem, major feasibility issues or unrealistic technical requirements
- 0 points: No clear solution presented, completely unrealistic, or doesn't address the stated problem

3. AI Technical Understanding (0-4 points)
What to look for: Do they understand which AI techniques to use? Can they explain how AI will work in their solution?
- 4 points: Demonstrates deep understanding of specific AI techniques (computer vision, NLP, machine learning, etc.), clearly explains HOW AI will work in their solution, mentions relevant technologies/approaches, shows understanding of AI capabilities and limitations
- 3 points: Good understanding of AI methods, explains the general approach of how AI will work, mentions relevant techniques, minor technical gaps or unclear explanations
- 2 points: Basic understanding of AI application, vague explanation of how AI fits in, some confusion about AI techniques or capabilities
- 1 point: Limited understanding, very vague about how AI will work, mentions AI but doesn't explain the technical approach
- 0 points: No clear explanation of AI implementation, fundamental misunderstanding of AI, or missing technical component entirely

4. Presentation Quality & Clarity (0-4 points)
What to look for: Is the presentation well-organized? Is communication clear and confident? Did they stay within time limits?
- 4 points: Exceptional presentation skills, very clear and confident communication, well-organized structure covering all 4 required elements (Title, Problem, Solution, AI Implementation), stayed within 3-minute limit, engaging delivery
- 3 points: Strong presentation with clear communication, covers all required elements, mostly well-organized, minor issues with clarity or slight time overrun
- 2 points: Adequate presentation but lacks clarity in some areas, covers most required elements, disorganized or goes noticeably over time
- 1 point: Poor presentation quality, unclear communication, missing some required elements, significantly disorganized or over time
- 0 points: Very poor presentation, incomprehensible, missing multiple required elements, or extremely over time

Required Output Format:
Team Name: {team_name}

Detailed Scoring:

1. Problem Clarity & Relevance: [X]/4 points
Reasoning: [Explain your score with specific examples from the transcript. What did they do well? What was missing?]

2. Solution Innovation & Feasibility: [X]/4 points
Reasoning: [Explain your score with specific examples from the transcript. How creative/feasible was their solution?]

3. AI Technical Understanding: [X]/4 points
Reasoning: [Explain your score with specific examples from the transcript. Did they demonstrate understanding of how AI will work?]

4. Presentation Quality & Clarity: [X]/4 points
Reasoning: [Explain your score with specific examples from the transcript. How well did they communicate?]

Total Score: [X]/16 points

Overall Assessment: [2-3 sentence summary of the team's strengths and areas for improvement]

Important Guidelines:
- Be Objective: Score based solely on what's presented in the transcript, not on whether you personally like the idea
- Use Evidence: Support every score with specific examples from the transcript
- Be Fair: Apply the rubric consistently – a score of 3 means the same thing for every team
- Focus on Requirements: Teams must cover Title, Problem, Solution, and AI Implementation
- Consider Feasibility: Judge based on current AI technology capabilities, not future possibilities
- Time Awareness: If transcript indicates they went significantly over 3 minutes, factor this into presentation score

Now, please evaluate the following team's presentation transcript:

{transcript}
    """
    
    try:
        response = anthropic_client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=3000,
            messages=[{"role": "user", "content": scoring_prompt}]
        )
        return response.content[0].text.strip()
    except Exception as e:
        return f"Error in scoring: {str(e)}"

def process_presentation(audio_file, team_name: str) -> Tuple[str, str]:
    """
    Main function to process audio file and return transcript and scoring
    """
    if audio_file is None:
        return "No audio file uploaded", ""
    
    if not team_name.strip():
        return "Please enter a team name", ""
    
    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".m4a") as tmp_file:
            tmp_file.write(audio_file)
            tmp_file_path = tmp_file.name
        
        # Transcribe and correct
        transcript = transcribe_and_correct(tmp_file_path, team_name)
        
        # Score the presentation
        scoring_result = score_presentation(team_name, transcript)
        
        # Clean up temporary file
        os.unlink(tmp_file_path)
        
        return transcript, scoring_result
        
    except Exception as e:
        return f"Error processing presentation: {str(e)}", ""

# Create Gradio interface
def create_interface():
    with gr.Blocks(title="AI Innovation Challenge Scorer", theme=gr.themes.Soft()) as interface:
        gr.Markdown("""
        # 🚀 AI Innovation Challenge Scorer
        
        Upload your team's presentation audio (M4A format) and get automated transcription and scoring based on the official rubric.
        
        **Instructions:**
        1. Enter your team name
        2. Upload your M4A audio file (max 3 minutes recommended)
        3. Click "Process Presentation" to get transcription and scoring
        """)
        
        with gr.Row():
            with gr.Column(scale=1):
                team_name_input = gr.Textbox(
                    label="Team Name",
                    placeholder="Enter your team name here",
                    lines=1
                )
                
                audio_input = gr.File(
                    label="Upload Presentation Audio (M4A)",
                    file_types=[".m4a", ".mp3", ".wav"],
                    type="binary"
                )
                
                process_btn = gr.Button("🎯 Process Presentation", variant="primary", size="lg")
        
        with gr.Row():
            with gr.Column(scale=1):
                transcript_output = gr.Textbox(
                    label="📝 Corrected Transcript",
                    lines=10,
                    interactive=False
                )
            
            with gr.Column(scale=1):
                scoring_output = gr.Textbox(
                    label="📊 Detailed Scoring & Feedback",
                    lines=15,
                    interactive=False
                )
        
        process_btn.click(
            fn=process_presentation,
            inputs=[audio_input, team_name_input],
            outputs=[transcript_output, scoring_output]
        )
        
        gr.Markdown("""
        ---
        **Note:** Make sure you have set both your `OPENAI_API_KEY` and `ANTHROPIC_API_KEY` environment variables before running this app.
        
        **Scoring Criteria:** Problem Clarity (4pts) + Solution Innovation (4pts) + AI Technical Understanding (4pts) + Presentation Quality (4pts) = 16 points total
        """)
    
    return interface

# Launch the interface
if __name__ == "__main__":
    # Check if API keys are set
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  Warning: OPENAI_API_KEY environment variable not set!")
        print("Please set your OpenAI API key before running the app:")
        print("export OPENAI_API_KEY='your_api_key_here'")
    
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("⚠️  Warning: ANTHROPIC_API_KEY environment variable not set!")
        print("Please set your Anthropic API key before running the app:")
        print("export ANTHROPIC_API_KEY='your_api_key_here'")
    
    app = create_interface()
    app.launch(
        share=True,  # Set to True if you want a public link
    )
