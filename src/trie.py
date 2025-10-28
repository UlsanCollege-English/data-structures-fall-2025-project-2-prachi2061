class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False
        self.freq = 0.0

class Trie:
    def __init__(self):
        self.root = TrieNode()
        self.word_count = 0

    def insert(self, word, freq):
        node = self.root
        for char in word:
            node = node.children.setdefault(char, TrieNode())
        if not node.is_end:
            self.word_count += 1
        node.is_end = True
        node.freq = freq

    def remove(self, word):
        def _remove(node, word, depth):
            if depth == len(word):
                if not node.is_end:
                    return False
                node.is_end = False
                node.freq = 0.0
                self.word_count -= 1
                return len(node.children) == 0
            char = word[depth]
            if char not in node.children:
                return False
            should_delete = _remove(node.children[char], word, depth + 1)
            if should_delete:
                del node.children[char]
                return not node.is_end and len(node.children) == 0
            return False

        return _remove(self.root, word, 0)

    def contains(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end

    def complete(self, prefix, k):
        def dfs(node, path, results):
            if node.is_end:
                results.append((path, node.freq))
            for char, child in node.children.items():
                dfs(child, path + char, results)

        node = self.root
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]

        results = []
        dfs(node, prefix, results)
        results.sort(key=lambda x: -x[1])
        return [word for word, _ in results[:k]]

    def stats(self):
        def height(node):
            if not node.children:
                return 1
            return 1 + max(height(child) for child in node.children.values())

        def count_nodes(node):
            return 1 + sum(count_nodes(child) for child in node.children.values())

        return self.word_count, height(self.root), count_nodes(self.root)

    def items(self):
        result = []

        def dfs(node, path):
            if node.is_end:
                result.append((path, node.freq))
            for char, child in node.children.items():
                dfs(child, path + char)

        dfs(self.root, "")
        return result