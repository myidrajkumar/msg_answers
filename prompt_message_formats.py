"""Prompt Formats"""


def get_system_prompt(results):
    """Ask the system prompt"""
    return (
        """
You must answer only based on the data given below.
Do NOT use your internal knowledge and do NOT share any other information.
When you are providing answer, no mention of 'text is provided' or 'according to data' as such.
Just provide the answer from the the knowledge I'm providing.
If you don't know the answer,
just say: Requested question is out of my knowledge.
--------------------
The data:
"""
        + str(results["documents"])
        + """
"""
    )
