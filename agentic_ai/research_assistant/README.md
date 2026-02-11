### Multi-Agent Research Assistant with Human-in-the-Loop

This project implements an autonomous research agent using LangGraph and LangChain.
It goes beyond simple single agent by employing a multi-agent "Interview" strategy where specialized AI analysts
identify sub-themes, conduct concurrent research, and synthesize information into a comprehensive, grounded report.

#### Project Architecture
The overall workflow is shown below

<img width="655" height="1350" alt="image" src="https://github.com/user-attachments/assets/a7ebe694-6fe2-4824-89ab-5360b2f4d03a" />

The agent follows a hierarchical structure that includes the following: 
1.	**Sub-agents spawning:** Based on the given topic, the master agent identifies sub-themes and spawns a maximum number of specialized
    "Analyst" agents. Each analyst agent is assigned a unique persona , role and organization that aligns with their respective theme. 
2.	**Human-in-the-Loop:** The workflow pauses for human intervention, allowing a user to review the analysts,
    refine their roles, or add new personas before the research begins. 
3.	**Concurrent Expert Interviews:** The analysts concurrently conduct interview with an expert on their sub-theme.
    This back-and-forth dialogue allows the sub-agent to dig deeper into the topic and ask non-obvious questions. 
4.	**Query Decomposition & Retrieval:** The conversation history is re-formatted into searchable queries for the Web and Wikipedia,
     breaking down composite questions into single-issue queries. 
6.	**Sub-sections generation with citations:** Sections are curated into markdown format with source citations for each claim
     to eliminate hallucinations. 
8.	**Final Report Compilation:** A "Lead Technical Writer" agent merges all sections into a coherent report with a compelling
    introduction, conclusion, and a consolidated list of references.
  	
### Challenges & Solutions
1. **Resource Optimization (Small LLM Efficiency):** I specifically chose Mistral-Small to explore how relatively
   small language models excel at reasoning and instruction following tasks. This required rigorous prompt engineering to
   ensure the model followed structured instructions and handled composite queries effectively. 
2. **Concurrency**: By using LangGraph's Send operation, I implemented parallel processing for the analyst interviews.
   This significantly reduced the total wall-clock time required to generate  reports.
3. **Verification & Grounding**: To ensure the agent is not hallucination, the agent is tasked with:   
   *Source Citing*: Every claim must have a citation.   
   *Summarization*: The final report is restricted to only the information gathered during the research phase,
       preventing the LLM from using any pre-trained knowledge or external information.
   
## Technical Stack
Agent workflow: LangGraph, LangChain 

LLM: Mistral-Small-Latest

Tools: Wikipedia Search, Web Search API 
    
## Example Workflow

  1.	**Topic**: 'Effect of LLM in student learning'
  
  2.	**Analysts Spawned:**
     
        Analyst-1: name='Dr. Sarah Chen', organization='..', **role='Senior Researcher'**,description="...".
        
        Analyst-2: name='Professor James Wilson', organization='..',  **role='Professor of Cognitive Psychology'**, description="..." 
        
        Analyst-3: name='Dr. Lisa Thompson', organization='..', **role='Assistant Professor of Education'**, description="..."
    
  3.	**Human Feedback:** Add a cognitive scientist.
     
        _Updated Analysts:_ 
        
        Analyst(name='Dr. Sarah Johnson', organization='Cognitive Science Institute',
         **role='Cognitive Scientist'**, description='..'),
        
        Analyst(name='Dr. Michael Chen', organization='Educational Technology Research Center',
        **role='Educational Technologist'**, description='..'),
        
        Analyst(name='Dr. Lisa Thompson', organization='Institute for Learning Analytics', 
        **role='Learning Analyst'**, description='..')
  
  4.	**Interview**: Agents concurrently conduct interviews with experts to gather information and ask follow-up questions
  5.	**Question Generation**: Based on this interview, the agent generates searchable queries
  6.	**Section Generation**: Based on the query results, individual sections are generated with citations
  7.	**Report Generation**: The sections are finally combined into one cohesive report with Introduction, conclusion and references.
  8.	**Final report**: A 1400+ word technical report with around 12 unique citations is generated. The full report is available in the output folder.

### Sample interview between Analyst and expert - Dr.Sara Johson - 'Cognitive Scientist'

**Interviewer (Dr. Sarah Johnson):**
"Thank you for taking the time to speak with me today. 
As a cognitive scientist, I'm particularly interested in the nuanced ways that large language models (LLMs) are reshaping student 
learning. One question that has been on my mind is: *How do LLMs influence the metacognitive processes of students,
particularly in their ability to self-regulate and monitor their own learning?*

I'm curious if you've observed any shifts in how students plan, monitor, and evaluate their learning 
when they have access to these powerful tools. 
For instance, do they become more reliant on the model's outputs, or does it enhance their ability to critically 
assess their own understanding?"

**Expert:**
"Great question, Dr. Johnson. We've actually seen some fascinating trends in this area. 
LLMs do seem to impact metacognitive processes, but the effects are nuanced.
On one hand, students often use LLMs to generate study plans or break down complex topics, which can scaffold their planning phase.
However, there's a risk that over-reliance on the model's outputs might lead to a reduced ability to self-monitor. 
For example, students might accept the LLM's explanations without critically evaluating them, 
which could hinder their metacognitive accuracy.

On the other hand, when used intentionally, LLMs can enhance metacognition. 
For instance, students might use the model to generate practice questions, then reflect on their answers and compare them to the 
model's feedback. This process can help them develop better self-assessment skills. 
The key seems to be whether students are actively engaging with the model's outputs or passively consuming them."

**Interviewer (Dr. Sarah Johnson):**
"That's a really insightful observation. It makes me think about the role of *deliberate practice* in this context. 
Have you noticed any differences in how students engage in self-regulated learning when they use LLMs compared to traditional 
study methods? For example, do they spend more time in the *zone of proximal development*—that is, 
working just at the edge of their current understanding—when they have access to an LLM?"

---- the interview goes on

### Sample questions

Based on the interview between each analyst and expert, the following questions are generated

  Analyst 1: questions generated: [
  'How do large language models (LLMs) influence the metacognitive processes of students, 
  particularly in their ability to self-regulate and monitor their own learning?',
  'What are the differences in how students engage in self-regulated learning when they use LLMs compared to traditional 
  study methods?'
  ]
  
  Analyst 2: questions generated: [
  'How are large language models (LLMs) transforming the way students approach interdisciplinary 
  problems in fields like bioinformatics or environmental science?', 
  'What role do large language models (LLMs) play in facilitating interdisciplinary connections and suggesting resources in 
  student research?']
  
  Analyst 3: questions generated: [
  'What are the under-discussed benefits of large language models (LLMs) in education beyond content generation?', 
  'How can educators adapt their teaching methods to leverage the cognitive mirror effect of LLMs in education?']

### Sample section:
   
  ## Unlocking Metacognition: How LLMs Transform Student Learning

  ### The Metacognitive Edge of LLMs
  
  The integration of large language models (LLMs) into educational settings has sparked significant interest in their 
  potential to enhance students' metacognitive processes, particularly in self-regulation and self-monitoring of learning. 
  Traditional study methods often rely on static resources and passive engagement, whereas LLMs offer dynamic, interactive, 
  and personalized learning experiences. This shift has profound implications for how students approach, monitor, 
  and regulate their learning journeys.
  
  One of the most compelling findings is that LLMs can significantly enhance students' self-reflective practices. 
  Through personalized feedback and prompts, LLMs encourage students to critically evaluate their learning strategies and outcomes. This interaction fosters a deeper understanding of their own cognitive processes, enabling them to better assess their comprehension and adjust their approaches accordingly [1,2]. The scalability of LLMs allows for widespread implementation of self-reflective practices, making metacognitive training more accessible to a broader range of students.
  
  Moreover, LLMs have been shown to positively influence the forethought phase of learning,
  where students set goals and plan their learning strategies.
  This enhancement is particularly notable in cognitive/metacognitive regulation and motivational/affective regulation,
  suggesting that LLMs can effectively support students in monitoring their learning progress and adapting their strategies as 
  needed [2]. The adaptability of LLMs makes them valuable tools for fostering metacognitive awareness and enhancing students' 
  ability to self-regulate their learning processes.
  
  ### Self-Regulated Learning: LLMs vs. Traditional Methods
  
  The differences in how students engage in self-regulated learning when using LLMs compared to traditional study methods are 
  both nuanced and significant. Traditional note-taking methods have long been valued for their ability to promote deeper 
  cognitive engagement and aid memory retention. However, LLMs offer unique advantages, such as reducing cognitive load and 
  making complex material more accessible. This ease of use can enhance students' motivation and engagement, particularly 
  when dealing with challenging subjects [3].
  
  Despite the perceived benefits of LLMs, research indicates that traditional note-taking remains 
  crucial for fostering deeper understanding and memory retention. A study involving 405 secondary school students 
  found that while both note-taking and a combination of note-taking with LLMs significantly improved 
  reading comprehension and retention compared to using LLMs alone, students generally preferred the LLM for its 
  perceived ease of use and ability to simplify complex material [3]. 
  This suggests that a nuanced approach to self-regulated learning, incorporating both methods, may be most effective.
  
  Interestingly, the study also identified various "archetypes" of student interaction with LLMs, 
  highlighting different strategies employed in self-regulated learning. 
  This diversity in interaction patterns underscores the adaptability of LLMs to different learning styles and preferences, 
  further enhancing their potential as tools for self-regulated learning [3].
  
  ### Assessing Cognitive Engagement
  
  Assessing the cognitive engagement of students when they interact with LLMs versus traditional study methods 
  involves a combination of quantitative and qualitative methods. Quantitative measures, 
  such as standardized tests for reading comprehension and retention, provide objective insights 
  into the effectiveness of different study methods. Qualitative feedback from students offers valuable context, 
  revealing their preferences and experiences with each method [4].
  
  One innovative approach to assessing cognitive engagement involves analyzing the discourse generated in 
  tutoring conversations with LLMs. This method allows for the classification of cognitive engagement 
  levels based on students' questions, explanations, and reasoning, providing deeper insights than traditional metrics. 
  The ICAP framework, which categorizes engagement into four levels—Interactive, Constructive, Active, 
  and Passive—has been used to evaluate the quality of mental effort in learning processes.
  Higher levels of cognitive engagement, particularly constructive and interactive engagement,
  are linked to improved learning outcomes [5].
  
  ### Conclusion
  
  The integration of LLMs into educational settings offers a transformative approach to
  enhancing students' metacognitive processes and self-regulated learning. 
  While traditional study methods remain valuable for promoting deeper understanding and memory retention, 
  LLMs provide unique advantages in accessibility, adaptability, and personalized feedback. 
  The combination of these methods holds significant potential for fostering more effective and engaging learning experiences.
  
  ### Sources
  
  [1] https://dl.acm.org/doi/10.1145/3657604.3662042
  
  [2] https://www.frontiersin.org/journals/education/articles/10.3389/feduc.2025.1738751/full
  
  [3] https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5095149
  
  [4] https://peer.asee.org/help-or-hype-exploring-llm-based-chatbots-in-self-regulated-learning.pdf
  
  [5] https://aclanthology.org/2025.aimecon-wip.6.pdf

        


