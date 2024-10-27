import asyncio
import os

from actions.action import SkillMatch, ProfileEnhance, ResumePolish, InterviewCoach
from metagpt.logs import logger
from metagpt.roles import Role
from metagpt.schema import Message
from dotenv import load_dotenv

class ResumeGenie(Role):
    """
    A ResumeGenie agent to guide users in refining resumes, generating interview questions, and
    enhancing job application profiles based on a job posting.

    Attributes:
        job_posting (str): The job posting content to analyze.
        resume (str): The resume content to enhance and polish.
        job_analysis (str): Analyzed job posting information from SkillMatch.
        enhanced_profile (str): Enhanced profile information from ProfileEnhance.
        refined_resume (str): Final refined resume output from ResumePolish.
    """

    def __init__(self, job_posting: str, resume: str, **kwargs):
        """
        Initializes ResumeGenie with actions to perform and input documents.

        Args:
            job_posting (str): The job posting details.
            resume (str): The applicant's resume details.
            **kwargs: Additional keyword arguments for the Role base class.
        """
        super().__init__(**kwargs)
        self.set_actions([SkillMatch(),
                          ProfileEnhance(),
                          ResumePolish(),
                          InterviewCoach()])
        self.job_posting = job_posting
        self.resume = resume
        self._set_react_mode(react_mode="by_order")

    async def _act(self) -> Message:
        """
        Performs the assigned action step-by-step, sequentially calling each action in order
        and storing intermediate results for use by subsequent actions.

        Returns:
            Message: A message object containing the output of the action.
        """
        logger.info(f"{self.__class__}: Awaiting result from step: {self.rc.todo}")
        todo = self.rc.todo

        if isinstance(todo, SkillMatch):
            job_analysis = await todo.run(self.job_posting)
            self.job_analysis = job_analysis
            ret = Message(content=job_analysis, role=self.profile, cause_by=type(todo))

        elif isinstance(todo, ProfileEnhance):
            messages = self.get_memories(k=2)
            translated_document = messages[1].content
            original_document = messages[0].content
            enhanced_profile = await todo.run(self.job_analysis, self.resume)
            self.enhanced_profile = enhanced_profile
            ret = Message(content=enhanced_profile, role=self.profile, cause_by=type(todo))

        elif isinstance(todo, ResumePolish):
            refined_resume = await todo.run(self.job_analysis, self.enhanced_profile, self.resume)
            self.refined_resume = refined_resume
            ret = Message(content=refined_resume, role=self.profile, cause_by=type(todo))

        elif isinstance(todo, InterviewCoach):
            interview_questions = await todo.run(self.refined_resume, self.job_posting)
            ret = Message(content=interview_questions, role=self.profile, cause_by=type(todo))

        self.rc.memory.add(ret)
        return ret

async def main():
    """
    Main function to load job posting and resume data, instantiate ResumeGenie, and run the
    resume generation and interview preparation process.

    The function retrieves the file paths from environment variables, reads the contents, and
    then initializes and executes the ResumeGenie role.
    """
    load_dotenv()
    job_posting_path = os.getenv("JOB_POSTING_PATH")
    resume_path = os.getenv("RESUME_PATH")

    # Load job posting and resume content from specified files
    with open(job_posting_path, 'r', encoding='utf-8') as file:
        job_posting = file.read()
    with open(resume_path, 'r', encoding='utf-8') as file:
        resume = file.read()

    resume_message = Message(content=resume)

    role = ResumeGenie(job_posting=job_posting, resume=resume)
    try:
        logger.info("Starting ResumeGenie processing with the provided resume.")
        result = await role.run(resume_message)
        print(result)
    except Exception as e:
        logger.error(f"Failed to run resume genie: {e}")

if __name__ == "__main__":
    asyncio.run(main())