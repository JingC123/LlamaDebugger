class TrieNode:
    def __init__(self):
        self.children = {}  # Dictionary to store child nodes
        self.is_end_of_word = False  # Flag to mark the end of a word

class WordSearch:
    def __init__(self):
        self.root = TrieNode()  # Initialize the root of the Trie

    def insert(self, word):
        """
        Insert a word into the Trie.
        """
        current = self.root
        for char in word:
            if char not in current.children:
                current.children[char] = TrieNode()
            current = current.children[char]
        current.is_end_of_word = True

    def search(self, word):
        """
        Search for a word in the Trie with support for '.' and '*'.
        """

        def dfs(node, i):
            if i == len(word):
                return node.is_end_of_word

            char = word[i]

            if char == '*':
                # '*' matches zero or more of any characters
                # Try matching zero occurrences
                if dfs(node, i + 1):
                    return True
                # Try matching one or more occurrences by traversing all possible paths
                for child in node.children.values():
                    if dfs(child, i):
                        return True
                return False

            elif i + 1 < len(word) and word[i + 1] == '*':
                # Handle character followed by '*', matching zero or more occurrences
                # Try matching zero occurrences
                if dfs(node, i + 2):
                    return True
                # Try matching one or more occurrences
                if char == '.':
                    for child in node.children.values():
                        if dfs(child, i):
                            return True
                else:
                    if char in node.children and dfs(node.children[char], i):
                        return True
                return False

            elif char == '.':
                # '.' matches any single character
                for child in node.children.values():
                    if dfs(child, i + 1):
                        return True
                return False

            else:
                # Regular character match
                if char in node.children:
                    return dfs(node.children[char], i + 1)
                else:
                    return False

        return dfs(self.root, 0)

def test_word_search_with_wildcard_and_star():
    # Initialize the WordSearch (Trie) object
    word_search = WordSearch()

    # Insert words into the Trie
    word_search.insert("hello")
    word_search.insert("hi")
    word_search.insert("apple")
    word_search.insert("happy")
    word_search.insert("hat")
    word_search.insert("ha")

    # Testcase 1: Exact match
    result1 = word_search.search("hello")
    print(f"Search 'hello': {result1}")  # Expected: True

    # Testcase 2: Match with '.'
    result2 = word_search.search("h.llo")
    print(f"Search 'h.llo': {result2}")  # Expected: True

    # Testcase 3: Match with '*' for 0 occurrences
    result3 = word_search.search("ha*")
    print(f"Search 'ha*': {result3}")  # Expected: True

    # Testcase 4: Match with '*' for multiple occurrences
    result4 = word_search.search("h.*y")
    print(f"Search 'h.*y': {result4}")  # Expected: True

    # Testcase 5: Match '*' alone (empty string)
    result5 = word_search.search("*")
    print(f"Search '*': {result5}")  # Expected: True

    # Testcase 6: Match with '.' and '*'
    result6 = word_search.search("h.*o")
    print(f"Search 'h.*o': {result6}")  # Expected: True
    
    result8 = word_search.search('hellooo')
    print(f'Search result 8 {result8}')
    # Testcase 7: Match '*' for consecutive characters
    result7 = word_search.search("ha*t")
    print(f"Search 'ha*t': {result7}")  # Expected: True

    # Testcase 8: Non-matching pattern
    result8 = word_search.search("ha*z")
    print(f"Search 'ha*z': {result8}")  # Expected: False

test_word_search_with_wildcard_and_star()