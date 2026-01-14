#!/usr/bin/env python3
import re

# Define the mapping of singular to plural forms only
# The script will automatically detect what changed
plural_mappings = [
    ("Apfel", "Äpfel"),
    ("Orange", "Orangen"),
    ("Kaffee", "Kaffees"),
    ("Saft", "Säfte"),
    ("Brötchen", "Brötchen"),
    ("Würstchen", "Würstchen"),
    ("Wurst", "Würste"),
    ("Birne", "Birnen"),
    ("Joghurt", "Joghurts"),
    ("Zwiebel", "Zwiebeln"),
    ("Großvater", "Großväter"),
    ("Großmutter", "Großmütter"),
    ("Mutter", "Mütter"),
    ("Vater", "Väter"),
    ("Onkel", "Onkel"),
    ("Tante", "Tanten"),
    ("Schwester", "Schwestern"),
    ("Bruder", "Brüder"),
    ("Frau", "Frauen"),
    ("Mann", "Männer"),
    ("Cousin", "Cousins"),
    ("Cousine", "Cousinen"),
    ("Schwiegersohn", "Schwiegersöhne"),
    ("Schwiegertochter", "Schwiegertöchter"),
    ("Enkel", "Enkel"),
    ("Enkelin", "Enkelinnen"),
    ("Sack", "Säcke"),
    ("Schachtel", "Schachteln"),
    ("Tüte", "Tüten"),
    ("Becher", "Becher"),
    ("Sechserpack", "Sechserpacks"),
    ("Dose", "Dosen"),
    ("Stück", "Stücke"),
    ("Rolle", "Rollen"),
    ("Glas", "Gläser"),
    ("Tafel", "Tafeln"),
    ("Flasche", "Flaschen"),
    ("Kasten", "Kästen"),
    ("Karton", "Kartons"),
    ("Portion", "Portionen"),
    ("Packung", "Packungen"),
    ("Netz", "Netze"),
    ("Haus", "Häuser"),
    ("Wohnung", "Wohnungen"),
    ("Wohnzimmer", "Wohnzimmer"),
    ("Arbeitszimmer", "Arbeitszimmer"),
    ("Kinderzimmer", "Kinderzimmer"),
    ("Schlafzimmer", "Schlafzimmer"),
    ("Bad", "Bäder"),
    ("Flur", "Flure"),
    ("Toilette", "Toiletten"),
    ("Küche", "Küchen"),
    ("Balkon", "Balkone"),
    ("Sofa", "Sofas"),
    ("Sessel", "Sessel"),
    ("Bett", "Betten"),
    ("Tisch", "Tische"),
    ("Lampe", "Lampen"),
    ("Badewanne", "Badewannen"),
    ("Schrank", "Schränke"),
    ("Stuhl", "Stühle"),
    ("Dusche", "Duschen"),
    ("Regal", "Regale"),
    ("Waschbecken", "Waschbecken"),
    ("Herd", "Herde"),
    ("Spiegel", "Spiegel"),
    ("Couch", "Couches"),
    ("Teppich", "Teppiche"),
    ("Kühlschrank", "Kühlschränke"),
    ("Uhr", "Uhren"),
    ("Waschmaschine", "Waschmaschinen"),
    ("Fernseher", "Fernseher"),
    ("Reiskocher", "Reiskocher"),
]

def find_changed_parts(singular, plural):
    """
    Compare singular and plural forms and identify all changed/added characters.
    Returns a list of changed character substrings in the plural form.
    """
    if singular == plural:
        return []
    
    # Simple character-by-character comparison approach
    changed_parts = []
    i = 0  # index in singular
    j = 0  # index in plural
    
    while i < len(singular) or j < len(plural):
        if i < len(singular) and j < len(plural) and singular[i] == plural[j]:
            # Characters match, move both forward
            i += 1
            j += 1
        else:
            # Characters don't match or one string is exhausted
            # Collect the changed/added substring in plural
            start_j = j
            
            # Try to find the next matching character
            found_match = False
            for look_ahead_i in range(i, len(singular)):
                for look_ahead_j in range(j, len(plural)):
                    if singular[look_ahead_i] == plural[look_ahead_j]:
                        # Found a potential match
                        changed_parts.append(plural[start_j:look_ahead_j])
                        i = look_ahead_i
                        j = look_ahead_j
                        found_match = True
                        break
                if found_match:
                    break
            
            if not found_match:
                # No match found, rest of plural is changed
                changed_parts.append(plural[start_j:])
                break
    
    # Filter out empty strings
    changed_parts = [p for p in changed_parts if p]
    return changed_parts

def create_colored_plural(plural_word, changed_parts):
    """Create a plural word with only the changed parts colored in orange"""
    if not changed_parts:
        return plural_word
    
    # Build the result by iterating through the plural word
    result = ""
    i = 0
    while i < len(plural_word):
        # Check if current position starts with any changed part
        found_change = False
        for changed in changed_parts:
            if plural_word[i:i+len(changed)] == changed:
                # Color this part in orange
                result += '<span style=""color: rgb(255, 140, 0);"">' + changed + '</span>'
                i += len(changed)
                found_change = True
                break
        
        if not found_change:
            result += plural_word[i]
            i += 1
    
    return result

def process_file(input_file, output_file):
    """
    Process A1.1_fix.txt:
    1. Find all plural words (after <small>pl</small> tag)
    2. Remove all color spans from them
    3. Apply new orange coloring to changed letters only
    """
    
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("Processing file...")
    changes = 0
    
    # For each plural mapping, find and update the plural forms
    for singular, plural in plural_mappings:
        # Detect what changed between singular and plural
        changed_parts = find_changed_parts(singular, plural)
        
        # Pattern to find the plural form after <small>pl</small> tag
        # It may have any color span wrapping it
        # Pattern: <small>pl</small> </span>die <span style=""...[word]</span>
        # or: <small>pl</small> </span>die [word] (uncolored)
        
        # Match: <small>pl</small> with any whitespace, then "die" and the word (with or without color spans)
        pattern = (
            r'(<span style=""color: rgb\(181, 181, 181\);"">\s*<small>pl</small>\s*</span>\s*die\s+)'
            r'(?:<span style=""color: rgb\([^)]+\);"">[^<]*(?:</span>[^<]*)*(?:<span style=""color: rgb\([^)]+\);"">[^<]*</span>)*|'
            + re.escape(plural) + 
            r')'
        )
        
        # Simpler approach: just replace any colored or uncolored version of the plural word
        # after <small>pl</small> with the correctly colored version
        
        # First, remove all coloring from the plural word
        uncolored_plural = plural
        
        # Create replacement: the capture group (prefix up to "die ") + the new colored plural
        if changed_parts:
            colored_plural = create_colored_plural(plural, changed_parts)
        else:
            colored_plural = uncolored_plural
        
        # Find patterns where plural word appears after <small>pl</small>
        # Pattern 1: <small>pl</small> </span>die <span ...>plural</span>
        pattern1 = (
            r'(<span style=""color: rgb\(181, 181, 181\);"">\s*<small>pl</small>\s*</span>\s*die\s+)'
            r'<span style=""color: rgb\([^)]+\);"">' + re.escape(plural) + r'</span>'
        )
        
        matches = len(re.findall(pattern1, content))
        if matches > 0:
            content = re.sub(pattern1, r'\1' + colored_plural, content)
            changes += matches
            print(f"  Updated {matches} occurrences of plural '{plural}'")
        
        # Pattern 2: <small>pl</small> </span>die plural (uncolored, with or without spaces)
        pattern2 = (
            r'(<span style=""color: rgb\(181, 181, 181\);"">\s*<small>pl</small>\s*</span>\s*die\s+)'
            + re.escape(plural) + r'(?=[\s\n"])'
        )
        
        matches = len(re.findall(pattern2, content))
        if matches > 0:
            content = re.sub(pattern2, r'\1' + colored_plural, content)
            changes += matches
            print(f"  Updated {matches} more occurrences of plural '{plural}'")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"\nProcessed file saved to {output_file}")
    print(f"Total changes made: {changes}")

if __name__ == "__main__":
    input_file = r"c:\code\anki_deutsch_cards\A1.1_fix.txt"
    output_file = r"c:\code\anki_deutsch_cards\A1.1_fix_updated.txt"
    process_file(input_file, output_file)
