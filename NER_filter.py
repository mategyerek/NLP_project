import pandas as pd
import spacy

# Load the SpaCy model
nlp = spacy.load("en_core_web_sm")


def select_relevant(file_path):
    data = pd.read_csv(file_path)

    # Define keywords related to the Russia-Ukraine conflict
    conflict_keywords = [
        "Ukraine", "Russia", "Putin", "Zelensky", "Kyiv", "Donbas"
        "Crimea", "Donetsk", "Luhansk", "Moscow", "Kremlin", "Moscow", 
        "NATO", "Mariupol", "Odesa", "Odessa", "Volodymyr", "Valdimir",
    ]

    # Filter the dataset to select only the rows where 'Parent ID' is None
    filtered_data = data[data['Parent ID'].isna()]
    relevant_IDs = []
    total_rows = len(filtered_data)
    for i in range(len(filtered_data)):
        if i % (total_rows // 20) == 0:  # Print progress every 5%
            print(f"Progress: {i / total_rows * 100:.2f}%")
        text = filtered_data.iloc[i]['Text']
        doc = nlp(text)
        for ent in doc.ents:
            if ent.text in conflict_keywords:
                relevant_IDs.append(filtered_data.iloc[i]['Post ID'])
    
    result = data[data['Parent ID'].isin(relevant_IDs) | data['Post ID'].isin(relevant_IDs)]
    if "combat" in file_path:
        result.to_csv("data/filtered_combatfootage.csv", index=False)
    else:
        result.to_csv("data/filtered_geopolitics.csv", index=False)

select_relevant(r"data\geopolitics_parent_child.csv")
select_relevant(r"data\combatfootage_parent_child.csv")