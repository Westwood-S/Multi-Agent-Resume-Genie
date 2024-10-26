import asyncio

from metagpt.actions import Action

# --------- Actions ---------
class SkillMatch(Action):
    PROMPT_TEMPLATE: str = """
    You are a **Tech Job Researcher** with an exceptional ability to analyze job postings to support job applicants. Your task is to perform a detailed analysis of the provided job posting, identifying the qualifications, skills, and attributes that employers seek. This information will form the foundation for tailoring effective job applications.

    Goal: Extract a structured breakdown of critical job requirements and insights to help applicants align their profiles effectively.

    **Instructions**: Analyze the job posting and provide a structured output with the following categories:
    - **Core Skills**: Specific technical and soft skills required (e.g., "Python programming", "project management").
    - **Experience Requirements**: Key experiences or years of experience required (e.g., "3+ years in data science").
    - **Educational Requirements**: Degrees, certifications, or specialized training necessary for the role (e.g., "Bachelor's in Computer Science", "AWS Certified Solutions Architect").
    - **Technical Knowledge or Tools**: Specific tools, languages, or platforms required for the role (e.g., "SQL", "TensorFlow", "AWS").
    - **Key Responsibilities**: Main responsibilities or duties the candidate will perform (e.g., "Manage a team of software engineers", "Develop REST APIs").
    - **Desired Traits**: Personality traits or soft skills valued by the employer (e.g., "attention to detail", "collaborative mindset").
    - **Company Culture Fit**: Attributes or values that align with the company culture (e.g., "innovation-driven", "collaborative environment").
    - **Communication and Collaboration Expectations**: Required communication skills or cross-team collaboration needs (e.g., "communicate technical concepts to non-technical stakeholders").

    Format your response in JSON as follows:
    ```
    {
        "core_skills": [...],
        "experience_requirements": [...],
        "educational_requirements": [...],
        "technical_knowledge_or_tools": [...],
        "key_responsibilities": [...],
        "desired_traits": [...],
        "company_culture_fit": [...],
        "communication_and_collaboration": [...]
    }
    ```

    **Job Posting**:
    ```
    {job_posting}
    ```
    """

    async def run(self, job_posting: str) -> str:
        prompt = self.PROMPT_TEMPLATE.format(job_posting=job_posting)
        response = await self._aask(prompt)
        return response

class ProfileEnhance(Action):
    PROMPT_TEMPLATE: str = """
    You are a **Personal Profiler for Engineers**, dedicated to helping applicants create standout profiles. Using the structured job analysis from SkillMatch, enhance the provided resume to align with the job's key qualifications, skills, and attributes.

    Goal: Refine the resume to highlight the applicant's most relevant skills, experiences, and qualities, ensuring alignment with the job's requirements to make a lasting impression.

    **Instructions**:
    - **Highlight Relevant Skills**: Ensure that core skills identified in "core_skills" are emphasized within the resume.
    - **Align Experience Details**: Adjust descriptions in the resume to align with "experience_requirements" and demonstrate the applicant’s suitability for the role.
    - **Emphasize Educational Background**: If relevant, ensure educational credentials in "educational_requirements" are prominent.
    - **Technical Knowledge and Tools**: Highlight specific tools, languages, or platforms from "technical_knowledge_or_tools" to show direct alignment with the job.
    - **Key Responsibilities**: Tailor experience descriptions to reflect the "key_responsibilities" of the role, showcasing similar accomplishments.
    - **Incorporate Desired Traits and Cultural Fit**: Subtly integrate references to desired traits from "desired_traits" and attributes from "company_culture_fit" to demonstrate alignment with company values.
    - **Communication and Collaboration**: Highlight any relevant communication or teamwork skills matching "communication_and_collaboration" needs.

     **Format**:
    Return the enhanced profile in JSON-like format as follows:
    ```
    {
        "highlight_relevant_skills": ["List of emphasized core skills"],
        "align_experience_details": [
            {
                "title": "Position Title",
                "company": "Company Name",
                "description": "Enhanced experience details aligning with job responsibilities and requirements"
            },
            ...
        ],
        "emphasize_educational_background": "Relevant educational qualifications",
        "technical_knowledge_and_tools": ["List of technical skills or tools relevant to the job"],
        "key_responsibilities": ["Responsibilities tailored to align with the job role"],
        "incorporate_desired_traits_and_cultural_fit": ["List of traits aligning with job and company culture"],
        "communication_and_collaboration": ["Relevant communication and collaboration skills"]
    }
    ```

    **Job Analysis**:
    ```
    {job_analysis}
    ```

    **Resume**:
    ```
    {resume}
    ```
    """

    async def run(self, job_analysis: str, resume: str) -> str:
        prompt = self.PROMPT_TEMPLATE.format(job_analysis=job_analysis, resume=resume)
        response = await self._aask(prompt)
        return response

class ResumePolish(Action):
    PROMPT_TEMPLATE: str = """
    You are a **Resume Strategist for Engineers** with expertise in creating impactful resumes. Based on the job analysis from SkillMatch and the enhanced profile from ProfileEnhance, your task is to draft a well-organized resume that aligns closely with job requirements and highlights the applicant's most relevant qualifications.

    Goal: Refine the resume to emphasize the applicant's core skills, aligned experiences, educational background, and traits, making it resonate strongly with the job requirements.

    **Instructions**:
    - **Use Bullet Points**: Write the experience section in bullet points, with each bullet point not exceeding four sentences.
    - **Highlight Core Skills and Technical Knowledge**: Include skills from the "core_skills" and "technical_knowledge_or_tools" sections in an organized skills section.
    - **Emphasize Relevant Experience**: Align the applicant's work experience with the "key_responsibilities" and "experience_requirements" identified in SkillMatch. Use concise bullet points to describe achievements and responsibilities.
    - **Incorporate Traits and Cultural Fit**: Subtly reflect desired traits and cultural fit in the phrasing of experiences and accomplishments.
    - **Educational Background**: Ensure any relevant educational qualifications are clearly stated and formatted.

    **Format**:
    The resume should be structured as follows:
    ```
    {
        "summary": "A concise summary highlighting the applicant's alignment with the job requirements.",
        "skills": ["List of key skills, including technical knowledge"],
        "experience": [
            {
                "title": "Position Title",
                "company": "Company Name",
                "dates": "Employment Dates",
                "bullet_points": [
                    "Bullet point describing an aligned achievement or responsibility.",
                    "Another bullet point with a max of 4 sentences.",
                    ...
                ]
            },
            ...
        ],
        "education": "Educational qualifications relevant to the job"
    }
    ```

    **Job Analysis**:
    ```
    {job_analysis}
    ```

    **Enhanced Profile**:
    ```
    {enhanced_profile}
    ```
    **Resume**:
    ```
    {resume}
    ```
    """

    async def run(self, job_analysis:str, enhanced_profile: str, resume: str) -> str:
        prompt = self.PROMPT_TEMPLATE.format(job_analysis=job_analysis, enhanced_profile=enhanced_profile, resume=resume)
        response = await self._aask(prompt)
        return response

class InterviewCoach(Action):
    PROMPT_TEMPLATE: str = """
    You are an **Engineering Interview Preparer**, specializing in crafting interview questions and talking points to help applicants confidently present their qualifications. Based on the refined resume from ResumePolish and the original job requirements, your task is to develop a set of strategic interview questions and key talking points.

    Goal: Create a preparation guide that includes targeted interview questions, suggested answers, and main talking points, allowing the candidate to highlight their most relevant skills, experiences, and accomplishments effectively.

    **Instructions**:
    - **Develop Targeted Interview Questions**: Use the applicant's experiences, skills, and traits to formulate questions that align with the job requirements.
    - **Suggested Answers**: Provide short, insightful answer suggestions for each question, focusing on how the applicant’s qualifications and experiences meet the job's demands.
    - **Key Talking Points**: Summarize important topics or themes the applicant should emphasize, particularly skills, experiences, and traits relevant to the role and company culture.
    - **Focus on Relevance**: Ensure that each question and talking point is directly related to the job requirements and the refined resume to maximize the applicant's alignment with the role.

    **Result Format**:
    ```
    {
        "interview_questions": [
            {
                "question": "A targeted question that aligns with the job requirements.",
                "suggested_answer": "A concise and insightful answer that highlights the applicant's relevant skills and experiences."
            },
            ...
        ],
        "key_talking_points": [
            "Important skill or experience to emphasize",
            "Another key point to discuss, tailored to the job requirements",
            ...
        ]
    }
    ```

    **Most Important Output**:
    The most critical aspect of this preparation is to provide **questions and talking points that allow the applicant to highlight the skills and experiences most relevant to the role**. This ensures the applicant is fully prepared to convey their alignment with the job and to handle the most common or challenging interview questions confidently.

    **Refined Resume**:
    ```
    {refined_resume}
    ```

    **Job Requirements**:
    ```
    {job_posting}
    ```
    """

    async def run(self, refined_resume: str, job_posting: str) -> str:
        prompt = self.PROMPT_TEMPLATE.format(refined_resume=refined_resume, job_posting=job_posting)
        response = await self._aask(prompt)
        return response