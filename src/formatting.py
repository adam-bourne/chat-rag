import pandas as pd

def format_data(chunk: dict) -> dict:
    """Takes a dict from the train.json data, combines the relevant data fields 
    (pre_text, post_text, table) into a single string, and returns a new dict
    
    Args:
        chunk (dict): a dict from the train.json file
    
    Returns:
        a new dict with the id, text, and year fields
    """ 
    
    # TEXT FORMATTING
    # pre text
    pre_text = "\n".join(chunk["pre_text"])

    # looks like all the chunks have the same table structure
    df = pd.DataFrame(chunk["table"][1:],  # Data rows
                        columns=[''] + chunk["table"][0][1:]) 
    table_text = df.to_markdown(
        index=False,
        tablefmt='pipe', 
        numalign='right',
        stralign='left'
    )

    # post text
    post_text = "\n".join(chunk["post_text"])

    # combine text
    total_text = pre_text + "\n\n" + table_text + "\n\n" + post_text

    # GET YEAR
    year = int(chunk["filename"].split('/')[1])
    
    # RETURN DICT
    return {
        "id": chunk["id"],
        "text": total_text,
        "year": year
    }

def format_ranked_docs(ranked_docs: list[dict]) -> str:
    """Format the ranked documents for the prompt"""

    format_reranked = ""
    for i, doc in enumerate(ranked_docs):
        format_reranked += f"<document_{i}>\nDoc ID: {doc['id']}\n Doc Content:{doc['text']}\n</document_{i}>\n\n"
    
    return format_reranked