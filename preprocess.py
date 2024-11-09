from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from llm_helper import model
import json
import os

def preprocess_data(file_path, new_file_path = None):
    
    enriched_posts = []
    
    with open(file_path, encoding = "utf-8") as f:
        
        posts = json.load(f)
        for post in posts:
            metadata = extract_metadata(post['text'])
            post_with_metadata = post | metadata
            enriched_posts.append(post_with_metadata)
            
    unified_tags = get_unified_tags(enriched_posts)
        
    
    for post in  enriched_posts:
        current_tags = post['tags']
        new_tags = set(unified_tags[tag] for tag in current_tags)
        post['tags'] = list(new_tags)
    
    with open(new_file_path, encoding="utf-8", mode="w") as file:
        json.dump(enriched_posts, file, indent=4)
        
        
def get_unified_tags(posts):
    
    unique_tags = set()
    
    for post in posts:
        unique_tags.update(post['tags'])
        
    unique_tags_list  = ','.join(unique_tags)
    
    template = '''Create a unified mapping of similar tags following these rules:

            1. Map semantically similar tags to a single standardized tag:
            - Job-related: "Jobseekers", "Job Hunting" → "Job Search"
            - Growth-related: "Personal Growth", "Personal Development" → "Self Improvement"
            - Inspiration-related: "Motivation", "Inspiration", "Drive" → "Motivation"
            - Warning-related: "Scam Alert", "Job Scam" → "Scams"

            2. Use Title Case for all unified tags (e.g., "Job Search", "Self Improvement")

            Return only a JSON object mapping original tags to their unified versions, like:
            {{
                "jobseekers": "Job Search",
                "job hunting": "Job Search",
                "personal development": "Self Improvement"
            }}

            Tags to unify:
            {tags}
        '''
        
    prompt_template = PromptTemplate.from_template(template = template)
    
    chain = prompt_template | model
    
    response = chain.invoke(input = {"tags" : str(unique_tags_list)})
    
    try:
        json_parser = JsonOutputParser()
        response = json_parser.parse(response.content)
    except OutputParserException:
        raise  OutputParserException("Failed to parse JSON response")
    return response
            
def extract_metadata(post):
    
    template = '''Extract information from the given LinkedIn post and return a JSON with three keys:

            1. "line_count": Count of actual text lines (excluding empty lines)
            2. "language": Must be either "English" or "Hinglish". Choose "Hinglish" only if post contains significant Hindi words written in English script.
            3. "tags": Array of maximum 2 most relevant topic tags (e.g., ["career", "technology"]) based on post content.

            Return only the JSON object without any explanation or preamble, following this exact format:
            {{
                "line_count": <number>,
                "language": "<English or Hinglish>",
                "tags": ["tag1", "tag2"]
            }}

            Post:
            {post}
        '''
        
    prompt_template = PromptTemplate.from_template(template = template)
    
    chain = prompt_template | model
    
    response = chain.invoke(input={'post':post})
    
    try:
    
        json_parser = JsonOutputParser()
        response = json_parser.parse(response.content)
    except  OutputParserException:
        raise OutputParserException("context is too big, unable to parse it")
    
    return response
    
if __name__ == "__main__":
    preprocess_data("data/raw_posts.json", "data/preprocessed_posts.json")