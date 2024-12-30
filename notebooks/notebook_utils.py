"""Misc utils used in the notebooks"""
import pandas as pd
from gliner import GLiNER

ner_model = GLiNER.from_pretrained("urchade/gliner_medium-v2.1")

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

def get_range(question: str) -> tuple:
    """Takes a question, extracts the years mentioned, and takes the latest year.
    Then will create a year containing the latest year and the next year.
    This should encompass a lot of the documts."""

    labels = ["Year"]
    entities = ner_model.predict_entities(question, labels, threshold=0.5)
    
    try:
        # sometimes we get errors if the entraction doesn't convert to an int
        years = (int(entity['text']) for entity in entities)
        max_year = max(years)
        return (max_year + 1, max_year)
    except:
        return ()
