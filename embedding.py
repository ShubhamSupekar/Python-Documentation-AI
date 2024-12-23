from sentence_transformers import SentenceTransformer
import json
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer('all-MiniLM-L6-v2')


with open('PythonDoc.json', 'r') as file:
    data = json.load(file)


# Combine description fields to create embeddings
corpus = [f"{item['function']} {item['description']} {item['query']} {item['eg_Description']}" for item in data]
embeddings = model.encode(corpus)

print("Done Embedding")

# Example: Test unrelated query
# query = "How to get the current date and time?"
test_queries = [
    # Mathematical Operations
    "How to calculate the absolute value of a number?",
    "How to round a number to the nearest integer?",
    "How to find the maximum value in a list?",

    # String Manipulations
    "How can I convert a string to uppercase?",
    "How to replace parts of a string with something else?",
    "How do I check if a string contains only numbers?",

    # List and Dictionary Operations
    "How do I sort a list in Python?",
    "How can I get the keys of a dictionary?",
    "How do I reverse a list in Python?",

    # File Handling
    "How to read a file line by line in Python?",
    "How do I write data to a text file?",
    "How can I check if a file exists?",

    # Date and Time
    "How to get the current date and time?",
    "How can I calculate the difference between two dates?",
    "How to format a date in Python?",

    # Control Flow
    "How can I iterate over a range of numbers?",
    "How do I use Python's enumerate function?",

    # Built-in Utilities
    "How to check the type of a variable in Python?",
    "How can I get help on a function in Python?",
    "How to evaluate a string as Python code?",

    # Advanced Queries
    # Error Handling
    "How do I catch exceptions in Python?",
    "What is the syntax for a try-except block?",

    # Modules and Libraries
    "How can I import a module in Python?",
    "How do I use the math module to calculate square root?",

    # Data Structures
    "How do I create a set in Python?",
    "How can I merge two dictionaries together?",

    # Input and Output
    "How do I take input from a user in Python?",
    "How to print formatted output in Python?",

    # Functional Programming
    "How can I apply a function to all elements in a list?",
    "What does the map function do in Python?",

    # Edge Case Queries
    # Unrelated Queries
    "How to bake a cake?",  # Test unrelated query handling

    # Ambiguous Queries
    "What does max do?",
    "How to use Python's open function?",

    # Complex Queries
    "How do I get the absolute value and round a number at the same time?"
]


for query in test_queries:

    query_embedding = model.encode(query)

    # Compute similarity with all function embeddings
    scores = cosine_similarity([query_embedding], embeddings)[0]

    # Get the most similar function
    most_similar_index = scores.argmax()
    print(query)
    print(f"Most similar function: {data[most_similar_index]['function']}")
    print(f"Similarity score: {scores[most_similar_index]}")
    print()