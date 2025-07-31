You are a system that answers a given question. You are given two sentences. What you need to determine is whether the two sentences are the same or not. Answer "True" if the two sentences are the same, and "False" if they are not. You should also give a reason for your answer. Please answer using the following example and format your answer in Json like { "answer" : "True" , "reason" : "This is a reason" } in Json format. 

Example Candidate sentences : Amrozi accused his brother , whom he called 'the witness' , of deliberately distorting his evidence.  Referring to him as only 'the witness' , Amrozi accused his brother of deliberately distorting his evidence. 
Example Output : { "answer": "True", "reason": "Both sentences convey the same core information: Amrozi accused his brother of deliberately distorting his evidence, and in both cases, the brother is referred to as 'the witness.' The phrasing 'whom he called 'the witness'' and 'Referring to him as only 'the witness'' essentially mean the same thing in this context – that Amrozi used the term 'the witness' to refer to his brother."}

Instruction: 

