from typing import List, Dict
import unicodedata


class TrieNode:
    def __init__(self):
        self.children: Dict[str, "TrieNode"] = {}
        self.is_end_of_word = False
        self.product_ids: List[int] = []


class ProductTrie:
    def __init__(self):
        self.root = TrieNode()

    def _normalize(self, text: str) -> str:
        """Enlève les accents et met en minuscules"""
        text = text.lower()
        return "".join(
            c
            for c in unicodedata.normalize("NFD", text)
            if unicodedata.category(c) != "Mn"
        )

    def insert(self, word: str, product_id: int):
        """Insère chaque mot du nom séparément dans le Trie"""
        words = word.split()  # Sépare les mots

        for w in words:
            normalized = self._normalize(w)
            node = self.root

            for char in normalized:
                if char not in node.children:
                    node.children[char] = TrieNode()
                node = node.children[char]

            node.is_end_of_word = True
            # Éviter les doublons
            if product_id not in node.product_ids:
                node.product_ids.append(product_id)

    def search_prefix(self, prefix: str, limit: int = 10) -> List[int]:
        """Retourne tous les product_ids qui commencent par le préfixe"""
        normalized_prefix = self._normalize(prefix)
        node = self.root

        for char in normalized_prefix:
            if char not in node.children:
                return []
            node = node.children[char]

        return self._collect_all_ids(node, limit)

    def _collect_all_ids(self, node: TrieNode, limit: int) -> List[int]:
        """Collecte les IDs avec une limite"""
        results = node.product_ids[:]

        if len(results) >= limit:
            return results[:limit]

        for child in node.children.values():
            remaining = limit - len(results)
            if remaining <= 0:
                break
            results.extend(self._collect_all_ids(child, remaining))

        return results[:limit]


product_trie = ProductTrie()
