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
        for ch in word:
            node = node.children.setdefault(ch, TrieNode())
        if not node.is_end:
            self.word_count += 1
        node.is_end = True
        node.freq = freq

    def remove(self, word):
        def _remove(node, depth):
            if depth == len(word):
                if not node.is_end:
                    return False
                node.is_end = False
                node.freq = 0.0
                self.word_count -= 1
                return len(node.children) == 0
            ch = word[depth]
            if ch not in node.children:
                return False
            should_delete = _remove(node.children[ch], depth + 1)
            if should_delete:
                del node.children[ch]
                return not node.is_end and len(node.children) == 0
            return False

        return _remove(self.root, 0)

    def contains(self, word):
        node = self.root
        for ch in word:
            if ch not in node.children:
                return False
            node = node.children[ch]
        return node.is_end

    def complete(self, prefix, k):
        node = self.root
        for ch in prefix:
            if ch not in node.children:
                return []
            node = node.children[ch]

        results = []
        def dfs(n, path):
            if n.is_end:
                results.append((path, n.freq))
            for c, child in n.children.items():
                dfs(child, path + c)

        dfs(node, prefix)
        results.sort(key=lambda x: (-x[1], x[0]))
        return [w for w, _ in results[:k]]

    def stats(self):
        def height(n):
            if not n.children:
                return 1
            return 1 + max(height(c) for c in n.children.values())

        def count_nodes(n):
            return 1 + sum(count_nodes(c) for c in n.children.values())

        return self.word_count, height(self.root), count_nodes(self.root)

    def items(self):
        result = []
        def dfs(n, path):
            if n.is_end:
                result.append((path, n.freq))
            for c, child in n.children.items():
                dfs(child, path + c)
        dfs(self.root, "")
        return result