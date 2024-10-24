import csv
from difflib import SequenceMatcher
from typing import List, Dict, Tuple
from itertools import combinations, groupby
import time


def similarity(a: str, b: str, cache: Dict[Tuple[str, str], float]) -> float:
    """Calculate similarity ratio with caching to avoid redundant comparisons."""
    if (a, b) in cache:
        return cache[(a, b)]
    if (b, a) in cache:
        return cache[(b, a)]

    sim = SequenceMatcher(None, a or '', b or '').ratio()
    cache[(a, b)] = sim
    return sim


def extract_username(email: str) -> str:
    """Extract the username part of an email (before '@')."""
    return email.split('@')[0] if email else ''


def match_score(contact1: Dict, contact2: Dict, cache: Dict[Tuple[str, str], float]) -> float:
    """Calculate match score with weights and bonus points."""
    if contact1['email'] == contact2['email']:
        return 1.0

    weights = {'email': 0.5, 'name': 0.3, 'address': 0.2}
    score = 0.0

    # Username similarity
    username_sim = similarity(
        extract_username(contact1['email']),
        extract_username(contact2['email']),
        cache
    )
    score += weights['email'] * username_sim

    # Name similarity
    name_sim = similarity(contact1['name'], contact2['name'], cache)
    last_name_sim = similarity(contact1['name1'], contact2['name1'], cache)
    score += weights['name'] * ((name_sim + last_name_sim) / 2)

    # Address similarity
    address_sim = similarity(contact1.get('address', ''), contact2.get('address', ''), cache)
    score += weights['address'] * address_sim

    return min(score, 1.0)


def cluster_contacts(contacts: List[Dict]) -> Dict[str, List[Dict]]:
    """Group contacts by the first letter of their name to reduce comparisons."""
    contacts.sort(key=lambda x: x['name'][0].lower())  # Sort by first letter
    grouped = groupby(contacts, key=lambda x: x['name'][0].lower())
    return {key: list(group) for key, group in grouped}


def find_potential_duplicates(contacts: List[Dict]) -> List[Tuple[int, int, str]]:
    """Find potential duplicate contacts with clustering and caching."""
    cache = {}  # Cache for similarity scores
    matches = []

    # Cluster contacts by the first letter of their name
    clusters = cluster_contacts(contacts)

    # Compare only within each cluster
    for _, group in clusters.items():
        for contact1, contact2 in combinations(group, 2):
            score = match_score(contact1, contact2, cache)
            accuracy = 'High' if score >= 0.75 else 'Low'
            matches.append((contact1['contactID'], contact2['contactID'], accuracy))

    return matches


def read_contacts_from_csv(file_path: str) -> List[Dict]:
    """Read contact data from a CSV file."""
    contacts = []
    with open(file_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            contacts.append({
                'contactID': int(row['contactID']),
                'name': row['name'],
                'name1': row['name1'],
                'email': row['email'],
                'address': row.get('address', '')
            })
    return contacts


def write_matches_to_csv(matches: List[Tuple[int, int, str,float]], output_file: str):
    """Write the match results to a CSV file."""
    with open(output_file, mode='w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Source Contact ID', 'Match Contact ID', 'Accuracy','Score'])
        writer.writerows(matches)

if __name__ == '__main__':
    # Start the timer
    start_time = time.time()
    input_file = 'contacts.csv' 
    output_file = 'matches.csv'
    contacts = read_contacts_from_csv(input_file)
    duplicates_start = time.time()
    matches = find_potential_duplicates(contacts)
    duplicates_end = time.time()
    write_matches_to_csv(matches, output_file)
    end_time = time.time()
    total_time = end_time - start_time
    duplicates_time = duplicates_end - duplicates_start
    print(f"Total execution time: {total_time:.2f} seconds")
    print(f"Time spent finding duplicates: {duplicates_time:.2f} seconds")
    print(f"Matches written to {output_file}")
