import asyncio
import os

from actions.action import SkillMatch, ProfileEnhance, ResumePolish, InterviewCoach
from metagpt.logs import logger
from metagpt.roles import Role
from metagpt.schema import Message
from dotenv import load_dotenv

class ResumeGenie(Role):
    def __init__(self, job_posting: str, resume: str, **kwargs):
        super().__init__(**kwargs)
        self.set_actions([SkillMatch(),
                          ProfileEnhance(),
                          ResumePolish(),
                          InterviewCoach()])
        self.job_posting = job_posting
        self.resume = resume
        self._set_react_mode(react_mode="by_order")

    async def _act(self) -> Message:
        logger.info(f"{self._setting}: Run step: {self.rc.todo}")
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
    # Get files from local
    load_dotenv()
    job_posting_path = os.getenv("JOB_POSTING_PATH")
    resume_path = os.getenv("RESUME_PATH")

    with open(job_posting_path, 'r', encoding='utf-8') as file:
        job_posting = file.read()
    with open(resume_path, 'r', encoding='utf-8') as file:
        resume = file.read()

    role = ResumeGenie(job_posting=job_posting, resume=resume)
    result = await role.run()

    print(result)

if __name__ == "__main__":
    asyncio.run(main())