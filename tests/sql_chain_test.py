import asyncio
import os
print(os.getcwd())
import sys
sys.path.append(os.getcwd())
from backend.chains.sql_chain import sql_chain_invoke
        
asyncio.set_event_loop(asyncio.new_event_loop()) 
loop = asyncio.get_event_loop()

questions = ["What customer made the most purchases?", 
             "What tracks did they purchase?", 
             "What album is the first track from?",
            "Name all the songs in that album."]
chat_history = ""

for question in questions:
    asyncio.set_event_loop(asyncio.new_event_loop()) 
    loop = asyncio.get_event_loop()
    
    
    output_text = loop.run_until_complete(
                        sql_chain_invoke(
                                        question=question,
                                        chat_history=chat_history))
    chat_history += ('Human: '+question+'\nAI: '+output_text+'\n')
    
print(chat_history)