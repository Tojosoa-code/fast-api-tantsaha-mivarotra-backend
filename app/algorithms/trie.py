from typing import List, Dict


class TrieNode:
    def __init__(self):
        self.children: Dict[str, "TrieNode"] = {}
        self.is_end_of_word = False
        self.product_ids: List[int] = []


class ProductTrie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str, product_id: int):
        node = self.root
        for char in word.lower():
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True
        node.product_ids.append(product_id)

    def search_prefix(self, prefix: str) -> List[int]:
        """Retourne tous les product_ids qui commencent par le préfixe"""
        node = self.root
        for char in prefix.lower():
            if char not in node.children:
                return []
            node = node.children[char]
        return self._collect_all_ids(node)

    def _collect_all_ids(self, node: TrieNode) -> List[int]:
        results = node.product_ids[:]
        for child in node.children.values():
            results.extend(self._collect_all_ids(child))
        return results


product_trie = ProductTrie()
